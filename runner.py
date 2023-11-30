import os
from file_handler import FileHandler
from change_detector import ChangeDetector
from project_manager import ProjectManager
from chat_engine import ChatEngine
from concurrent.futures import ThreadPoolExecutor, as_completed
from relationships import get_func_relationships
import inspect
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Runner:
    def __init__(self,config_file,repo_path):
        self.project_manager = ProjectManager() # TODO: repo_path参数传参方式优化
        self.change_detector = ChangeDetector(repo_path=repo_path)
        self.chat_engine = ChatEngine(config_file=config_file)
    

    def get_all_pys(self, directory):
        """
        获取给定目录下的所有 Python 文件。

        Args:
            directory (str): 要搜索的目录。

        Returns:
            list: 所有 Python 文件的路径列表。
        """
        python_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        return python_files
        
    def run_initial_doc(self,):
        """
        根据现有仓库的代码生成初始文档

        """
        repo_path = self.project_manager.repo_path
        md_root_path = os.path.join(repo_path, 'Markdown_Docs')  # 新的根目录

        for file_path in self.get_all_pys(repo_path):
            # 判断当前python文件内容是否为空：
            if os.path.getsize(file_path) == 0:
                continue
            # 判断当前文件是否有对应的md文件
            relative_path = os.path.relpath(file_path, repo_path)  # 获取相对路径
            md_file_path = os.path.join(md_root_path, relative_path.replace('.py', '.md'))

            # 如果md文件所在的目录不存在，创建它
            md_dir = os.path.dirname(md_file_path)
            if not os.path.exists(md_dir):
                os.makedirs(md_dir)

            if os.path.exists(md_file_path):
                logger.info(f"检测到 {md_file_path} 文件，将更新现有文档。")
            else:
                logger.info(f"未检测到 {md_file_path} 文件，将创建新文档。")
                with open(md_file_path, 'w') as md_file:  # 创建新的 .md 文件
                    md_file.write(f"***\n")  # 写入初始内容，例如对象的名称

    def fake_for_first_generate(self):
        """
        获取给定目录下的所有 Python 文件。

        Args:
            directory (str): 要搜索的目录。

        Returns:
            dict: 所有 Python 文件的路径映射到 True 的字典。
        """
        python_files = {}

        for root, dirs, files in os.walk(self.project_manager.repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    python_files[file_path] = True

        for file_path, is_new_file in python_files.items():
                # 判断当前python文件内容是否为空，如果为空则跳过：
                if os.path.getsize(file_path) == 0:
                    continue
                # 否则，根据文件路径处理变更的文件
                self.process_file_changes(self.project_manager.repo_path, file_path, is_new_file)


    def git_commit(self, file_path, commit_message):
        try:
            subprocess.check_call(['git', 'add', file_path])
            subprocess.check_call(['git', 'commit', '-m', commit_message])
        except subprocess.CalledProcessError as e:
            print(f'An error occurred while trying to commit {file_path}: {str(e)}')


    def run(self):
            """
            Runs the document update process.

            This method detects the changed Python files, processes each file, and updates the documents accordingly.

            Returns:
                None
            """
            changed_files = self.change_detector.get_changed_pys()
            logger.info(f"检测到变更的文件：{changed_files}")
            if len(changed_files) == 0:
                logger.info("没有检测到任何变更，不需要更新文档。")
                return

            repo_path = self.project_manager.repo_path

            for file_path, is_new_file in changed_files.items(): # 这里的file_path是相对路径

                # file_path = os.path.join(repo_path, file_path)  # 将file_path变成绝对路径
                # 判断当前python文件内容是否为空，如果为空则跳过：
                if os.path.getsize(os.path.join(repo_path, file_path)) == 0:
                    continue
                # 否则，根据文件路径处理变更的文件
                self.process_file_changes(repo_path, file_path, is_new_file)

    
    def process_file_changes(self, repo_path, file_path, is_new_file):
        """
        函数将在检测到的变更文件的循环中被调用，作用是根据文件绝对路径处理变更的文件，包括新增的文件和已存在的文件。
        其中，changes_in_pyfile是一个字典，包含了发生变更的结构的信息，示例格式为：{'added': {'add_context_stack', '__init__'}, 'removed': set()}

        Args:
            repo_path (str): The path to the repository.
            file_path (str): The path to the file.
            is_new_file (bool): Indicates whether the file is new or not.

        Returns:
            None
        """
        file_handler = FileHandler(repo_path=repo_path, file_path=file_path)
        # 获取整个py文件的代码
        source_code = file_handler.content
        changed_lines = self.change_detector.parse_diffs(self.change_detector.get_file_diff(file_path, is_new_file))
        changes_in_pyfile = self.change_detector.identify_changes_in_structure(changed_lines, file_handler.get_functions_and_classes(source_code))
        logger.info(f"检测到变更对象：\n{changes_in_pyfile}")
        # 判断当前文件是否有对应的md文件
        md_file_path = os.path.join(repo_path, "Markdown_Docs", file_path.replace('.py', '.md'))
        if os.path.exists(md_file_path):
            logger.info(f"检测到 {md_file_path} 文件，将更新现有文档。")
            self.update_documentation(file_handler, changes_in_pyfile, source_code, md_file_path)
        else:
            logger.info(f"未检测到 {md_file_path} 文件，将创建新文档。")
            self.create_new_documentation(file_handler, source_code, md_file_path)
        
    
    def update_documentation(self, file_handler, changes_in_pyfile, source_code, md_file_path):
        """
        函数的作用是接收变更对象字典，根据字典里的变更对象（added和removed）来更新已经存在的文档内容
        Args:
            file_handler (FileHandler): 文件处理器对象。
            changes_in_pyfile (list): Python文件中的更改列表。
            source_code (str): 源代码字符串。
            md_file_path (str): Markdown文件路径。

        Returns:
            None
        """
        new_obj, del_obj = self.get_new_objects(file_handler)
        # print(f"\n\ndel_obj(真正要被删除的对象):{del_obj}\n\n")

        # 处理被删除的对象
        for obj in del_obj: # 真正被删除的对象
            self.delete_documentation_from_md(obj, md_file_path)

        # 处理新增/更改的对象
        for changed_obj_name in changes_in_pyfile['added']:
            self.process_changed_object(file_handler, source_code, md_file_path, changed_obj_name)

        # 提交到git仓库

    def update_md_file(self, md_file_path, content, code_name, operation):
        """
        Update the Markdown file based on the operation.

        Args:
            md_file_path (str): The path to the Markdown file.
            content (str): The content to be written or the name of the code to be deleted.
            code_name (str): The name of the code being documented or deleted.
            operation (str): The operation to be performed, either 'write' or 'delete'.

        Returns:
            None
        """
        try:
            with open(md_file_path, 'r+') as md_file:
                md_content = md_file.read()
                obj_start = md_content.find("# " + code_name)

                if obj_start == -1:  # 如果没找到
                    if operation == 'write':
                        md_file.write(content)  # 新增内容直接写在文件末尾
                    else:
                        logger.info(f"未在 {md_file_path} 文件中找到 {code_name} 对象的文档，不做任何删除操作。")
                    return

                # 匹配对象文档的结尾字符
                obj_end = md_content.find("***", obj_start)

                if obj_end != -1:  # 如果匹配到了结尾字符
                    obj_end += len("***")  # 包括 "***" 本身的长度
                    if operation == 'write':
                        md_content = md_content[:obj_start] + content + md_content[obj_end:]
                    else:
                        md_content = md_content[:obj_start] + md_content[obj_end:]
                else:
                    if operation == 'write':
                        md_content = md_content[:obj_start] + content
                    else:
                        md_content = md_content[:obj_start]

                md_file.seek(0)
                md_file.write(md_content)
                md_file.truncate()

                if operation == 'delete':
                    logger.info(f"已从 {md_file_path} 文件中删除 {code_name} 对象的文档。")
                else:
                    logger.info(f"已将 {code_name} 对象的文档写入 {md_file_path} 文件。")
                
                # 将修改后的md文件内容提交到git仓库，输出文件相对路径
                # self.git_commit(md_file_path, f"Update {os.path.basename(md_file_path)}")
            


        except IOError as e:
            logger.error(f"Error updating documentation: {e}")

     
    def process_changed_object(self, file_handler, source_code, md_file_path, changed_obj_name):
        """
        处理added中的变更对象

        Args:
            file_handler (FileHandler): The file handler object.
            source_code (str): The source code of the whole .py file.
            md_file_path (str): The path of the markdown file.
            changed_obj_name (str): The name of the changed object.
            new_obj (bool): Flag indicating if the object is new.

        Returns:
            None
        """
        # 生成文档
        self.generate_markdown(file_handler, source_code, md_file_path, changed_obj_name)


    def get_new_objects(self, file_handler):
        """
        函数通过比较当前版本和上一个版本的.py文件，获取新增和删除的对象

        Args:
            file_handler (FileHandler): 文件处理器对象。
        Returns:
            tuple: 包含新增和删除对象的元组，格式为 (new_obj, del_obj)
        """
        current_version, previous_version = file_handler.get_modified_file_versions()
        parse_current_py = file_handler.get_functions_and_classes(current_version)
        parse_previous_py = file_handler.get_functions_and_classes(previous_version) if previous_version else []

        current_obj = {f[1] for f in parse_current_py}
        previous_obj = {f[1] for f in parse_previous_py}

        new_obj = list(current_obj - previous_obj)
        del_obj = list(previous_obj - current_obj)

        return new_obj, del_obj


    def create_new_documentation(self, file_handler, source_code, md_file_path):
        """
        这个函数处理的场景是创建新的文档，而不是更新现有文档。
        只有当前变更的.py文件找不到对应的.md文件的时候才会调用这个函数。

        Args:
            file_handler (FileHandler): The file handler object used to read the source code.
            source_code (str): The source code to generate documentation from.
            md_file_path (str): The file path to write the generated documentation.

        Returns:
            None
        """
        # 如果md文件所在的目录不存在，创建它
        md_dir = os.path.dirname(md_file_path)
        if not os.path.exists(md_dir):
            os.makedirs(md_dir)
        # 根据md_file_path创建一个空的.md文件
        open(md_file_path, 'a+').close()
        logger.info(f"新文档{md_file_path}已创建")

        # 获取当前.py文件源代码-->得到完整结构信息-->为每一个结构信息生成文档-->将文档写入.md文件
        self.generate_markdown(file_handler, source_code, md_file_path)


    def generate_markdown(self, file_handler, source_code, md_file_path, changed_obj_name=None):
        """
        对于 create_new_documentation 方法：

        当调用 generate_markdown 方法时，changed_obj_name 默认为 None。
        在 generate_markdown 方法内，当 changed_obj_name 为 None 时，if changed_obj_name is not None and name != changed_obj_name 这个条件判断总是为假，因此不会跳过任何对象。
        这意味着该方法会为源代码中的所有函数和类生成文档，符合 create_new_documentation 的预期行为。
        对于 process_changed_object 方法：

        当调用 generate_markdown 方法时，会传递一个特定的 changed_obj_name（即 update_document函数中的changes_in_pyfile['added']中的单个元素）。
        在 generate_markdown 方法内，当遍历到的对象名称 name 与 changed_obj_name 不匹配时，if changed_obj_name is not None and name != changed_obj_name 条件判断为真，因此会跳过这些不匹配的对象。
        只有当对象名称与 changed_obj_name 匹配时，才会为该对象生成文档，这符合 process_changed_object 需要只处理变更对象的预期行为。
        """
        with ThreadPoolExecutor(max_workers = 5) as executor:
            futures = []
            names = []
            for structure_type, name, start_line, end_line in file_handler.get_functions_and_classes(source_code):
                # 当changed_obj_name不为None时,表明这是process_changed_object的逻辑，只处理与之匹配的对象
                if changed_obj_name is not None and name != changed_obj_name:
                    continue
                
                # 只有当changed_obj_name为None（代表create_new_documentation逻辑），以及name与changed_obj_name相等时（代表process_changed_object的逻辑），才会执行下面的代码
                code_info = file_handler.get_obj_code(structure_type, name, start_line, end_line)
                future = executor.submit(self.chat_engine.generate_doc, code_info)
                futures.append(future)
                names.append(name)

                    
            # 等待所有线程完成，并按照原始顺序收集结果
            results = [future.result() for future in futures]
            print(f"results:{results}")

            for name, response_message in zip(names, results):
                documentation = response_message.content + "\n***\n"
                self.write_doc_to_md(md_file_path, documentation, name)


    def write_doc_to_md(self, md_file_path, documentation, code_name):
        self.update_md_file(md_file_path, documentation, code_name, 'write')


    def delete_documentation_from_md(self, changed_obj_name, md_file_path):
        self.update_md_file(md_file_path, '', changed_obj_name, 'delete')
   


if __name__ == "__main__":

    config_file = '/Users/logic/Documents/VisualStudioWorkspace/AI_doc/config.yml'
    repo_path = "/Users/logic/Documents/VisualStudioWorkspace/XAgent-Dev/"

    runner = Runner(config_file, repo_path)
    
    runner.run()

    logger.info("文档任务完成。")
