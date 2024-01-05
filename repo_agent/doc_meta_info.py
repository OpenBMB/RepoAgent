"""存储doc对应的信息，同时处理引用的关系
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from colorama import Fore, Style
from enum import Enum, unique, auto
import os
import json
from loguru import logger
import jedi

from config import CONFIG


@unique
class EdgeType(Enum):
    reference_edge = auto() #一个obj引用另一个obj
    subfile_edge = auto() # 一个 文件/文件夹 属于一个文件夹
    file_item_edge = auto() #一个 obj 属于一个文件

@unique
class SubTreeAvailable(Enum):
    uncheck = auto()
    unavailable = auto()
    available = auto() #符合算法要求

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


@dataclass
class DocItem():
    item_type: DocItemType = DocItemType._class_function
    available_type: SubTreeAvailable = SubTreeAvailable.uncheck
    obj_name: str = ""

    document: str = ""

    content: Dict[Any,Any] = field(default_factory=dict) #原本存储的信息

    depth: int = 0

    children: Dict[str, DocItem] = field(default_factory=dict) #他引用了谁
    father: Any[DocItem] = None
    tree_path: List[DocItem] = field(default_factory=list) #一整条链路，从root开始

    max_reference_ansce: Any[DocItem] = None


    reference_who: List[DocItem] = field(default_factory=list) #他引用了谁
    who_reference_me: List[DocItem] = field(default_factory=list) #谁引用了他

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
    
    
    def find(self, recursive_file_path: list) -> DocItem:
        """从repo根节点根据path_list找到对应的文件
        """
        assert self.item_type == DocItemType._repo
        pos = 0
        now = self
        while pos < len(recursive_file_path):
            assert recursive_file_path[pos] in now.children.keys()
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



def find_all_referencer(repo_path, variable_name, file_path, line_number, column_number):
    """复制过来的之前的实现"""
    script = jedi.Script(path=os.path.join(repo_path, file_path))
    references = script.get_references(line=line_number, column=column_number)

    try:
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
    target_repo_hierarchical_tree: DocItem = field(default_factory="Docitem") #整个repo的文件结构

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


    def find_obj_with_lineno(self, file_node, start_line_num, end_line_num) -> DocItem:
        """每个DocItem._file，对于所有的行，建立他们对应的对象是谁"""
        now_node = file_node
        while len(now_node.children) > 0:
            find_qualify_child = False
            for _, child in now_node.children.items():
                assert child.content != None
                if child.content["code_start_line"] <= start_line_num and child.content["code_end_line"] >= end_line_num:
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
        for file_node in file_nodes:
            ref_count = 0
            rel_file_path = file_node.get_full_name()

            def walk_file(now_obj: DocItem):
                """在文件内遍历所有变量"""
                nonlocal ref_count
                reference_list = find_all_referencer(
                    repo_path=self.repo_path,
                    variable_name=now_obj.obj_name,
                    file_path=rel_file_path,
                    line_number=now_obj.content["code_start_line"],
                    column_number=now_obj.content["name_column"]
                )
                for referencer_pos in reference_list:
                    referencer_node = self.find_obj_with_lineno(file_node, referencer_pos[1],referencer_pos[2])
                    
                    if DocItem.has_ans_relation(now_obj, referencer_node) == None:
                        # 不考虑祖先节点之间的引用
                        referencer_node.reference_who.append(now_obj)
                        now_obj.who_reference_me.append(referencer_node)

                        min_ances = DocItem.find_min_ances(referencer_node, now_obj)
                        if referencer_node.max_reference_ansce == None:
                            referencer_node.max_reference_ansce = min_ances
                        else: #是否更大
                            if min_ances in referencer_node.max_reference_ansce.tree_path:
                                referencer_node.max_reference_ansce = min_ances

                        ref_count += 1

                for _, child in now_obj.children.items():
                    walk_file(child)

            for _,child in file_node.children.items():
                walk_file(child)
            logger.info(f"find {ref_count} refer-relation in {file_node.get_full_name()}")
    

    def get_subtree_list(self, now_node: DocItem) -> List[Any]:
        # def check_node_available(now_node: DocItem):
        #     """一个节点能形成subtree，需要里面所有的引用关系对应的最小公共祖先都在子树内
        #     """
        #     if len(now_node.children) == 0:
        #         now_node.available_type = SubTreeAvailable.available
        #         return
        #     for key, child in now_node.children.items():
        #         if child.available_type == SubTreeAvailable.uncheck:
        #             check_node_available(child)
        """先写一个退化的版本，只考虑拓扑引用关系
        """
        doc_items = now_node.get_travel_list()
        items_by_depth = sorted(doc_items, key=lambda x: x.depth)
        sorted_items = []
        while items_by_depth:
            for item in items_by_depth:
                if all(referenced in sorted_items for referenced in item.reference_who):
                    sorted_items.append(item)
                    items_by_depth.remove(item)

                    def check_father(item):
                        nonlocal sorted_items
                        nonlocal items_by_depth
                        if item.father == None:
                            return
                        father_node = item.father
                        for _,node in father_node.children.items():
                            if node not in sorted_items:
                                return
                        #所有儿子都进去了，父亲也可以进去，并且应该挨着
                        sorted_items.append(father_node)
                        items_by_depth.remove(father_node)
                        check_father(father_node)

                    check_father(item)
                    break

        # Further optimization for minimizing tree distance could be added here
        return sorted_items

    def get_topology(self) -> List[DocItem]:
        """计算repo中所有对象的拓扑顺序
        """
        self.parse_reference()
        topology_list = self.get_subtree_list(self.target_repo_hierarchical_tree)
        return topology_list


    @staticmethod
    def from_project_hierarchy_json(repo_path: str):
        """project_hierarchy_json全是压平的文件，递归的文件目录都在最终的key里面, 把他转换到我们的数据结构
        """
        project_hierarchy_json_path = os.path.join(repo_path, ".project_hierarchy.json")
        logger.info(f"parsing from {project_hierarchy_json_path}")
        if not os.path.exists(project_hierarchy_json_path):
            raise NotImplementedError("怪")
        
        with open(project_hierarchy_json_path,'r', encoding="utf-8") as reader:
            project_hierarchy_json = json.load(reader)
        
        target_meta_info = MetaInfo(
            repo_path=repo_path,
            target_repo_hierarchical_tree=DocItem( #根节点
                
                item_type=DocItemType._repo,
                obj_name="full_repo",
            )
        )

        for file_name, file_content in project_hierarchy_json.items(): 
            # 首先parse file archi
            if os.path.getsize(os.path.join(CONFIG['repo_path'],file_name)) == 0:
                logger.info(f"skip {file_name}, blank")
                continue

            recursive_file_path = file_name.split("/")
            pos = 0
            now_structure = target_meta_info.target_repo_hierarchical_tree
            while pos < len(recursive_file_path) - 1:
                if recursive_file_path[pos] not in now_structure.children.keys():
                    now_structure.children[recursive_file_path[pos]] = DocItem(
                        item_type=DocItemType._dir,
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
                                    )
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