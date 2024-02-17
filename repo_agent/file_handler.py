# FileHandler 类，实现对文件的读写操作，这里的文件包括markdown文件和python文件
# repo_agent/file_handler.py
import git
import os,json
import ast
from config import CONFIG
from utils.gitignore_checker import GitignoreChecker

# 这个类会在遍历变更后的文件的循环中，为每个变更后文件（也就是当前文件）创建一个实例
class FileHandler:
    def __init__(self, repo_path, file_path):
        self.file_path = file_path # 这里的file_path是相对于仓库根目录的路径
        self.repo_path = repo_path
        self.project_hierarchy = os.path.join(repo_path, CONFIG['project_hierarchy'])

    def read_file(self):
        """
        Read the file content

        Returns:
            str: The content of the current changed file
        """
        abs_file_path = os.path.join(self.repo_path, self.file_path)
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def get_obj_code_info(self, code_type, code_name, start_line, end_line, parent, file_path = None):
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
        code_info['type'] = code_type
        code_info['name'] = code_name
        code_info['md_content'] = ""
        code_info['code_start_line'] = start_line
        code_info['code_end_line'] = end_line
        code_info['parent'] = parent

        with open(os.path.join(self.repo_path, file_path if file_path != None else self.file_path), 'r', encoding='utf-8') as code_file:
            lines = code_file.readlines()
            code_content = ''.join(lines[start_line-1:end_line])
            # 获取对象名称在第一行代码中的位置
            name_column = lines[start_line-1].find(code_name)
            # 判断代码中是否有return字样
            if 'return' in code_content:
                have_return = True
            else:  
                have_return = False
            
            code_info['have_return'] = have_return
            # # 使用 json.dumps 来转义字符串，并去掉首尾的引号
            # code_info['code_content'] = json.dumps(code_content)[1:-1]
            code_info['code_content'] = code_content
            code_info['name_column'] = name_column
                
        return code_info

    def write_file(self, file_path, content):
        """
        Write content to a file.

        Args:
            file_path (str): The relative path of the file.
            content (str): The content to be written to the file.
        """
        # 确保file_path是相对路径
        if file_path.startswith('/'):
            # 移除开头的 '/'
            file_path = file_path[1:]
            
        abs_file_path = os.path.join(self.repo_path, file_path)
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, 'w', encoding='utf-8') as file:
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
        with open(current_version_path, 'r', encoding='utf-8') as file:
            current_version = file.read()

        # Get the file version from the last commit (previous version)
        commits = list(repo.iter_commits(paths=self.file_path, max_count=1))
        previous_version = None
        if commits:
            commit = commits[0]
            try:
                previous_version = (commit.tree / self.file_path).data_stream.read().decode('utf-8')
            except KeyError:
                previous_version = None  # The file may be newly added and not present in previous commits

        return current_version, previous_version
        
    def get_end_lineno(self,node):
        """
        Get the end line number of a given node.

        Args:
            node: The node for which to find the end line number.

        Returns:
            int: The end line number of the node. Returns -1 if the node does not have a line number.
        """
        if not hasattr(node, 'lineno'):
            return -1  # 返回-1表示此节点没有行号

        end_lineno = node.lineno
        for child in ast.iter_child_nodes(node):
            child_end = getattr(child, 'end_lineno', None) or self.get_end_lineno(child)
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
        """
        Retrieves all functions, classes, and their hierarchical relationships.
        Output Examples: [('FunctionDef', 'AI_give_params', 86, 95, None), ('ClassDef', 'PipelineEngine', 97, 104, None), ('FunctionDef', 'get_all_pys', 99, 104, 'PipelineEngine')]
        On the example above, PipelineEngine is the Father structure for get_all_pys.

        Args:
            code_content: The code content of the whole file to be parsed.

        Returns:
            A list of tuples containing the type of the node (FunctionDef, ClassDef, AsyncFunctionDef),
            the name of the node, the starting line number, the ending line number, and the name of the parent node.
        """
        tree = ast.parse(code_content)
        self.add_parent_references(tree)
        functions_and_classes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno
                end_line = self.get_end_lineno(node)
                parent_name = node.parent.name if 'name' in dir(node.parent) else None
                functions_and_classes.append(
                    (type(node).__name__, node.name, start_line, end_line, parent_name)
                )
        return functions_and_classes
        
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
        with open(os.path.join(self.repo_path,file_path), 'r', encoding='utf-8') as f:
            content = f.read()
            structures = self.get_functions_and_classes(content)
            file_objects = {}
            for struct in structures:
                structure_type, name, start_line, end_line, parent = struct
                code_info = self.get_obj_code_info(structure_type, name, start_line, end_line, parent, file_path)
                file_objects[name] = code_info

        return file_objects
    

    def generate_overall_structure(self) -> dict:
        """
        Generate the overall structure of the repository.

        Returns:
            dict: A dictionary representing the structure of the repository.
        """
        repo_structure = {}
        gitignore_checker = GitignoreChecker(directory=self.repo_path,
                                            gitignore_path=os.path.join(self.repo_path, '.gitignore'))
        for not_ignored_files in gitignore_checker.check_files_and_folders():
            try:
                repo_structure[not_ignored_files] = self.generate_file_structure(not_ignored_files)
            except Exception as e:
                print(f"Alert: An error occurred while generating file structure for {not_ignored_files}: {e}")
                continue
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
        with open(self.project_hierarchy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if file_path is None:
            file_path = self.file_path

        # Find the file object in json_data that matches file_path
        file_dict = json_data.get(file_path)

        if file_dict is None:
            raise ValueError(f"No file object found for {self.file_path} in project_hierarchy.json")

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
            markdown += f"{'#' * level} {obj['type']} {obj['name']}\n"
            markdown += f"{obj['md_content']}\n"
        markdown += "***\n"

        return markdown

    def convert_all_to_markdown_files_from_json(self):
        """
        Converts all files to markdown format based on the JSON data.

        Reads the project hierarchy from a JSON file, checks if the Markdown_docs folder exists,
        creates it if it doesn't, and then iterates through each file in the JSON data.
        For each file, it converts the file to markdown format and writes it to the Markdown_docs folder.

        Args:
            self (object): The file_handler object.

        Returns:
            None
        """
        with open(self.project_hierarchy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # 检查根目录是否存在Markdown_docs文件夹，如果不存在则创建
        markdown_docs_path = os.path.join(self.repo_path, CONFIG['Markdown_Docs_folder'])
        if not os.path.exists(markdown_docs_path):
            os.mkdir(markdown_docs_path)

        # 遍历json_data["files"]列表中的每个字典
        for rel_file_path, file_dict in json_data.items():
            md_path = os.path.join(markdown_docs_path, rel_file_path.replace('.py', '.md'))
            markdown = self.convert_to_markdown_file(rel_file_path)
            
            # 检查目录是否存在，如果不存在，就创建它
            os.makedirs(os.path.dirname(md_path), exist_ok=True)

            # 将markdown文档写入到Markdown_docs文件夹中
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
    

if __name__ == "__main__":

    # 打开py文件读取源代码
    # file_handler = FileHandler('/path/to/repo', '/path/to/file.py')

    file_handler = FileHandler(CONFIG['repo_path'], 'XAgent/engines/pipeline_old.py')
    # file_handler.generate_markdown_from_json()
    file_handler.convert_all_to_markdown_files_from_json()
    # code_content = file_handler.read_file()
    # functions_and_classes = file_handler.get_functions_and_classes(code_content)
    # print(functions_and_classes)
