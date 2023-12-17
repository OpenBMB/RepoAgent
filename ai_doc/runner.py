import os, json
from ai_doc.file_handler import FileHandler
from ai_doc.change_detector import ChangeDetector
from ai_doc.project_manager import ProjectManager
from ai_doc.chat_engine import ChatEngine
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import subprocess
import logging
from ai_doc.config import CONFIG


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

        json_file = os.path.join(CONFIG['repo_path'], CONFIG['project_hierachy'])
        # Save the JSON to a file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)

        # logger.info(f"JSON structure generated and saved to '{json_file}'.")

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
        

    def first_generate(self):
        """
        根据全局json结构的信息，生成整个项目所有python文件的文档
        """
        # 检测是否存在全局的 project_hierachy.json 结构信息
        if not os.path.exists(self.project_manager.project_hierachy):
            self.generate_hierachy()
            logger.info(f"已生成项目全局结构信息，存储路径为: {self.project_manager.project_hierachy}")

        with open(self.project_manager.project_hierachy, 'r') as f:
            json_data = json.load(f)

        # 创建一个线程池
        # TODO: Jedi 库多线程调用会出错，待解决
        with ThreadPoolExecutor(max_workers=1) as executor: 
            logger.info(f"正在生成项目所有 {len(json_data['files'])}个 Python文件的文档...")

            # 遍历json_data中的每个文件
            for file in json_data['files']:
                futures = []
                file_handler = FileHandler(CONFIG['repo_path'], os.path.relpath(file['file_path'], CONFIG['repo_path']))

                # 判断当前文件是否为空，如果为空则跳过：
                if os.path.getsize(file['file_path']) == 0:
                    continue

                # 遍历文件中的每个对象
                for index, obj in enumerate(file['objects']):
                    code_info = {
                        # 提取obj中的信息
                        "type": obj["type"],
                        "name": obj["name"],
                        "code_content": obj["code_content"],
                        "have_return": obj["have_return"],
                        "code_start_line": obj["code_start_line"],
                        "code_end_line": obj["code_end_line"],
                        "parent": obj["parent"],
                        "name_column": obj["name_column"]
                    }

                    # 并发提交文件中每个对象的文档生成任务到线程池，并将future和对应的obj存储为元组
                    future = executor.submit(self.chat_engine.generate_doc, code_info, file_handler)
                    futures.append((future, obj, index))

                # 收集响应结果
                for future, obj, index in futures:
                    response_message = future.result()  # 等待结果
                    logger.info(f" -- 正在生成 {file_handler.file_path}中的{obj['name']} 对象文档...")
                    file['objects'][index]["md_content"] = response_message.content
                
                futures = []

                # 将json_data写回文件
                with open(self.project_manager.project_hierachy, 'w') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)

                # 对于每个文件，转换json内容到markdown
                markdown = file_handler.convert_to_markdown_file(file_path=file['file_path'])
                # 写入markdown内容到.md文件
                file_handler.write_file(os.path.join(self.project_manager.repo_path, CONFIG['Markdown_Docs_folder'], file_handler.file_path.replace('.py', '.md')), markdown)
                logger.info(f"已生成 {file_handler.file_path} 的Markdown文档。")

            

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
        # 首先检测是否存在全局的 project_hierachy.json 结构信息
        abs_project_hierachy_path = os.path.join(CONFIG['repo_path'], CONFIG['project_hierachy'])
        if not os.path.exists(abs_project_hierachy_path):
            self.generate_hierachy()
            logger.info(f"已生成项目全局结构信息，存储路径为: {abs_project_hierachy_path}")
    
        changed_files = self.change_detector.get_staged_pys()

        if len(changed_files) == 0:
            logger.info("没有检测到任何变更，不需要更新文档。")
            return
        
        else:
            logger.info(f"检测到暂存区中变更的文件：{changed_files}")

        repo_path = self.project_manager.repo_path

        for file_path, is_new_file in changed_files.items(): # 这里的file_path是相对路径

            # file_path = os.path.join(repo_path, file_path)  # 将file_path变成绝对路径
            # 判断当前python文件内容是否为空，如果为空则跳过：
            if os.path.getsize(os.path.join(repo_path, file_path)) == 0:
                continue
            # 否则，根据文件路径处理变更的文件
            self.process_file_changes(repo_path, file_path, is_new_file)
        
        logger.info(f'添加了 {self.change_detector.add_unstaged_mds()} 到暂存区') 


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

        # 只要一个文件中的某一个对象发生了变更，这个文件中的其他对象的code_info内容（除了md_content）都需要改变
        # 依靠再次识别这个文件的代码，更新其他对象的code_start_line等等可能被影响到的字段信息
        file_structure_result = file_handler.generate_file_structure(file["file_path"])
        # file_structure_result返回的是：
        # {
        #     "file_path": file_path,
        #     "objects": json_objects
        # }

        new_objects = file_structure_result["objects"]
        for new_obj in new_objects:
            for obj in file["objects"]:
                if obj["name"] == new_obj["name"]:
                    obj["type"] = new_obj["type"]
                    obj["code_start_line"] = new_obj["code_start_line"]
                    obj["code_end_line"] = new_obj["code_end_line"]
                    obj["parent"] = new_obj["parent"]
                    obj["name_column"] = new_obj["name_column"]
                
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


if __name__ == "__main__":

    runner = Runner()
    
    if CONFIG["first_generate"]:
        runner.first_generate()
    runner.run()

    logger.info("文档任务完成。")

