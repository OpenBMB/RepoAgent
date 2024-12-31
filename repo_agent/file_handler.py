# FileHandler 类，实现对文件的读写操作，这里的文件包括markdown文件和python文件
# repo_agent/file_handler.py
import ast
import json
import os
from importlib import resources

import git
from colorama import Fore, Style
from tqdm import tqdm
from tree_sitter_languages import get_parser

from repo_agent.log import logger
from repo_agent.settings import SettingsManager
from repo_agent.utils.gitignore_checker import GitignoreChecker
from repo_agent.utils.meta_info_utils import latest_verison_substring


def get_scm_fname(lang):
    try:
        return resources.files(__package__).joinpath("queries", f"ts-{lang}-tags.scm")
    except KeyError:
        return

class FileHandler:
    """
    历变更后的文件的循环中，为每个变更后文件（也就是当前文件）创建一个实例
    """

    def __init__(self, repo_path, file_path):
        self.file_path = file_path  # 这里的file_path是相对于仓库根目录的路径
        self.repo_path = repo_path

        setting = SettingsManager.get_setting()

        self.project_hierarchy = (
            setting.project.target_repo / setting.project.hierarchy_name
        )

        self.language = "python"
        self.ts_parser = None

    def read_file(self):
        """
        Read the file content

        Returns:
            str: The content of the current changed file
        """
        abs_file_path = os.path.join(self.repo_path, self.file_path)

        with open(abs_file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    

    def get_obj_code_info(
        self, code_type, code_name, start_line, end_line, params, file_path=None
    ):
        """
        Get the code information for a given object.

        Args:
            code_type (str): The type of the code.
            code_name (str): The name of the code.
            start_line (int): The starting line number of the code.
            end_line (int): The ending line number of the code.
            parent (str): The parent of the code.
            file_path (str, optional): The file path. Defaults to None.

        Returns:
            dict: A dictionary containing the code information.
        """

        code_info = {}
        code_info["type"] = code_type
        code_info["name"] = code_name
        code_info["md_content"] = []
        code_info["code_start_line"] = start_line
        code_info["code_end_line"] = end_line
        code_info["params"] = params

        with open(
            os.path.join(
                self.repo_path, file_path if file_path != None else self.file_path
            ),
            "r",
            encoding="utf-8",
        ) as code_file:
            lines = code_file.readlines()
            code_content = "".join(lines[start_line - 1 : end_line])
            # 获取对象名称在第一行代码中的位置
            name_column = lines[start_line - 1].find(code_name)
            # 判断代码中是否有return字样
            if "return" in code_content:
                have_return = True
            else:
                have_return = False

            code_info["have_return"] = have_return
            # # 使用 json.dumps 来转义字符串，并去掉首尾的引号
            # code_info['code_content'] = json.dumps(code_content)[1:-1]
            code_info["code_content"] = code_content
            code_info["name_column"] = name_column

        return code_info

    def write_file(self, file_path, content):
        """
        Write content to a file.

        Args:
            file_path (str): The relative path of the file.
            content (str): The content to be written to the file.
        """
        # 确保file_path是相对路径
        if file_path.startswith("/"):
            # 移除开头的 '/'
            file_path = file_path[1:]

        abs_file_path = os.path.join(self.repo_path, file_path)
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def get_modified_file_versions(self):
        """
        Get the current and previous versions of the modified file.

        Returns:
            tuple: A tuple containing the current version and the previous version of the file.
        """
        repo = git.Repo(self.repo_path)

        # Read the file in the current working directory (current version)
        current_version_path = os.path.join(self.repo_path, self.file_path)
        with open(current_version_path, "r", encoding="utf-8") as file:
            current_version = file.read()

        # Get the file version from the last commit (previous version)
        commits = list(repo.iter_commits(paths=self.file_path, max_count=1))
        previous_version = None
        if commits:
            commit = commits[0]
            try:
                previous_version = (
                    (commit.tree / self.file_path).data_stream.read().decode("utf-8")
                )
            except KeyError:
                previous_version = None  # The file may be newly added and not present in previous commits

        return current_version, previous_version

    def get_end_lineno(self, node):
        """
        Get the end line number of a given node.

        Args:
            node: The node for which to find the end line number.

        Returns:
            int: The end line number of the node. Returns -1 if the node does not have a line number.
        """
        if not hasattr(node, "lineno"):
            return -1  # 返回-1表示此节点没有行号

        end_lineno = node.lineno
        for child in ast.iter_child_nodes(node):
            child_end = getattr(child, "end_lineno", None) or self.get_end_lineno(child)
            if child_end > -1:  # 只更新当子节点有有效行号时
                end_lineno = max(end_lineno, child_end)
        return end_lineno

    def add_parent_references(self, node, parent=None):
        """
        Adds a parent reference to each node in the AST.

        Args:
            node: The current node in the AST.

        Returns:
            None
        """
        for child in ast.iter_child_nodes(node):
            child.parent = node
            self.add_parent_references(child, node)

    def get_functions_and_classes(self, code_content):
        ts_parser = get_parser(self.language)
        ts_tree = ts_parser.parse(bytes(code_content, "utf-8"))
        return self._extract_class_info_recursive(ts_tree.root_node)
    
    def _extract_class_info_recursive(self, node):
        """
        Recursively extracts class and function information from a tree-sitter node.

        Args:
            node (tree_sitter.Node): The tree-sitter AST node to analyze

        Returns:
            list[tuple]: A list of tuples containing:
                - str: Type of definition ('ClassDef' or 'FunctionDef')
                - str: Name of the class or function
                - int: Start line number
                - int: End line number 
                - list[str]: List of parameter names for functions, empty list for classes
        """
        results = []
        
        # Check current node
        if node.type == "class_definition":
            class_name = None
            for child in node.named_children:
                if child.type == "identifier":
                    class_name = str(child.text, encoding="utf-8")
                    break
                    
            if class_name:
                results.append((
                    "ClassDef",
                    class_name,
                    node.start_point[0] + 1,
                    node.end_point[0] + 1,
                    []
                )) 
        elif node.type == "function_definition":
            func_name = None
            parameters = []
            
            for child in node.named_children:
                if child.type == "identifier":
                    func_name = str(child.text, encoding="utf-8")
                elif child.type == "parameters":
                    # Extract parameter names from the parameters node
                    for param in child.named_children:
                        if param.type == "identifier":
                            parameters.append(str(param.text, encoding="utf-8"))
                            
            if func_name:
                results.append((
                    "FunctionDef", 
                    func_name,
                    node.start_point[0] + 1,
                    node.end_point[0] + 1, 
                    parameters
                ))
        
        # Recursively check all children
        for child in node.named_children:
            child_results = self._extract_class_info_recursive(child)
            results.extend(child_results)
            
        return results

    def generate_file_structure(self, file_path):
        """
        Generates the file structure for the given file path.

        Args:
            file_path (str): The relative path of the file.

        Returns:
            dict: A dictionary containing the file path and the generated file structure.

        Output example:
        {
            "function_name": {
                "type": "function",
                "start_line": 10,
                ··· ···
                "end_line": 20,
                "parent": "class_name"
            },
            "class_name": {
                "type": "class",
                "start_line": 5,
                ··· ···
                "end_line": 25,
                "parent": None
            }
        }
        """
        with open(os.path.join(self.repo_path, file_path), "r", encoding="utf-8") as f:
            content = f.read()
            structures = self.get_functions_and_classes(content)
            file_objects = []  # 以列表的形式存储
            for struct in structures:
                structure_type, name, start_line, end_line, params = struct
                code_info = self.get_obj_code_info(
                    structure_type, name, start_line, end_line, params, file_path
                )
                file_objects.append(code_info)

        return file_objects

    def generate_overall_structure(self, file_path_reflections, jump_files) -> dict:
        """获取目标仓库的文件情况，通过AST-walk获取所有对象等情况。
        对于jump_files: 不会parse，当做不存在
        """
        repo_structure = {}
        gitignore_checker = GitignoreChecker(
            directory=self.repo_path,
            gitignore_path=os.path.join(self.repo_path, ".gitignore"),
        )

        bar = tqdm(gitignore_checker.check_files_and_folders())
        for not_ignored_files in bar:
            normal_file_names = not_ignored_files
            if not_ignored_files in jump_files:
                print(
                    f"{Fore.LIGHTYELLOW_EX}[File-Handler] Unstaged AddFile, ignore this file: {Style.RESET_ALL}{normal_file_names}"
                )
                continue
            elif not_ignored_files.endswith(latest_verison_substring):
                print(
                    f"{Fore.LIGHTYELLOW_EX}[File-Handler] Skip Latest Version, Using Git-Status Version]: {Style.RESET_ALL}{normal_file_names}"
                )
                continue
            # elif not_ignored_files.endswith(latest_version):
            #     """如果某文件被删除但没有暂存，文件系统有fake_file但没有对应的原始文件"""
            #     for k,v in file_path_reflections.items():
            #         if v == not_ignored_files and not os.path.exists(os.path.join(setting.project.target_repo, not_ignored_files)):
            #             print(f"{Fore.LIGHTYELLOW_EX}[Unstaged DeleteFile] load fake-file-content: {Style.RESET_ALL}{k}")
            #             normal_file_names = k #原来的名字
            #             break
            #     if normal_file_names == not_ignored_files:
            #         continue

            # if not_ignored_files in file_path_reflections.keys():
            #     not_ignored_files = file_path_reflections[not_ignored_files] #获取fake_file_path
            #     print(f"{Fore.LIGHTYELLOW_EX}[Unstaged ChangeFile] load fake-file-content: {Style.RESET_ALL}{normal_file_names}")

            try:
                repo_structure[normal_file_names] = self.generate_file_structure(
                    not_ignored_files
                )
            except Exception as e:
                logger.error(
                    f"Alert: An error occurred while generating file structure for {not_ignored_files}: {e}"
                )
                continue
            bar.set_description(f"generating repo structure: {not_ignored_files}")
        return repo_structure

    def convert_to_markdown_file(self, file_path=None):
        """
        Converts the content of a file to markdown format.

        Args:
            file_path (str, optional): The relative path of the file to be converted. If not provided, the default file path, which is None, will be used.

        Returns:
            str: The content of the file in markdown format.

        Raises:
            ValueError: If no file object is found for the specified file path in project_hierarchy.json.
        """
        with open(self.project_hierarchy, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if file_path is None:
            file_path = self.file_path

        # Find the file object in json_data that matches file_path

        file_dict = json_data.get(file_path)

        if file_dict is None:
            raise ValueError(
                f"No file object found for {self.file_path} in project_hierarchy.json"
            )

        markdown = ""
        parent_dict = {}
        objects = sorted(file_dict.values(), key=lambda obj: obj["code_start_line"])
        for obj in objects:
            if obj["parent"] is not None:
                parent_dict[obj["name"]] = obj["parent"]
        current_parent = None
        for obj in objects:
            level = 1
            parent = obj["parent"]
            while parent is not None:
                level += 1
                parent = parent_dict.get(parent)
            if level == 1 and current_parent is not None:
                markdown += "***\n"
            current_parent = obj["name"]
            params_str = ""
            if obj["type"] in ["FunctionDef", "AsyncFunctionDef"]:
                params_str = "()"
                if obj["params"]:
                    params_str = f"({', '.join(obj['params'])})"
            markdown += f"{'#' * level} {obj['type']} {obj['name']}{params_str}:\n"
            markdown += (
                f"{obj['md_content'][-1] if len(obj['md_content']) >0 else ''}\n"
            )
        markdown += "***\n"

        return markdown
