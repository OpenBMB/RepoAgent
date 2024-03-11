"""存储doc对应的信息，同时处理引用的关系
"""
from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, field
from enum import Enum, auto, unique
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import jedi
from colorama import Fore, Style
from prettytable import PrettyTable
from tqdm import tqdm

from repo_agent.file_handler import FileHandler
from repo_agent.log import logger
from repo_agent.multi_task_dispatch import Task, TaskManager
from repo_agent.settings import setting
from repo_agent.utils.meta_info_utils import latest_verison_substring


@unique
class EdgeType(Enum):
    reference_edge = auto()  # 一个obj引用另一个obj
    subfile_edge = auto()  # 一个 文件/文件夹 属于一个文件夹
    file_item_edge = auto()  # 一个 obj 属于一个文件


@unique
class DocItemType(Enum):
    # 对可能的对象文档类型进行定义（分不同细粒度）
    _repo = auto()  # 根节点，需要生成readme
    _dir = auto()
    _file = auto()
    _class = auto()
    _class_function = auto()
    _function = auto()  # 文件内的常规function
    _sub_function = auto()  # function内的定义的subfunction
    _global_var = auto()

    def to_str(self):
        if self == DocItemType._class:
            return "ClassDef"
        elif self == DocItemType._function:
            return "FunctionDef"
        elif self == DocItemType._class_function:
            return "FunctionDef"
        elif self == DocItemType._sub_function:
            return "FunctionDef"
        # assert False, f"{self.name}"
        return self.name

    def print_self(self):
        color = Fore.WHITE
        if self == DocItemType._dir:
            color = Fore.GREEN
        elif self == DocItemType._file:
            color = Fore.YELLOW
        elif self == DocItemType._class:
            color = Fore.RED
        elif self in [ DocItemType._function, DocItemType._sub_function, DocItemType._class_function]:
            color = Fore.BLUE
        return color + self.name + Style.RESET_ALL

    def get_edge_type(self,
        from_item_type: DocItemType, to_item_type: DocItemType
    ):
        pass


@unique
class DocItemStatus(Enum):
    doc_up_to_date = auto()  # 无需生成文档
    doc_has_not_been_generated = auto()  # 文档还未生成，需要生成
    code_changed = auto()  # 源码被修改了，需要改文档
    add_new_referencer = auto()  # 添加了新的引用者
    referencer_not_exist = auto()  # 曾经引用他的obj被删除了，或者不再引用他了


def need_to_generate(doc_item: DocItem, ignore_list: List[str]  = []) -> bool:
    """只生成item的，文件及更高粒度都跳过。另外如果属于一个blacklist的文件也跳过"""
    if doc_item.item_status == DocItemStatus.doc_up_to_date:
        return False
    rel_file_path = doc_item.get_full_name()
    if doc_item.item_type in [DocItemType._file, DocItemType._dir, DocItemType._repo]: #暂时不生成file及以上的doc
        return False
    doc_item = doc_item.father
    while doc_item:
        if doc_item.item_type == DocItemType._file:
            # 如果当前文件在忽略列表中，或者在忽略列表某个文件路径下，则跳过
            if any(
                rel_file_path.startswith(ignore_item) for ignore_item in ignore_list
            ):
                return False
            else:
                return True
        doc_item = doc_item.father
    return False

