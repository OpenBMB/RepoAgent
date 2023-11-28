# FileHandler 类，实现对文件的读写操作，这里的文件包括markdown文件和python文件
import git
import os
import ast

# 这个类会在遍历变更后的文件的循环中，为每个变更后文件（也就是当前文件）创建一个实例
class FileHandler:
    def __init__(self, repo_path, file_path):
        self.file_path = file_path
        self.repo_path = repo_path
        # 当前文件的代码内容
        self.content = self.read_file()

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

    def get_obj_code(self, code_type, code_name, start_line, end_line):
        code_info = {}
        code_info['type'] = code_type
        code_info['name'] = code_name
        with open(os.path.join(self.repo_path, self.file_path), 'r') as code_file:
            lines = code_file.readlines()
            code_content = ''.join(lines[start_line-1:end_line])
            code_info['content'] = code_content
            # 判断代码中是否有return字样
            if 'return' in code_content:
                have_return = True
            else:  
                have_return = False
            
            code_info['have_return'] = have_return

                
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
        with open(file_path, 'a+') as file:
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

    def get_functions_and_classes(self,code_content):
            """
            Retrieves all functions and classes from the content of the file.
            输出示例：[('FunctionDef', 'PipelineEngine', 86, 95), ('ClassDef', 'AI_give_params', 97, 104)]

            Returns:
                A list of tuples containing the type of the node (FunctionDef, ClassDef, AsyncFunctionDef),
                the name of the node, the starting line number, and the ending line number.
            """
            tree = ast.parse(code_content)
            functions_and_classes = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    start_line = node.lineno
                    end_line = self.get_end_lineno(node)
                    functions_and_classes.append((type(node).__name__, node.name, start_line, end_line))
            return functions_and_classes
