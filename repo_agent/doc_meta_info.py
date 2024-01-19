"""存储doc对应的信息，同时处理引用的关系
"""
from __future__ import annotations
import threading
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
from colorama import Fore, Style
from enum import Enum, unique, auto
import time
import os
import json
from loguru import logger
import jedi
from tqdm import tqdm

from config import CONFIG
from file_handler import FileHandler
from multi_task_dispatch import TaskManager

@unique
class EdgeType(Enum):
    reference_edge = auto() #一个obj引用另一个obj
    subfile_edge = auto() # 一个 文件/文件夹 属于一个文件夹
    file_item_edge = auto() #一个 obj 属于一个文件


@unique
class DocItemType(Enum):
    _repo = auto() #根节点，需要生成readme
    _dir = auto()
    _file = auto()
    _class = auto()
    _class_function = auto()
    _function = auto() #文件内的常规function
    _sub_function = auto() #function内的定义的subfunction
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
            color = Fore.BLUE
        elif self == DocItemType._function:
            color = Fore.RED
        return color + self.name + Style.RESET_ALL

    def get_edge_type(from_item_type: DocItemType, to_item_type: DocItemType) -> EdgeType:
        pass

@unique
class DocItemStatus(Enum):
    doc_up_to_date = auto() #无需生成文档
    doc_has_not_been_generated = auto() #文档还未生成，需要生成
    code_changed = auto() #源码被修改了，需要改文档
    add_new_referencer = auto() #添加了新的引用者
    referencer_not_exist = auto() #曾经引用他的obj被删除了，或者不再引用他了