@dataclass
class DocItem:
    item_type: DocItemType = DocItemType._class_function
    item_status: DocItemStatus = DocItemStatus.doc_has_not_been_generated

    obj_name: str = "" #对象的名字
    code_start_line: int = -1
    code_end_line: int = -1
    md_content: List[str] = field(default_factory=list) #存储不同版本的doc
    content: Dict[Any,Any] = field(default_factory=dict) #原本存储的信息

    children: Dict[str, DocItem] = field(default_factory=dict)  # 子对象
    father: Any[DocItem] = None

    depth: int = 0
    tree_path: List[DocItem] = field(default_factory=list)  # 一整条链路，从root开始
    max_reference_ansce: Any[DocItem] = None

    reference_who: List[DocItem] = field(default_factory=list) #他引用了谁
    who_reference_me: List[DocItem] = field(default_factory=list) #谁引用了他
    special_reference_type: List[bool] = field(default_factory=list)

    reference_who_name_list: List[str] = field(default_factory=list) #他引用了谁，这个可能是老版本
    who_reference_me_name_list: List[str] = field(default_factory=list) #谁引用了他，这个可能是老版本的

    has_task: bool = False

    multithread_task_id: int = -1  # 在多线程中的task_id


    @staticmethod
    def has_ans_relation(now_a: DocItem, now_b: DocItem):
        """Check if there is an ancestor relationship between two nodes and return the earlier node if exists.

        Args:
            now_a (DocItem): The first node.
            now_b (DocItem): The second node.

        Returns:
            DocItem or None: The earlier node if an ancestor relationship exists, otherwise None.
        """
        if now_b in now_a.tree_path:
            return now_b
        if now_a in now_b.tree_path:
            return now_a
        return None


    def get_travel_list(self):
        '''按照先序遍历的顺序，根节点在第一个'''
        now_list = [self]
        for _, child in self.children.items():
            now_list = now_list + child.get_travel_list()
        return now_list
    
    def check_depth(self):
        """
        Recursively calculates the depth of the node in the tree.

        Returns:
            int: The depth of the node.
        """
        if len(self.children) == 0:
            self.depth = 0
            return self.depth
        max_child_depth = 0
        for _, child in self.children.items():
            child_depth = child.check_depth()
            max_child_depth = max(child_depth, max_child_depth)
        self.depth = max_child_depth + 1
        return self.depth

    def parse_tree_path(self, now_path):
        """
        Recursively parses the tree path by appending the current node to the given path.

        Args:
            now_path (list): The current path in the tree.

        Returns:
            None
        """
        self.tree_path = now_path + [self]
        for key, child in self.children.items():
            child.parse_tree_path(self.tree_path)

    def get_file_name(self):
        full_name = self.get_full_name()
        return full_name.split(".py")[0] + ".py"

    def get_full_name(self, strict = False):
            """获取从下到上所有的obj名字

            Returns:
                str: 从下到上所有的obj名字，以斜杠分隔
            """
            if self.father == None:
                return self.obj_name
            name_list = []
            now = self
            while now != None:
                self_name = now.obj_name
                if strict:
                    for name, item in self.father.children.items():
                        if item == now:
                            self_name = name
                            break
                    if self_name != now.obj_name:
                        self_name = self_name + "(name_duplicate_version)"
                name_list = [self_name] + name_list
                now = now.father

            name_list = name_list[1:]
            return "/".join(name_list)

    def find(self, recursive_file_path: list) -> Optional[DocItem]:
        """
        从repo根节点根据path_list找到对应的文件, 否则返回False

        Args:
            recursive_file_path (list): The list of file paths to search for.

        Returns:
            Optional[DocItem]: The corresponding file if found, otherwise None.
        """
        assert self.item_type == DocItemType._repo
        pos = 0
        now = self
        while pos < len(recursive_file_path):
            if not recursive_file_path[pos] in now.children.keys():
                return None
            now = now.children[recursive_file_path[pos]]
            pos += 1
        return now
    
    @staticmethod
    def check_has_task(now_item: DocItem, ignore_list: List[str] = []):
        if need_to_generate(now_item, ignore_list=ignore_list):
            now_item.has_task = True
        for _, child in now_item.children.items():
            DocItem.check_has_task(child, ignore_list)
            now_item.has_task = child.has_task or now_item.has_task

    def print_recursive(self, indent=0, print_content=False, diff_status = False, ignore_list: List[str] = []):
        """递归打印repo对象"""

        def print_indent(indent=0):
            if indent == 0:
                return ""
            return "  " * indent + "|-"
        print_obj_name = self.obj_name
        if self.item_type == DocItemType._repo:
            print_obj_name = setting.project.target_repo
        if diff_status and need_to_generate(self, ignore_list=ignore_list):
            print(
                print_indent(indent) + f"{self.item_type.print_self()}: {print_obj_name} : {self.item_status.name}",
            )
        else:
            print(
                print_indent(indent) + f"{self.item_type.print_self()}: {print_obj_name}",
            )
        for child_name, child in self.children.items():
            if diff_status and child.has_task == False:
                continue
            child.print_recursive(indent=indent + 1, print_content=print_content, diff_status = diff_status, ignore_list = ignore_list)


