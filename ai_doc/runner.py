import os,sys,re,json
import file_handler as file_handler
from file_handler import FileHandler
from change_detector import ChangeDetector
from project_manager import ProjectManager
from chat_engine import ChatEngine
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import subprocess
import logging
from config import CONFIG


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Runner:
    def __init__(self):
        self.project_manager = ProjectManager(repo_path=CONFIG['repo_path'],project_hierachy=CONFIG['project_hierachy']) 
        self.change_detector = ChangeDetector(repo_path=CONFIG['repo_path'])
        self.chat_engine = ChatEngine(CONFIG=CONFIG)
    
    def generate_hierachy(self):
        """
        函数的作用是为整个项目生成一个最初的全局结构信息
        """
        # 初始化一个File_handler
        file_handler = FileHandler(self.project_manager.repo_path, None)
        file_structure = file_handler.generate_overall_structure()
        json_output = file_handler.convert_structure_to_json(file_structure)

        json_file = os.path.join(self.CONFIG['repo_path'], self.CONFIG['project_hierachy'])
        # Save the JSON to a file
        with open(os.path.join(file_handler.repo_path, json_file), 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)

        logger.info(f"JSON structure generated and saved to '{json_file}'.")

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
        
    # def run_initial_structure(self):
    #     """
    #     根据现有仓库的代码生成初始文档结构

    #     """
    #     repo_path = self.project_manager.repo_path
    #     md_root_path = os.path.join(repo_path, self.CONFIG['Markdown_Docs_folder'])  # 新的根目录

    #     for file_path in self.get_all_pys(repo_path):
    #         # 判断当前python文件内容是否为空：
    #         if os.path.getsize(file_path) == 0:
    #             continue
    #         # 判断当前文件是否有对应的md文件
    #         relative_path = os.path.relpath(file_path, repo_path)  # 获取相对路径
    #         md_file_path = os.path.join(md_root_path, relative_path.replace('.py', '.md'))

    #         # 如果md文件所在的目录不存在，创建它
    #         md_dir = os.path.dirname(md_file_path)
    #         if not os.path.exists(md_dir):
    #             os.makedirs(md_dir)

    #         if os.path.exists(md_file_path):
    #             logger.info(f"检测到 {md_file_path} 文件，将更新现有文档。")
    #         else:
    #             logger.info(f"未检测到 {md_file_path} 文件，将创建新文档。")
    #             with open(md_file_path, 'w') as md_file:  # 创建新的 .md 文件
    #                 md_file.write(f"***\n")  # 写入初始内容，例如对象的名称

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
            subprocess.check_call(['git', 'commit', '--no-verify', '-m', commit_message])
        except subprocess.CalledProcessError as e:
            print(f'An error occurred while trying to commit {file_path}: {str(e)}')


    def run(self):
            """
            Runs the document update process.

            This method detects the changed Python files, processes each file, and updates the documents accordingly.

            Returns:
                None
            """
            changed_files = self.change_detector.get_staged_pys()
            logger.info(f"检测到暂存区中变更的文件：{changed_files}")
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


    def add_new_item(self, file_handler, json_data):
        new_item = {}
        new_item["file_path"] = os.path.join(self.project_manager.repo_path, file_handler.file_path)
        new_item["objects"] = []
        # 因为是新增的项目，所以这个文件里的所有对象都要写一个文档
        for structure_type, name, start_line, end_line, parent in file_handler.get_functions_and_classes(file_handler.read_file()):
            code_info = file_handler.get_obj_code_info(structure_type, name, start_line, end_line, parent)
            md_content = self.chat_engine.generate_doc(code_info, file_handler)
            code_info["md_content"] = md_content
            new_item["objects"].append(code_info)

        json_data["files"].append(new_item)
        # 将新的项写入json文件
        with open(self.project_manager.project_hierachy, 'w') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        logger.info(f"已将新增文件 {file_handler.file_path} 的结构信息写入json文件。")
        # 将变更部分的json文件内容转换成markdown内容
        markdown = file_handler.convert_to_markdown_file(file_path=os.path.join(self.project_manager.repo_path, file_handler.file_path))
        # 将markdown内容写入.md文件
        file_handler.write_file(os.path.join(self.project_manager.repo_path, CONFIG['Markdown_Docs_folder'], file_handler.file_path.replace('.py', '.md')), markdown)
        logger.info(f"已生成新增文件 {file_handler.file_path} 的Markdown文档。")

    
    def process_file_changes(self, repo_path, file_path, is_new_file):
        """
        函数将在检测到的变更文件的循环中被调用，作用是根据文件绝对路径处理变更的文件，包括新增的文件和已存在的文件。
        其中，changes_in_pyfile是一个字典，包含了发生变更的结构的信息，示例格式为：{'added': {'add_context_stack', '__init__'}, 'removed': set()}

        Args:
            repo_path (str): The path to the repository.
            file_path (str): The relative path to the file.
            is_new_file (bool): Indicates whether the file is new or not.

        Returns:
            None
        """
        file_handler = FileHandler(repo_path=repo_path, file_path=file_path) # 变更文件的操作器
        # 获取整个py文件的代码
        source_code = file_handler.read_file()
        changed_lines = self.change_detector.parse_diffs(self.change_detector.get_file_diff(file_path, is_new_file))
        changes_in_pyfile = self.change_detector.identify_changes_in_structure(changed_lines, file_handler.get_functions_and_classes(source_code))
        logger.info(f"检测到变更对象：\n{changes_in_pyfile}")
        
        # 判断project_hierachy.json文件中能否找到对应.py文件路径的项
        with open(self.project_manager.project_hierachy, 'r') as f:
            json_data = json.load(f)
        
        # 标记是否找到了对应的文件
        found = False
        for i, file in enumerate(json_data["files"]):
            if file["file_path"] == os.path.join(self.project_manager.repo_path, file_handler.file_path): # 找到了对应文件
                # 更新json文件中的内容
                json_data["files"][i] = self.update_existing_item(file, file_handler, changes_in_pyfile)
                # 将更新后的file写回到json文件中
                with open(self.project_manager.project_hierachy, 'w') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                
                logger.info(f"已更新{file_handler.file_path}文件的json结构信息。")

                found = True

                # 将变更部分的json文件内容转换成markdown内容
                markdown = file_handler.convert_to_markdown_file(file_path=os.path.join(self.project_manager.repo_path, file_handler.file_path))
                # 将markdown内容写入.md文件
                file_handler.write_file(os.path.join(self.project_manager.repo_path, CONFIG['Markdown_Docs_folder'], file_handler.file_path.replace('.py', '.md')), markdown)
                logger.info(f"已更新{file_handler.file_path}文件的Markdown文档。")
                break

        # 如果没有找到对应的文件，就添加一个新的项
        if not found:
            self.add_new_item(file_handler,json_data)


    def update_existing_item(self, file, file_handler, changes_in_pyfile):
        
        new_obj, del_obj = self.get_new_objects(file_handler)

        # 处理被删除的对象
        for obj_name in del_obj: # 真正被删除的对象
            for file_obj in file["objects"]:
                if file_obj["name"] == obj_name:
                    file["objects"].remove(file_obj)
                    logger.info(f"已删除 {obj_name} 对象。")
                    break

        # 处理新增/更改的对象
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for changed_obj in changes_in_pyfile['added']:
                future = executor.submit(self.update_object, file, file_handler, changed_obj[0])
                logger.info(f"正在生成 {file_handler.file_path}中的{changed_obj[0]} 对象文档...")
                futures.append(future)

            for future in futures:
                future.result()

        # 更新传入的file参数
        return file


    def update_object(self, file, file_handler, obj_name):
        for obj in file["objects"]:
            if obj["name"] == obj_name:
                code_info = {
                    "type": obj["type"],
                    "name": obj["name"],
                    "code_content": obj["code_content"],
                    "have_return": obj["have_return"],
                    "code_start_line": obj["code_start_line"],
                    "code_end_line": obj["code_end_line"],
                    "parent": obj["parent"],
                    "name_column": obj["name_column"]
                }
                response_message = self.chat_engine.generate_doc(code_info, file_handler)
                obj["md_content"] = response_message.content

                break


    def update_documentation(self, file_handler, changes_in_pyfile, source_code):
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
            self.delete_doc_from_json(file_handler, obj)

        # 处理新增/更改的对象
        for changed_obj in changes_in_pyfile['added']:
            self.process_changed_object(file_handler, source_code, changed_obj)


    def process_changed_object(self, file_handler, source_code, changed_obj):
        """
        处理added中的变更对象

        Args:
            file_handler (FileHandler): The file handler object.
            source_code (str): The source code of the whole .py file.
            md_file_path (str): The path of the markdown file.
            changed_obj (str): The name of the changed object.
            new_obj (bool): Flag indicating if the object is new.

        Returns:
            None
        """
        # 生成文档
        self.generate_markdown(file_handler, source_code, changed_obj)


    def get_new_objects(self, file_handler):
        """
        函数通过比较当前版本和上一个版本的.py文件，获取新增和删除的对象

        Args:
            file_handler (FileHandler): 文件处理器对象。
        Returns:
            tuple: 包含新增和删除对象的元组，格式为 (new_obj, del_obj)
        输出示例：
        new_obj: ['add_context_stack', '__init__']
        del_obj: []
        """
        current_version, previous_version = file_handler.get_modified_file_versions()
        parse_current_py = file_handler.get_functions_and_classes(current_version)
        parse_previous_py = file_handler.get_functions_and_classes(previous_version) if previous_version else []

        current_obj = {f[1] for f in parse_current_py}
        previous_obj = {f[1] for f in parse_previous_py}

        new_obj = list(current_obj - previous_obj)
        del_obj = list(previous_obj - current_obj)

        return new_obj, del_obj


    # def create_new_documentation(self, file_handler, source_code, md_file_path):
    #     """
    #     这个函数处理的场景是创建新的文档，而不是更新现有文档。
    #     只有当前变更的.py文件找不到对应的.md文件的时候才会调用这个函数。

    #     Args:
    #         file_handler (FileHandler): The file handler object used to read the source code.
    #         source_code (str): The source code to generate documentation from.
    #         md_file_path (str): The file path to write the generated documentation.

    #     Returns:
    #         None
    #     """
    #     # 对一个新文档来说，先要在json文件中增加它的项，所以要先调用LLM生成doc内容，写入json中

    #     # 如果md文件所在的目录不存在，创建它
    #     md_dir = os.path.dirname(md_file_path)
    #     if not os.path.exists(md_dir):
    #         os.makedirs(md_dir)
    #     # 根据md_file_path创建一个空的.md文件
    #     open(md_file_path, 'a+').close()
    #     logger.info(f"新文档{md_file_path}已创建")
    #     # 获取当前.py文件源代码-->得到完整结构信息-->为每一个结构信息生成文档-->将每一个文档结构信息写入json文件
    #     changed_obj = file_handler.get_functions_and_classes(source_code)
    #     self.generate_markdown(file_handler, source_code)

    #     # 将json文件中这部分的内容转换成markdown内容
    #     markdown = file_handler.convert_to_markdown_file()
    #     # 将markdown内容写入.md文件
    #     file_handler.write_file(md_file_path, markdown)

    def generate_markdown(self, file_handler, source_code, changed_obj=None):
        """
        对于 create_new_documentation 方法：

        当调用 generate_markdown 方法时，changed_obj 默认为 None。
        在 generate_markdown 方法内，当 changed_obj 为 None 时，if changed_obj is not None and name != changed_obj 这个条件判断总是为假，因此不会跳过任何对象。
        这意味着该方法会为源代码中的所有函数和类生成文档，符合 create_new_documentation 的预期行为。
        对于 process_changed_object 方法：

        当调用 generate_markdown 方法时，会传递一个特定的 changed_obj（即 update_document函数中的changes_in_pyfile['added']中的单个元素）。
        在 generate_markdown 方法内，当遍历到的对象名称 name 与 changed_obj 不匹配时，if changed_obj is not None and name != changed_obj 条件判断为真，因此会跳过这些不匹配的对象。
        只有当对象名称与 changed_obj 匹配时，才会为该对象生成文档，这符合 process_changed_object 需要只处理变更对象的预期行为。
        """

        with ThreadPoolExecutor(max_workers = 5) as executor:
            futures = []
            code_infos = []
            for structure_type, name, start_line, end_line, parent in file_handler.get_functions_and_classes(source_code):
                # 当changed_obj不为None时,表明这是process_changed_object的逻辑，只处理与之匹配的对象
                # TODO: 生成新文档时候的逻辑未完成
                changed_obj_name = changed_obj[0] if changed_obj is not None else None
                if changed_obj_name is not None and name != changed_obj_name:
                    continue
                
                # 只有当changed_obj为None（代表create_new_documentation逻辑），以及name与changed_obj相等时（代表process_changed_object的逻辑），才会执行下面的代码
                code_info = file_handler.get_obj_code_info(structure_type, name, start_line, end_line, parent)
                future = executor.submit(self.chat_engine.generate_doc, code_info, file_handler)
                futures.append(future)
                code_infos.append(code_info)
                    
            # 等待所有线程完成，并按照原始顺序收集结果
            results = [future.result() for future in futures]

            for code_info, response_message in zip(code_infos, results):
                documentation = response_message.content + "\n***\n"
                self.write_doc_to_json(file_handler, documentation, code_info)


    # def write_doc_to_json(self, file_handler, documentation, code_info):
    #     self.update_json_file(file_handler, documentation, code_info, 'write')


    # def delete_doc_from_json(self, file_handler, obj):
    #     code_info = {"name": obj}
    #     self.update_json_file(file_handler, '', code_info, 'delete')


    # def update_json_file(self, file_handler, doc, code_info, operation):
    #     """
    #     Update the Json file based on the operation.

    #     Args:
    #         md_file_path (str): The path to the Markdown file.
    #         content (str): The content to be written or the name of the code to be deleted.
    #         code_info (str): The info of the code being documented or deleted.
    #         operation (str): The operation to be performed, either 'write' or 'delete'.

    #     Returns:
    #         None
    #     """
    #     # 打开json文件，如果文件不存在，抛出异常
    #     json_file_path = os.path.join(self.project_manager.repo_path, 'project_hierachy.json')
    #     if not os.path.exists(json_file_path):
    #         raise ValueError(f"JSON file not found at {json_file_path}")
    #     try:
    #         # 读取json文件，在json数据中寻找根据file_handler.file_path更改后缀的绝对路径
    #         with open(json_file_path, 'r', encoding='utf-8') as f:
    #             json_data = json.load(f)
    #         # 遍历json_data["files"]列表中的每个字典
    #         for file in json_data["files"]:
    #             if file["file_path"] == os.path.join(self.project_manager.repo_path, file_handler.file_path): # 找到了对应文件
    #                 # 根据传入的code_info对file_objects中的对象进行operation操作
    #                 for obj in file["objects"]:
    #                     if obj["name"] == code_info["name"]:
    #                         if operation == 'write':
    #                             obj["md_content"] = doc
    #                         else:
    #                             file["objects"].remove(obj)
    #                         break
    #                     # 如果code_name不在file_objects中，说明是新增的对象，需要将其添加到file_objects中
    #                     else:
    #                         if operation == 'write':
    #                             code_info["md_content"] = doc
    #                             file["objects"].append(code_info)
    #                             # 把更改后的file_objects写回到json文件中
    #                     break
    #         with open(json_file_path, 'w', encoding='utf-8') as f:
    #             json.dump(json_data, f, ensure_ascii=False, indent=4) 
            

    #         if operation == 'delete':
    #             logger.info(f"已从json文件中删除 {code_info['name']} 对象。")
    #         else:
    #             logger.info(f"已将 {code_info['name']} 对象的文档写入json文件。")
            

    #     except Exception as e:
    #             logger.error(f"Error updating documentation: {e}")
             
    #             # 将修改后的md文件内容提交到git仓库，输出文件相对路径
    #             # self.git_commit(md_file_path, f"Update {os.path.basename(md_file_path)}")
            

if __name__ == "__main__":

    runner = Runner()
    
    # runner.generate_hierachy()
    runner.run()

    logger.info("文档任务完成。")

    # sys.exit(1)

    # file_handler = FileHandler(repo_path, 'XAgent/DSL_runner/ProAgent/n8n_tester/mock_input_test.py')
    # new_obj, del_obj = runner.get_new_objects(file_handler)

    # print(f"\n\nnew_obj:{new_obj}\n\ndel_obj:{del_obj}\n\n")
