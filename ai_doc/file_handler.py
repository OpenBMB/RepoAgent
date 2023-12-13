# FileHandler 类，实现对文件的读写操作，这里的文件包括markdown文件和python文件
import git
import os,json
import ast
from config import CONFIG


# 这个类会在遍历变更后的文件的循环中，为每个变更后文件（也就是当前文件）创建一个实例
class FileHandler:
    def __init__(self, repo_path, file_path):
        self.file_path = file_path # 这里的file_path是相对于仓库根目录的路径
        self.repo_path = repo_path
        self.project_hierachy = os.path.join(repo_path, CONFIG['project_hierachy'])

    def read_file(self):
        """
        读取文件内容

        Returns:
            str: 当前变更文件的文件内容
        """
        file_path = os.path.join(self.repo_path, self.file_path)
        with open(file_path, 'r') as file:
            content = file.read()
        return content

    def get_obj_code_info(self, code_type, code_name, start_line, end_line, parent, file_path = None):

        code_info = {}
        code_info['type'] = code_type
        code_info['name'] = code_name
        code_info['md_content'] = ""
        code_info['code_start_line'] = start_line
        code_info['code_end_line'] = end_line
        code_info['parent'] = parent

        with open(os.path.join(self.repo_path, file_path if file_path != None else self.file_path), 'r') as code_file:
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
            code_info['code_content'] = code_content
            code_info['name_column'] = name_column
                
        return code_info

    def write_file(self, file_path, content):
        """
        写入文件内容

        Args:
            repo_path (str): 仓库路径
            file_path (str): 文件路径
            content (str): 文件内容
        """
        file_path = os.path.join(self.repo_path, file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)


    def get_modified_file_versions(self):
        """
        获取文件的修改前后的版本

        Returns:
            tuple: 包含两个字符串，分别是修改后的完整代码和修改前的完整代码.注意，如果是新添加的文件，则返回的修改前的版本为None
        """
        repo = git.Repo(self.repo_path)

        # 读取当前工作目录中的文件（修改后的版本）
        current_version_path = os.path.join(self.repo_path, self.file_path)
        with open(current_version_path, 'r') as file:
            current_version = file.read()

        # 获取最后一次提交中的文件版本（修改前的版本）
        commits = list(repo.iter_commits(paths=self.file_path, max_count=1))
        previous_version = None
        if commits:
            commit = commits[0]
            try:
                previous_version = (commit.tree / self.file_path).data_stream.read().decode('utf-8')
            except KeyError:
                previous_version = None  # 文件可能是新添加的，之前的提交中不存在

        return current_version, previous_version
        
    def get_end_lineno(self,node):
        """ 获取AST节点的结束行号

        Args:
            node: AST节点

        Returns:
            int: AST节点的结束行号，如果节点没有行号则返回-1
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
        为AST中的每个节点添加父级引用。

        Args:
            node: AST节点
            parent: 父级节点
        """
        for child in ast.iter_child_nodes(node):
            child.parent = node
            self.add_parent_references(child, node)
    

    def get_functions_and_classes(self, code_content):
        """
        Retrieves all functions, classes, and their hierarchical relationships.
        输出示例：[('FunctionDef', 'AI_give_params', 86, 95, None), ('ClassDef', 'PipelineEngine', 97, 104, None), ('FunctionDef', 'get_all_pys', 99, 104, 'PipelineEngine')]
        在上述示例中，PipelineEngine是get_all_pys的父级结构。

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
                file_path (str): The path of the file.

            Returns:
                dict: A dictionary containing the file path and the generated file structure.
            """
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                structures = self.get_functions_and_classes(content)
                json_objects = []
                for struct in structures:
                    structure_type, name, start_line, end_line, parent = struct
                    code_info = self.get_obj_code_info(structure_type, name, start_line, end_line, parent, file_path)

                    json_objects.append(code_info)
            return {
                "file_path": file_path,
                "objects": json_objects
            }

    def generate_overall_structure(self):
        file_structure = []
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    absolute_file_path = os.path.join(root, file)
                    file_structure.append(self.generate_file_structure(absolute_file_path))
        return file_structure
    
    def convert_structure_to_json(self, file_structure):
        json_data = {"files": []}
        for file_data in file_structure:
            json_data["files"].append(file_data)
        return json_data

    def convert_to_markdown_file(self, file_path = None):
        with open(self.project_hierachy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if file_path == None:   
            file_path = os.path.join(self.repo_path, self.file_path)

        # Find the file object in json_data that matches file_path
        file_object = next((file for file in json_data["files"] if file["file_path"] == file_path), None)
        
        if file_object is None:
            raise ValueError(f"No file object found for {self.file_path} in project_hierachy.json")

        markdown = ""
        parent_dict = {}
        objects = sorted(file_object["objects"], key=lambda obj: obj["code_start_line"])
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
        with open(self.project_hierachy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # 检查根目录是否存在Markdown_docs文件夹，如果不存在则创建
        markdown_docs_path = os.path.join(self.repo_path, CONFIG['Markdown_Docs_folder'])
        if not os.path.exists(markdown_docs_path):
            os.mkdir(markdown_docs_path)

        # 遍历json_data["files"]列表中的每个字典
        for file in json_data["files"]:
            md_path = file["file_path"].replace(self.repo_path, markdown_docs_path).replace('.py', '.md')
            markdown = self.convert_to_markdown_file(file["file_path"])
            
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