def find_all_referencer(
    repo_path, variable_name, file_path, line_number, column_number, in_file_only=False
):
    """复制过来的之前的实现"""
    script = jedi.Script(path=os.path.join(repo_path, file_path))
    try:
        if in_file_only:
            references = script.get_references(
                line=line_number, column=column_number, scope="file"
            )
        else:
            references = script.get_references(line=line_number, column=column_number)
        # 过滤出变量名为 variable_name 的引用，并返回它们的位置
        variable_references = [ref for ref in references if ref.name == variable_name]
        # if variable_name == "need_to_generate": 
        #     import pdb; pdb.set_trace()
        return [
            (os.path.relpath(ref.module_path, repo_path), ref.line, ref.column)
            for ref in variable_references
            if not (ref.line == line_number and ref.column == column_number)
        ]
    except Exception as e:
        # 打印错误信息和相关参数
        logger.info(f"Error occurred: {e}")
        logger.info(
            f"Parameters: variable_name={variable_name}, file_path={file_path}, line_number={line_number}, column_number={column_number}"
        )
        return []


@dataclass
class MetaInfo:
    repo_path: str = ""
    document_version: str = (
        ""  # 随时间变化，""代表没完成，否则对应一个目标仓库的commit hash
    )
    target_repo_hierarchical_tree: DocItem = field(
        default_factory="Docitem"
    )  # 整个repo的文件结构
    white_list: Any[List] = None

    fake_file_reflection: Dict[str, str] = field(default_factory=dict)
    jump_files: List[str] = field(default_factory=list)
    deleted_items_from_older_meta: List[List] = field(default_factory=list)

    in_generation_process: bool = False

    checkpoint_lock: threading.Lock = threading.Lock()

    @staticmethod
    def init_meta_info(file_path_reflections, jump_files) -> MetaInfo:
        """从一个仓库path中初始化metainfo"""
        project_abs_path = setting.project.target_repo
        print(f"{Fore.LIGHTRED_EX}Initializing MetaInfo: {Style.RESET_ALL}from {project_abs_path}")
        file_handler = FileHandler(project_abs_path, None)
        repo_structure = file_handler.generate_overall_structure(file_path_reflections, jump_files)
        metainfo = MetaInfo.from_project_hierarchy_json(repo_structure)
        metainfo.repo_path = project_abs_path
        metainfo.fake_file_reflection = file_path_reflections
        metainfo.jump_files = jump_files
        return metainfo

    @staticmethod
    def from_checkpoint_path(checkpoint_dir_path: str | Path ) -> MetaInfo:
        """从已有的metainfo dir里面读取metainfo"""
        project_hierarchy_json_path = os.path.join(
            checkpoint_dir_path, "project_hierarchy.json"
        )

        with open(project_hierarchy_json_path, "r", encoding="utf-8") as reader:
            project_hierarchy_json = json.load(reader)
        metainfo = MetaInfo.from_project_hierarchy_json(project_hierarchy_json)

        with open(
            os.path.join(checkpoint_dir_path, "meta-info.json"), "r", encoding="utf-8"
        ) as reader:
            meta_data = json.load(reader)
            metainfo.repo_path = str(setting.project.target_repo)  # Convert DirectoryPath to string
            metainfo.document_version = meta_data["doc_version"]
            metainfo.fake_file_reflection = meta_data["fake_file_reflection"]
            metainfo.jump_files = meta_data["jump_files"]
            metainfo.in_generation_process = meta_data["in_generation_process"]
            metainfo.deleted_items_from_older_meta = meta_data["deleted_items_from_older_meta"]

        print(
            f"{Fore.CYAN}Loading MetaInfo:{Style.RESET_ALL} {checkpoint_dir_path}"
        )
        return metainfo

    def checkpoint(self, target_dir_path: str | Path, flash_reference_relation=False):
        """
        Save the MetaInfo object to the specified directory.

        Args:
            target_dir_path (str): The path to the target directory where the MetaInfo will be saved.
            flash_reference_relation (bool, optional): Whether to include flash reference relation in the saved MetaInfo. Defaults to False.
        """
        with self.checkpoint_lock:
            print(f"{Fore.GREEN}MetaInfo is Refreshed and Saved{Style.RESET_ALL}")
            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)
            now_hierarchy_json = self.to_hierarchy_json(
                flash_reference_relation=flash_reference_relation
            )
            with open(
                os.path.join(target_dir_path, "project_hierarchy.json"), "w", encoding='utf-8'
            ) as writer:
                json.dump(now_hierarchy_json, writer, indent=2, ensure_ascii=False)

            with open(os.path.join(target_dir_path, "meta-info.json"), "w") as writer:
                meta = {
                    "doc_version": self.document_version,
                    "in_generation_process": self.in_generation_process,
                    "fake_file_reflection": self.fake_file_reflection,
                    "jump_files": self.jump_files,
                    "deleted_items_from_older_meta": self.deleted_items_from_older_meta,
                }
                json.dump(meta, writer, indent=2, ensure_ascii=False)
    
    
    def print_task_list(self, task_dict: Dict[Task]):
        '''打印'''
        task_table = PrettyTable(["task_id","Doc Generation Reason", "Path","dependency"])
        for task_id, task_info in task_dict.items():
            remain_str = "None"
            if task_info.dependencies != []:
                remain_str = ",".join([str(d_task.task_id) for d_task in task_info.dependencies])
                if len(remain_str) > 20:
                    remain_str = remain_str[:8] + "..." + remain_str[-8:]
            task_table.add_row([task_id, task_info.extra_info.item_status.name, task_info.extra_info.get_full_name(strict=True), remain_str])
        # print("Remain tasks to be done")
        print(task_table)

    def get_all_files(self) -> List[DocItem]:
        """获取所有的file节点"""
        files = []

        def walk_tree(now_node):
            if now_node.item_type == DocItemType._file:
                files.append(now_node)
            for _, child in now_node.children.items():
                walk_tree(child)

        walk_tree(self.target_repo_hierarchical_tree)
        return files


    def find_obj_with_lineno(self, file_node: DocItem, start_line_num) -> DocItem:
        """每个DocItem._file，对于所有的行，建立他们对应的对象是谁
        一个行属于这个obj的范围，并且没法属于他的儿子的范围了"""
        now_node = file_node
        # if 
        assert now_node != None
        while len(now_node.children) > 0:
            find_qualify_child = False
            for _, child in now_node.children.items():
                assert child.content != None
                if (
                    child.content["code_start_line"] <= start_line_num
                    and child.content["code_end_line"] >= start_line_num
                ):
                    now_node = child
                    find_qualify_child = True
                    break
            if not find_qualify_child:
                return now_node
        return now_node

    def parse_reference(self):
        """双向提取所有引用关系"""
        file_nodes = self.get_all_files()

        white_list_file_names, white_list_obj_names = (
            [],
            [],
        )  # 如果指定白名单，只处理白名单上的双向引用关系
        if self.white_list != None:
            white_list_file_names = [cont["file_path"] for cont in self.white_list]
            white_list_obj_names = [cont["id_text"] for cont in self.white_list]

        for file_node in tqdm(file_nodes, desc="parsing bidirectional reference"):
            """检测一个文件内的所有引用信息，只能检测引用该文件内某个obj的其他内容。
            1. 如果某个文件是jump-files，就不应该出现在这个循环里
            2. 如果检测到的引用信息来源于一个jump-files, 忽略它
            3. 如果检测到一个引用来源于fake-file,则认为他的母文件是原来的文件
            """
            assert not file_node.get_full_name().endswith(latest_verison_substring)

            ref_count = 0
            rel_file_path = file_node.get_full_name()
            assert rel_file_path not in self.jump_files

            if white_list_file_names != [] and (
                file_node.get_file_name() not in white_list_file_names
            ):  # 如果有白名单，只parse白名单里的对象
                continue

            def walk_file(now_obj: DocItem):
                """在文件内遍历所有变量"""
                nonlocal ref_count, white_list_file_names
                in_file_only = False
                if white_list_obj_names != [] and (
                    now_obj.obj_name not in white_list_obj_names
                ):
                    in_file_only = True  # 作为加速，如果有白名单，白名单obj同文件夹下的也parse，但是只找同文件内的引用

                reference_list = find_all_referencer(
                    repo_path=self.repo_path,
                    variable_name=now_obj.obj_name,
                    file_path=rel_file_path,
                    line_number=now_obj.content["code_start_line"],
                    column_number=now_obj.content["name_column"],
                    in_file_only=in_file_only,
                )
                for referencer_pos in reference_list:  # 对于每个引用
                    referencer_file_ral_path = referencer_pos[0]
                    if referencer_file_ral_path in self.fake_file_reflection.values():
                        """检测到的引用者来自于unstaged files，跳过该引用"""
                        print(
                            f"{Fore.LIGHTBLUE_EX}[Reference From Unstaged Version, skip]{Style.RESET_ALL} {referencer_file_ral_path} -> {now_obj.get_full_name()}"
                        )
                        continue
                    elif referencer_file_ral_path in self.jump_files:
                        """检测到的引用者来自于untracked files，跳过该引用"""
                        print(
                            f"{Fore.LIGHTBLUE_EX}[Reference From Unstracked Version, skip]{Style.RESET_ALL} {referencer_file_ral_path} -> {now_obj.get_full_name()}"
                        )
                        continue

                    target_file_hiera = referencer_file_ral_path.split("/")
                    # for file_hiera_id in range(len(target_file_hiera)):
                    #     if target_file_hiera[file_hiera_id].endswith(fake_file_substring):
                    #         prefix = "/".join(target_file_hiera[:file_hiera_id+1])
                    #         find_in_reflection = False
                    #         for real, fake in self.fake_file_reflection.items():
                    #             if fake == prefix:
                    #                 print(f"{Fore.BLUE}Find Reference in Fake-File: {Style.RESET_ALL}{referencer_file_ral_path} {Fore.BLUE}referred{Style.RESET_ALL} {now_obj.item_type.name} {now_obj.get_full_name()}")
                    #                 target_file_hiera = real.split("/") + target_file_hiera[file_hiera_id+1:]
                    #                 find_in_reflection = True
                    #                 break
                    #         assert find_in_reflection
                    #         break

                    referencer_file_item = self.target_repo_hierarchical_tree.find(target_file_hiera)
                    if referencer_file_item == None:
                        print(
                            f"{Fore.LIGHTRED_EX}Error: Find \"{referencer_file_ral_path}\"(not in target repo){Style.RESET_ALL} referenced {now_obj.get_full_name()}"
                        )
                        continue
                    referencer_node = self.find_obj_with_lineno(referencer_file_item, referencer_pos[1])
                    if referencer_node.obj_name == now_obj.obj_name:
                        logger.info(
                            f"Jedi find {now_obj.get_full_name()} with name_duplicate_reference, skipped"
                        )
                        continue
                    # if now_obj.get_full_name() == "repo_agent/runner.py/Runner/run":
                    #     import pdb; pdb.set_trace()
                    if DocItem.has_ans_relation(now_obj, referencer_node) == None:
                        # 不考虑祖先节点之间的引用
                        if now_obj not in referencer_node.reference_who:
                            special_reference_type = (referencer_node.item_type in [DocItemType._function, DocItemType._sub_function, DocItemType._class_function]) and referencer_node.code_start_line == referencer_pos[1]
                            referencer_node.special_reference_type.append(special_reference_type)
                            referencer_node.reference_who.append(now_obj)
                            now_obj.who_reference_me.append(referencer_node)
                            ref_count += 1
                for _, child in now_obj.children.items():
                    walk_file(child)

            for _, child in file_node.children.items():
                walk_file(child)
            # logger.info(f"find {ref_count} refer-relation in {file_node.get_full_name()}")
    

    def get_task_manager(self, now_node: DocItem, task_available_func) -> TaskManager:
        """先写一个退化的版本，只考虑拓扑引用关系
        """
        doc_items = now_node.get_travel_list()
        if self.white_list != None:

            def in_white_list(item: DocItem):
                for cont in self.white_list:
                    if (
                        item.get_file_name() == cont["file_path"]
                        and item.obj_name == cont["id_text"]
                    ):
                        return True
                return False

            doc_items = list(filter(in_white_list, doc_items))
        doc_items = list(filter(task_available_func, doc_items))
        doc_items = sorted(doc_items, key=lambda x: x.depth) #叶子节点在前面
        deal_items = []
        task_manager = TaskManager()
        bar = tqdm(total = len(doc_items),desc="parsing topology task-list")
        while doc_items:
            min_break_level = 1e7
            target_item = None
            for item in doc_items:
                """一个任务依赖于所有引用者和他的子节点,我们不能保证引用不成环(也许有些仓库的废代码会出现成环)。
                这时就只能选择一个相对来说遵守程度最好的了
                有特殊情况func-def中的param def可能会出现循环引用
                另外循环引用真实存在，对于一些bind类的接口真的会发生，比如：
                ChatDev/WareHouse/Gomoku_HumanAgentInteraction_20230920135038/main.py里面的: on-click、show-winner、restart
                """
                best_break_level = 0
                second_best_break_level = 0
                for _,child in item.children.items(): #父亲依赖儿子的关系是一定要走的
                    if task_available_func(child) and (child not in deal_items):
                        best_break_level += 1
                for referenced,special in zip(item.reference_who,item.special_reference_type):
                    if task_available_func(referenced) and (referenced not in deal_items):
                        best_break_level += 1
                    if task_available_func(referenced) and (not special) and (referenced not in deal_items):
                        second_best_break_level += 1
                if best_break_level == 0:
                    min_break_level = -1
                    target_item = item
                    break
                if second_best_break_level < min_break_level:
                    target_item = item
                    min_break_level = second_best_break_level

            if min_break_level > 0:
                print(f"circle-reference(second-best still failed), level={min_break_level}: {target_item.get_full_name()}")

            item_denp_task_ids = []
            for _, child in target_item.children.items():
                if child.multithread_task_id != -1:
                    assert child.multithread_task_id in task_manager.task_dict.keys()
                    item_denp_task_ids.append(child.multithread_task_id)
            for referenced_item in target_item.reference_who:
                if referenced_item.multithread_task_id in task_manager.task_dict.keys():
                    item_denp_task_ids.append(referenced_item.multithread_task_id)
            item_denp_task_ids = list(set(item_denp_task_ids))  # 去重
            if task_available_func == None or task_available_func(target_item):
                task_id = task_manager.add_task(
                    dependency_task_id=item_denp_task_ids, extra=target_item
                )
                target_item.multithread_task_id = task_id
            deal_items.append(target_item)
            doc_items.remove(target_item)
            bar.update(1)

        return task_manager

    def get_topology(self, task_available_func) -> TaskManager:
        """计算repo中所有对象的拓扑顺序
        """
        self.parse_reference()
        task_manager = self.get_task_manager(
            self.target_repo_hierarchical_tree, task_available_func=task_available_func
        )
        return task_manager

    def _map(self, deal_func: Callable):
        """将所有节点进行同一个操作"""

        def travel(now_item: DocItem):
            deal_func(now_item)
            for _, child in now_item.children.items():
                travel(child)

        travel(self.target_repo_hierarchical_tree)

    def load_doc_from_older_meta(self, older_meta: MetaInfo):
        """older_meta是老版本的、已经生成doc的meta info"""
        logger.info("merge doc from an older version of metainfo")
        root_item = self.target_repo_hierarchical_tree # 新版的根节点
        deleted_items = []
        def find_item(now_item: DocItem) -> Optional[DocItem]:
            """
            Find an item in the new version of meta based on its original item.

            Args:
                now_item (DocItem): The original item to be found in the new version of meta.

            Returns:
                Optional[DocItem]: The corresponding item in the new version of meta if found, otherwise None.
            """
            nonlocal root_item
            if now_item.father == None:  # The root node can always be found
                return root_item
            father_find_result = find_item(now_item.father)
            if not father_find_result:
                return None
            #注意：这里需要考虑 now_item.obj_name可能会有重名，并不一定等于
            real_name = None
            for child_real_name, temp_item in now_item.father.children.items():
                if temp_item == now_item:
                    real_name = child_real_name
                    break
            assert real_name != None
            # if real_name != now_item.obj_name:
            #     import pdb; pdb.set_trace()
            if real_name in father_find_result.children.keys():
                result_item = father_find_result.children[real_name]
                return result_item
            return None

        def travel(now_older_item: DocItem):  # 只寻找源码是否被修改的信息
            # if now_older_item.get_full_name() == "autogen/_pydantic.py/type2schema":
            #     import pdb; pdb.set_trace()
            result_item = find_item(now_older_item)
            if not result_item:  # 新版文件中找不到原来的item，就回退
                deleted_items.append([now_older_item.get_full_name(), now_older_item.item_type.name])
                return
            result_item.md_content = now_older_item.md_content
            result_item.item_status = now_older_item.item_status
            # if result_item.obj_name == "run":
            #     import pdb; pdb.set_trace()
            if "code_content" in now_older_item.content.keys():
                assert "code_content" in result_item.content.keys()
                if (
                    now_older_item.content["code_content"]
                    != result_item.content["code_content"]
                ):  # 源码被修改了
                    result_item.item_status = DocItemStatus.code_changed

            for _, child in now_older_item.children.items():
                travel(child)

        travel(older_meta.target_repo_hierarchical_tree)

        """接下来，parse现在的双向引用，观察谁的引用者改了"""
        self.parse_reference()

        def travel2(now_older_item: DocItem):
            result_item = find_item(now_older_item)
            if not result_item:  # 新版文件中找不到原来的item，就回退
                return
            """result_item引用的人是否变化了"""
            new_reference_names = [
                name.get_full_name(strict=True) for name in result_item.who_reference_me
            ]
            old_reference_names = now_older_item.who_reference_me_name_list
            # if now_older_item.get_full_name() == "autogen/_pydantic.py/type2schema":
            #     import pdb; pdb.set_trace() 
            if not (set(new_reference_names) == set(old_reference_names)) and (
                result_item.item_status == DocItemStatus.doc_up_to_date
            ):
                if set(new_reference_names) <= set(
                    old_reference_names
                ):  # 旧的referencer包含新的referencer
                    result_item.item_status = DocItemStatus.referencer_not_exist
                else:
                    result_item.item_status = DocItemStatus.add_new_referencer
            for _, child in now_older_item.children.items():
                travel2(child)

        travel2(older_meta.target_repo_hierarchical_tree)

        self.deleted_items_from_older_meta = deleted_items

    @staticmethod
    def from_project_hierarchy_path(repo_path: str) -> MetaInfo:
        """project_hierarchy_json全是压平的文件，递归的文件目录都在最终的key里面, 把他转换到我们的数据结构"""
        project_hierarchy_json_path = os.path.join(repo_path, "project_hierarchy.json")
        logger.info(f"parsing from {project_hierarchy_json_path}")
        if not os.path.exists(project_hierarchy_json_path):
            raise NotImplementedError("Invalid operation detected")

        with open(project_hierarchy_json_path, "r", encoding="utf-8") as reader:
            project_hierarchy_json = json.load(reader)
        return MetaInfo.from_project_hierarchy_json(project_hierarchy_json)

    def to_hierarchy_json(self, flash_reference_relation=False):
        """
        Convert the document metadata to a hierarchical JSON representation.

        Args:
            flash_reference_relation (bool): If True, the latest bidirectional reference relations will be written back to the meta file.

        Returns:
            dict: A dictionary representing the hierarchical JSON structure of the document metadata.
        """
        hierachy_json = {}
        file_item_list = self.get_all_files()
        for file_item in file_item_list:
            file_hierarchy_content = []
            
            def walk_file(now_obj: DocItem):
                nonlocal file_hierarchy_content, flash_reference_relation
                temp_json_obj = now_obj.content
                temp_json_obj["name"] = now_obj.obj_name
                temp_json_obj["type"] = now_obj.item_type.to_str()
                temp_json_obj["md_content"] = now_obj.md_content
                temp_json_obj["item_status"] = now_obj.item_status.name
                
                if flash_reference_relation:
                    temp_json_obj["who_reference_me"] = [cont.get_full_name(strict=True) for cont in now_obj.who_reference_me]
                    temp_json_obj["reference_who"] = [cont.get_full_name(strict=True) for cont in now_obj.reference_who]
                    temp_json_obj["special_reference_type"] = now_obj.special_reference_type
                else:
                    temp_json_obj["who_reference_me"] = now_obj.who_reference_me_name_list
                    temp_json_obj["reference_who"] = now_obj.reference_who_name_list
                    # temp_json_obj["special_reference_type"] = 
                file_hierarchy_content.append(temp_json_obj)

                for _, child in now_obj.children.items():
                    walk_file(child)

            for _, child in file_item.children.items():
                walk_file(child)
            hierachy_json[file_item.get_full_name()] = file_hierarchy_content
        return hierachy_json

    @staticmethod
    def from_project_hierarchy_json(project_hierarchy_json) -> MetaInfo:
        target_meta_info = MetaInfo(
            # repo_path=repo_path,
            target_repo_hierarchical_tree=DocItem(  # 根节点
                item_type=DocItemType._repo,
                obj_name="full_repo",
            )
        )

        for file_name, file_content in tqdm(project_hierarchy_json.items(),desc="parsing parent relationship"): 
            # 首先parse file archi
            if not os.path.exists(os.path.join(setting.project.target_repo, file_name)):
                logger.info(f"deleted content: {file_name}")
                continue
            elif os.path.getsize(os.path.join(setting.project.target_repo, file_name)) == 0:
                logger.info(f"blank content: {file_name}")
                continue

            recursive_file_path = file_name.split("/")
            pos = 0
            now_structure = target_meta_info.target_repo_hierarchical_tree
            while pos < len(recursive_file_path) - 1:
                if recursive_file_path[pos] not in now_structure.children.keys():
                    now_structure.children[recursive_file_path[pos]] = DocItem(
                        item_type=DocItemType._dir,
                        md_content="",
                        obj_name=recursive_file_path[pos],
                    )
                    now_structure.children[
                        recursive_file_path[pos]
                    ].father = now_structure
                now_structure = now_structure.children[recursive_file_path[pos]]
                pos += 1
            if recursive_file_path[-1] not in now_structure.children.keys():
                now_structure.children[recursive_file_path[pos]] = DocItem(
                    item_type=DocItemType._file,
                    obj_name=recursive_file_path[-1],
                )
                now_structure.children[recursive_file_path[pos]].father = now_structure

            # 然后parse file内容
            assert type(file_content) == list
            file_item = target_meta_info.target_repo_hierarchical_tree.find(recursive_file_path)
            assert file_item.item_type == DocItemType._file
            '''用类线段树的方式：
            1.先parse所有节点，再找父子关系
            2.一个节点的父节点，所有包含他的code范围的节点里的，最小的节点
            复杂度是O(n^2)
            3.最后来处理节点的type问题
            '''

            obj_item_list: List[DocItem] = []
            for value in file_content:
                obj_doc_item = DocItem(
                                        obj_name=value["name"],
                                        content = value,
                                        md_content=value["md_content"],
                                        code_start_line=value["code_start_line"],
                                        code_end_line=value["code_end_line"],
                                    )
                if "item_status" in value.keys():
                    obj_doc_item.item_status = DocItemStatus[value["item_status"]]
                if "reference_who" in value.keys():
                    obj_doc_item.reference_who_name_list = value["reference_who"]
                if "special_reference_type" in value.keys():
                    obj_doc_item.special_reference_type = value["special_reference_type"]
                if "who_reference_me" in value.keys():
                    obj_doc_item.who_reference_me_name_list = value["who_reference_me"]
                obj_item_list.append(obj_doc_item)

            #接下里寻找可能的父亲
            for item in obj_item_list:
                potential_father = None
                for other_item in obj_item_list:
                    def code_contain(item, other_item) -> bool:
                        if other_item.code_end_line == item.code_end_line and other_item.code_start_line == item.code_start_line:
                            return False
                        if other_item.code_end_line < item.code_end_line or other_item.code_start_line > item.code_start_line:
                            return False
                        return True
                    if code_contain(item, other_item):
                        if potential_father == None or ((other_item.code_end_line - other_item.code_start_line) < (potential_father.code_end_line - potential_father.code_start_line)):
                            potential_father = other_item
                
                if potential_father == None:
                    potential_father = file_item
                item.father = potential_father
                child_name = item.obj_name
                if child_name in potential_father.children.keys(): 
                    # 如果存在同层次的重名问题，就重命名成 xxx_i的形式
                    now_name_id = 0
                    while (child_name + f"_{now_name_id}") in potential_father.children.keys():
                        now_name_id += 1
                    child_name = child_name + f"_{now_name_id}"
                    logger.warning(f"Name duplicate in {file_item.get_full_name()}: rename to {item.obj_name}->{child_name}")
                potential_father.children[child_name] = item
                # print(f"{potential_father.get_full_name()} -> {item.get_full_name()}")
            
            def change_items(now_item: DocItem):
                if now_item.item_type != DocItemType._file:
                    if now_item.content["type"] == "ClassDef":
                        now_item.item_type = DocItemType._class
                    elif now_item.content["type"] == "FunctionDef":
                        now_item.item_type = DocItemType._function
                        if now_item.father.item_type == DocItemType._class:
                            now_item.item_type = DocItemType._class_function
                        elif now_item.father.item_type in [ DocItemType._function, DocItemType._sub_function]:
                            now_item.item_type = DocItemType._sub_function
                for _, child in now_item.children.items():
                    change_items(child)
            change_items(file_item)
           
            
        target_meta_info.target_repo_hierarchical_tree.parse_tree_path(now_path=[])
        target_meta_info.target_repo_hierarchical_tree.check_depth()
        return target_meta_info


if __name__ == "__main__":
    repo_path = "some_repo_path"
    meta = MetaInfo.from_project_hierarchy_json(repo_path)
    meta.target_repo_hierarchical_tree.print_recursive()
    topology_list = meta.get_topology()