@dataclass
class DocItem():
    item_type: DocItemType = DocItemType._class_function
    item_status: DocItemStatus = DocItemStatus.doc_has_not_been_generated

    obj_name: str = "" #对象的名字
    md_content: List[str] = field(default_factory=list) #存储不同版本的doc
    content: Dict[Any,Any] = field(default_factory=dict) #原本存储的信息

    children: Dict[str, DocItem] = field(default_factory=dict) #子对象
    father: Any[DocItem] = None

    depth: int = 0
    tree_path: List[DocItem] = field(default_factory=list) #一整条链路，从root开始
    max_reference_ansce: Any[DocItem] = None

    reference_who: List[DocItem] = field(default_factory=list) #他引用了谁
    who_reference_me: List[DocItem] = field(default_factory=list) #谁引用了他

    reference_who_name_list: List[str] = field(default_factory=list) #他引用了谁，这个可能是老版本的
    who_reference_me_name_list: List[str] = field(default_factory=list) #谁引用了他，这个可能是老版本的

    multithread_task_id: int = -1 #在多线程中的task_id

    def __eq__(self, other) -> bool:
        # 检查other是否是MyCustomClass的实例
        if not isinstance(other, DocItem):
            return False
        if self.item_type != other.item_type:
            return False
        if self.obj_name != other.obj_name:
            return False
        return self.get_full_name() == other.get_full_name()


    @staticmethod
    def has_ans_relation(now_a: DocItem, now_b: DocItem):
        """node之间是否是祖先关系，有的话返回更早的节点"""
        if now_b in now_a.tree_path:
            return now_b
        if now_a in now_b.tree_path:
            return now_a
        return None
    
    def get_travel_list(self):
        now_list = [self]
        for _, child in self.children.items():
            now_list = now_list + child.get_travel_list()
        return now_list
    
    def check_depth(self):
        if len(self.children) == 0:
            self.depth = 0
            return self.depth
        max_child_depth = 0
        for _, child in self.children.items():
            child_depth = child.check_depth()
            max_child_depth = max(child_depth, max_child_depth)
        self.depth = max_child_depth + 1
        return self.depth


    
    @staticmethod
    def find_min_ances(node_a: DocItem, node_b: DocItem):
        pos = 0
        assert node_a.tree_path[pos] == node_b.tree_path[pos]
        while True:
            pos += 1
            if node_a.tree_path[pos] != node_b.tree_path[pos]:
                return node_a.tree_path[pos - 1]

    def parse_tree_path(self, now_path):
        self.tree_path = now_path + [self]
        for key, child in self.children.items():
            child.parse_tree_path(self.tree_path)

    def get_file_name(self):
        full_name = self.get_full_name()
        return full_name.split(".py")[0] + ".py"
    def get_full_name(self): 
        """获取从下到上所有的obj名字"""
        if self.father == None:
            return self.obj_name
        name_list = []
        now = self
        while now != None:
            name_list = [now.obj_name] + name_list
            now = now.father
        
        name_list = name_list[1:]
        return "/".join(name_list)
    
    
    def find(self, recursive_file_path: list) -> Optional[DocItem]:
        """从repo根节点根据path_list找到对应的文件, 否则返回False
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

    def print_recursive(self, indent=0, print_content = False):
        """递归打印repo对象
        """
        def print_indent(indent=0):
            if indent == 0:
                return ""
            return "  "*indent+"|-"
        print(print_indent(indent) + f"{self.item_type.print_self()}: {self.obj_name}",end="")
        if len(self.children) > 0 :
            print(f", {len(self.children)} children")
        else:
            print()
        for child_name, child in self.children.items():
            child.print_recursive(indent=indent+1, print_content=print_content)



def find_all_referencer(repo_path, variable_name, file_path, line_number, column_number, in_file_only=False):
    """复制过来的之前的实现"""
    script = jedi.Script(path=os.path.join(repo_path, file_path))

    try:
        if in_file_only:
            references = script.get_references(line=line_number, column=column_number, scope="file")
        else:
            references = script.get_references(line=line_number, column=column_number)
        # 过滤出变量名为 variable_name 的引用，并返回它们的位置
        variable_references = [ref for ref in references if ref.name == variable_name]
        return [(os.path.relpath(ref.module_path, repo_path), ref.line, ref.column) for ref in variable_references if not (ref.line == line_number and ref.column == column_number)]
    except Exception as e:
        # 打印错误信息和相关参数
        print(f"Error occurred: {e}")
        print(f"Parameters: variable_name={variable_name}, file_path={file_path}, line_number={line_number}, column_number={column_number}")
        return []


@dataclass
class MetaInfo():
    repo_path: str = ""
    document_version: str = "" #随时间变化，""代表没完成，否则对应一个目标仓库的commit hash
    target_repo_hierarchical_tree: DocItem = field(default_factory="Docitem") #整个repo的文件结构
    white_list: Any[List] = None

    in_generation_process: bool = False

    checkpoint_lock: threading.Lock = threading.Lock()

    @staticmethod
    def init_from_project_path(project_abs_path: str) -> MetaInfo:
        """从一个仓库path中初始化metainfo"""
        project_abs_path = CONFIG['repo_path']
        logger.info(f"initializing a new meta-info from {project_abs_path}")
        file_handler = FileHandler(project_abs_path, None)
        repo_structure = file_handler.generate_overall_structure()
        metainfo = MetaInfo.from_project_hierarchy_json(repo_structure)
        metainfo.repo_path = project_abs_path
        return metainfo
    
    @staticmethod
    def from_checkpoint_path(checkpoint_dir_path: str) -> MetaInfo:
        """从已有的metainfo dir里面读取metainfo
        """
        project_hierarchy_json_path = os.path.join(checkpoint_dir_path, ".project_hierarchy.json")
        
        with open(project_hierarchy_json_path,'r', encoding="utf-8") as reader:
            project_hierarchy_json = json.load(reader)
        metainfo = MetaInfo.from_project_hierarchy_json(project_hierarchy_json)        
        
        with open(os.path.join(checkpoint_dir_path, "meta-info.json"),'r', encoding="utf-8") as reader:
            meta_data = json.load(reader)
            metainfo.repo_path = meta_data["repo_path"]
            metainfo.document_version = meta_data["doc_version"]
            metainfo.in_generation_process = meta_data["in_generation_process"]

        logger.info(f"loading meta-info from {checkpoint_dir_path}, document-version=\"{metainfo.document_version}\"")
        return metainfo   

    def checkpoint(self, target_dir_path: str, flash_reference_relation=False):
        with self.checkpoint_lock:
            logger.info(f"will save MetaInfo at {target_dir_path}")
            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)
            now_hierarchy_json = self.to_hierarchy_json(flash_reference_relation=flash_reference_relation)
            with open(os.path.join(target_dir_path, ".project_hierarchy.json"), "w") as writer:
                json.dump(now_hierarchy_json, writer, indent=2, ensure_ascii=False)
            
            with open(os.path.join(target_dir_path, "meta-info.json"), "w") as writer:
                meta = {
                    "repo_path": self.repo_path,
                    "doc_version": self.document_version,
                    "in_generation_process": self.in_generation_process,
                }
                json.dump(meta, writer, indent=2, ensure_ascii=False)
    
    
    def print_task_list(self, item_list):
        from prettytable import PrettyTable
        task_table = PrettyTable(["task_id","Doc Generation Reason", "Path"])
        task_count = 0
        for k, item in enumerate(item_list):
            task_table.add_row([task_count, item.item_status.name, item.get_full_name()])
            task_count += 1
        print("Remain tasks to be done")
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


    def find_obj_with_lineno(self, file_node, start_line_num) -> DocItem:
        """每个DocItem._file，对于所有的行，建立他们对应的对象是谁"""
        now_node = file_node
        while len(now_node.children) > 0:
            find_qualify_child = False
            for _, child in now_node.children.items():
                assert child.content != None
                if child.content["code_start_line"] <= start_line_num:
                    now_node = child
                    find_qualify_child = True
                    break
            if not find_qualify_child: 
                return now_node
        return now_node

            

    def parse_reference(self):
        """双向提取所有引用关系
        """
        file_nodes = self.get_all_files()
        white_list_file_names = []
        obj_names = []
        if self.white_list != None:
            white_list_file_names = [cont["file_path"] for cont in self.white_list]
            white_list_file_names = [cont["id_text"] for cont in self.white_list]
        for file_node in tqdm(file_nodes, desc="parsing bidirectional reference"):
            ref_count = 0
            rel_file_path = file_node.get_full_name()
            if white_list_file_names != [] and (file_node.get_file_name() not in white_list_file_names): #如果有白名单，只parse白名单里的对象
                continue

            def walk_file(now_obj: DocItem):
                """在文件内遍历所有变量"""
                nonlocal ref_count
                in_file_only = False
                if white_list_file_names != [] and (now_obj.obj_name not in white_list_file_names):
                    in_file_only = True #作为加速，如果有白名单，白名单obj同文件夹下的也parse，但是只找同文件内的引用

                reference_list = find_all_referencer(
                    repo_path=self.repo_path,
                    variable_name=now_obj.obj_name,
                    file_path=rel_file_path,
                    line_number=now_obj.content["code_start_line"],
                    column_number=now_obj.content["name_column"],
                    in_file_only=True,
                )
                for referencer_pos in reference_list: #对于每个引用
                    referencer_file_ral_path = referencer_pos[0]
                    referencer_file_item = self.target_repo_hierarchical_tree.find(referencer_file_ral_path.split("/"))
                    referencer_node = self.find_obj_with_lineno(referencer_file_item, referencer_pos[1])
                    # if now_obj.get_full_name() == "experiment2_gpt4_pdb.py/main":
                    #     print(reference_list)
                    #     print(referencer_node.get_full_name())
                    if DocItem.has_ans_relation(now_obj, referencer_node) == None:
                        # 不考虑祖先节点之间的引用
                        # print(referencer_node.get_full_name())
                        if now_obj not in referencer_node.reference_who:
                            referencer_node.reference_who.append(now_obj)
                            now_obj.who_reference_me.append(referencer_node)

                            min_ances = DocItem.find_min_ances(referencer_node, now_obj)
                            if referencer_node.max_reference_ansce == None:
                                referencer_node.max_reference_ansce = min_ances
                            else: #是否更大
                                if min_ances in referencer_node.max_reference_ansce.tree_path:
                                    referencer_node.max_reference_ansce = min_ances

                            ref_count += 1
                # e = time.time()
                # print(f"遍历reference 用时: {e-s}")
                for _, child in now_obj.children.items():
                    walk_file(child)

            for _,child in file_node.children.items():
                walk_file(child)
            # logger.info(f"find {ref_count} refer-relation in {file_node.get_full_name()}")
    

    def get_task_manager(self, now_node: DocItem, task_available_func: Callable = None) -> TaskManager:
        """先写一个退化的版本，只考虑拓扑引用关系
        """
        doc_items = now_node.get_travel_list()
        if self.white_list != None:
            def in_white_list(item: DocItem):
                for cont in self.white_list:
                    if item.get_file_name() == cont["file_path"] and item.obj_name == cont["id_text"]:
                        return True
                return False
            doc_items = list(filter(in_white_list, doc_items))
        items_by_depth = sorted(doc_items, key=lambda x: x.depth)
        deal_items = []
        task_manager = TaskManager()
        bar = tqdm(total = len(items_by_depth),desc="sorting topology order")
        while items_by_depth:
            for item in items_by_depth:
                if all(referenced in deal_items for referenced in item.reference_who):
                    """一个任务依赖于所有引用者和他的子节点"""
                    item_denp_task_ids = []
                    for _, child in item.children.items():
                        if child.multithread_task_id in task_manager.task_dict.keys():
                            item_denp_task_ids.append(child.multithread_task_id)
                    for referenced_item in item.reference_who:
                        if referenced_item.multithread_task_id in task_manager.task_dict.keys():
                            item_denp_task_ids.append(referenced_item.multithread_task_id)
                    item_denp_task_ids = list(set(item_denp_task_ids)) #去重
                    if task_available_func == None or task_available_func(item):
                        task_id = task_manager.add_task(dependency_task_id=item_denp_task_ids,extra=item)
                        item.multithread_task_id = task_id
                    deal_items.append(item)
                    items_by_depth.remove(item)
                    bar.update(1)
                    break

                    # #将尾递归转化为while的形式来解决最大深度的问题
                    # while item.father is not None:
                    #     father_node = item.father
                    #     all_children_processed = True
                    #     for _, node in father_node.children.items():
                    #         if node not in sorted_items:
                    #             all_children_processed = False
                    #             break
                    #     if not all_children_processed:
                    #         break
                    #     sorted_items.append(father_node)
                    #     if father_node in items_by_depth:
                    #         items_by_depth.remove(father_node)
                    #     bar.update(1)
                    #     item = father_node  # 更新item为父节点，继续循环
                    # break

        # Further optimization for minimizing tree distance could be added here
        return task_manager

    def get_topology(self, task_available_func = None) -> TaskManager:
        """计算repo中所有对象的拓扑顺序
        """
        self.parse_reference()
        task_manager = self.get_task_manager(self.target_repo_hierarchical_tree,task_available_func=task_available_func)
        return task_manager
    
    def _map(self, deal_func: Callable):
        """将所有节点进行同一个操作"""
        def travel(now_item: DocItem):
            deal_func(now_item)
            for _, child in now_item.children.items():
                travel(child)
        travel(self.target_repo_hierarchical_tree)

    def load_doc_from_older_meta(self, older_meta: MetaInfo):
        """older_meta是老版本的、已经生成doc的meta info
        """
        logger.info("merge doc from an older version of metainfo")
        root_item = self.target_repo_hierarchical_tree
        def find_item(now_item: DocItem) -> Optional[DocItem]:
            """新版的meta中能不能找到原来的某个东西"""
            nonlocal root_item
            if now_item.father == None: #根节点永远能找到
                return root_item
            father_find_result = find_item(now_item.father)
            if not father_find_result:
                return None
            if now_item.obj_name in father_find_result.children.keys():
                return father_find_result.children[now_item.obj_name]
            return None


        def travel(now_older_item: DocItem): #只寻找源码是否被修改的信息
            result_item = find_item(now_older_item)
            if not result_item: #新版文件中找不到原来的item，就回退
                # print(f"return: {now_older_item.get_full_name()}")
                return
            result_item.md_content = now_older_item.md_content
            result_item.item_status = now_older_item.item_status
            # if result_item.obj_name == "run":
            #     import pdb; pdb.set_trace()
            if "code_content" in now_older_item.content.keys():
                assert "code_content" in result_item.content.keys()
                if now_older_item.content["code_content"] != result_item.content["code_content"]: #源码被修改了
                    result_item.item_status = DocItemStatus.code_changed

            for _, child in now_older_item.children.items():
                travel(child)
        travel(older_meta.target_repo_hierarchical_tree)

        """接下来，parse现在的双向引用，观察谁的引用者改了"""
        self.parse_reference() 

        def travel2(now_older_item: DocItem):
            result_item = find_item(now_older_item)
            if not result_item: #新版文件中找不到原来的item，就回退
                return
            """result_item引用的人是否变化了"""
            new_reference_names = [name.get_full_name() for name in result_item.who_reference_me]
            old_reference_names = now_older_item.who_reference_me_name_list

            if not (set(new_reference_names) == set(old_reference_names)) and (result_item.item_status == DocItemStatus.doc_up_to_date):
                if set(new_reference_names) <= set(old_reference_names): #旧的referencer包含新的referencer
                    result_item.item_status = DocItemStatus.referencer_not_exist
                else:
                    result_item.item_status = DocItemStatus.add_new_referencer
            for _, child in now_older_item.children.items():
                travel2(child)
        travel2(older_meta.target_repo_hierarchical_tree)


    @staticmethod
    def from_project_hierarchy_path(repo_path: str) -> MetaInfo:
        """project_hierarchy_json全是压平的文件，递归的文件目录都在最终的key里面, 把他转换到我们的数据结构
        """
        project_hierarchy_json_path = os.path.join(repo_path, ".project_hierarchy.json")
        logger.info(f"parsing from {project_hierarchy_json_path}")
        if not os.path.exists(project_hierarchy_json_path):
            raise NotImplementedError("怪")
        
        with open(project_hierarchy_json_path,'r', encoding="utf-8") as reader:
            project_hierarchy_json = json.load(reader)
        return MetaInfo.from_project_hierarchy_json(project_hierarchy_json)
    
    def to_hierarchy_json(self, flash_reference_relation = False):
        """
        如果flash_reference_relation=True,则会将最新的双向引用关系写回到meta文件中
        """
        hierachy_json = {}
        file_item_list = self.get_all_files()
        for file_item in file_item_list:
            file_hierarchy_content = {}
            
            def walk_file(now_obj: DocItem):
                nonlocal file_hierarchy_content, flash_reference_relation
                file_hierarchy_content[now_obj.obj_name] = now_obj.content
                file_hierarchy_content[now_obj.obj_name]["name"] = now_obj.obj_name
                file_hierarchy_content[now_obj.obj_name]["type"] = now_obj.item_type.to_str()
                file_hierarchy_content[now_obj.obj_name]["md_content"] = now_obj.md_content
                file_hierarchy_content[now_obj.obj_name]["item_status"] = now_obj.item_status.name
                
                if flash_reference_relation:
                    file_hierarchy_content[now_obj.obj_name]["who_reference_me"] = [cont.get_full_name() for cont in now_obj.who_reference_me]
                    file_hierarchy_content[now_obj.obj_name]["reference_who"] = [cont.get_full_name() for cont in now_obj.reference_who]

                file_hierarchy_content[now_obj.obj_name]["parent"] = None
                if now_obj.father.item_type != DocItemType._file:
                    file_hierarchy_content[now_obj.obj_name]["parent"] = now_obj.father.obj_name

                for _, child in now_obj.children.items():
                    walk_file(child)

            for _,child in file_item.children.items():
                walk_file(child)
            hierachy_json[file_item.get_full_name()] = file_hierarchy_content
        return hierachy_json

    @staticmethod
    def from_project_hierarchy_json(project_hierarchy_json) -> MetaInfo:
        target_meta_info = MetaInfo(
            # repo_path=repo_path,
            target_repo_hierarchical_tree=DocItem( #根节点
                
                item_type=DocItemType._repo,
                obj_name="full_repo",
            )
        )

        for file_name, file_content in project_hierarchy_json.items(): 
            # 首先parse file archi
            if not os.path.exists(os.path.join(CONFIG['repo_path'],file_name)):
                logger.info(f"deleted content: {file_name}")
                continue
            elif os.path.getsize(os.path.join(CONFIG['repo_path'],file_name)) == 0:
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
                    now_structure.children[recursive_file_path[pos]].father = now_structure
                now_structure = now_structure.children[recursive_file_path[pos]]
                pos += 1
            if recursive_file_path[-1] not in now_structure.children.keys():
                now_structure.children[recursive_file_path[pos]] = DocItem(
                    item_type=DocItemType._file,
                    obj_name=recursive_file_path[-1],
                )
                now_structure.children[recursive_file_path[pos]].father = now_structure 
        
            # 然后parse file内容
            assert type(file_content) == dict
            file_item = target_meta_info.target_repo_hierarchical_tree.find(recursive_file_path)
            assert file_item.item_type == DocItemType._file

            def parse_one_item(key, value, item_reflection):
                #递归parse，做过了就跳过，如果有father就先parse father
                # print(f"key: {key}")
                if key in item_reflection.keys():
                    return 
                if value["parent"] != None:
                    # print(f"will parse father {value['parent']}")
                    parse_one_item(value["parent"], file_content[value["parent"]], item_reflection)

                item_reflection[key] = DocItem(
                                        obj_name=key,
                                        content = value,
                                        md_content=value["md_content"],
                                    )
                if "item_status" in value.keys():
                    item_reflection[key].item_status = DocItemStatus[value["item_status"]]
                if "reference_who" in value.keys():
                    item_reflection[key].reference_who_name_list = value["reference_who"]
                if "who_reference_me" in value.keys():
                    item_reflection[key].who_reference_me_name_list = value["who_reference_me"]
                if value["parent"] != None:
                    item_reflection[value["parent"]].children[key] = item_reflection[key]
                    item_reflection[key].father = item_reflection[value["parent"]]
                else:
                    file_item.children[key] = item_reflection[key]
                    item_reflection[key].father = file_item

                if value["type"] == "ClassDef":
                    item_reflection[key].item_type = DocItemType._class
                elif value["type"] == "FunctionDef":
                    item_reflection[key].item_type = DocItemType._function
                    if value["parent"] != None:
                        parent_value = file_content[value["parent"]]
                        if parent_value["type"] == "FunctionDef":
                            item_reflection[key].item_type = DocItemType._sub_function
                        elif parent_value["type"] == "ClassDef":
                            item_reflection[key].item_type = DocItemType._class_function


            item_reflection = {}
            for key, value in file_content.items():
                parse_one_item(key, value, item_reflection)
            
        target_meta_info.target_repo_hierarchical_tree.parse_tree_path(now_path=[])
        target_meta_info.target_repo_hierarchical_tree.check_depth()
        return target_meta_info

if __name__ == "__main__":
    repo_path = "/Users/yeyn/data/git_repos/AutoPDB/"
    meta = MetaInfo.from_project_hierarchy_json(repo_path)
    meta.target_repo_hierarchical_tree.print_recursive()
    topology_list = meta.get_topology()