import os, json
from ai_doc.file_handler import FileHandler
from ai_doc.change_detector import ChangeDetector
from ai_doc.project_manager import ProjectManager
from ai_doc.chat_engine import ChatEngine
from ai_doc.doc_meta_info import MetaInfo
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import subprocess
from loguru import logger
from ai_doc.config import CONFIG


class Runner:
    def __init__(self):
        self.project_manager = ProjectManager(repo_path=CONFIG['repo_path'],project_hierarchy=CONFIG['project_hierarchy']) 
        self.change_detector = ChangeDetector(repo_path=CONFIG['repo_path'])
        self.chat_engine = ChatEngine(CONFIG=CONFIG)

        self.ensure_project_hierarchy()
        self.meta_info = MetaInfo.from_project_hierarchy_json(CONFIG['repo_path'])
        # self.meta_info.target_repo_hierarchical_tree.print_recursive()
        # topology_list = self.meta_info.get_topology()

    def ensure_project_hierarchy(self):
        if not os.path.exists(self.project_manager.project_hierarchy):
            self.generate_hierachy()
            logger.info(f"已生成项目全局结构信息，存储路径为: {self.project_manager.project_hierarchy}")

    
    def generate_hierachy(self):
        """
        函数的作用是为整个项目生成一个最初的全局结构信息
        """
        # 初始化一个File_handler
        file_handler = FileHandler(self.project_manager.repo_path, None)
        repo_structure = file_handler.generate_overall_structure()
        # json_output = file_handler.convert_structure_to_json(repo_structure)

        json_file = os.path.join(CONFIG['repo_path'], CONFIG['project_hierarchy'])
        # Save the JSON to a file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(repo_structure, f, indent=4, ensure_ascii=False)

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
        logger.info("Starting to generate documentation.")

        with open(self.project_manager.project_hierarchy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # 遍历json_data中的每个对象
        for rel_file_path, file_dict in json_data.items():

            # 判断当前文件是否为空，如果为空则跳过：
            if os.path.getsize(os.path.join(CONFIG['repo_path'],rel_file_path)) == 0:
                continue

            # 对于每个单独文件里的每一个对象：获取其引用者列表
            referencer_list = [] # 单独拿一个referencer_list出来存储引用者是为了避免JEDI并发处理报错
            
            for obj_name, obj_info in file_dict.items():
                referencer_obj = {
                    "obj_name": obj_name,
                    "obj_referencer_list": self.project_manager.find_all_referencer(
                        variable_name=obj_name,
                        file_path=rel_file_path,
                        line_number=obj_info["code_start_line"],
                        column_number=obj_info["name_column"]
                    )
                }
                referencer_list.append(referencer_obj)

            
            # 在每一个file下面开一个线程池，线程是对一个文件中的多个obj进行文档生成
            with ThreadPoolExecutor(max_workers=5) as executor: 

                futures = []
                file_handler = FileHandler(CONFIG['repo_path'], rel_file_path)

                # 遍历文件中的每个对象
                for index, ref_obj in enumerate(referencer_list):
                    if ref_obj["obj_name"] in file_dict:
                        # 并发提交文件中每个对象的文档生成任务到线程池，并将future和对应的obj存储为元组
                        future = executor.submit(self.chat_engine.generate_doc, file_dict[ref_obj['obj_name']], file_handler, ref_obj["obj_referencer_list"])
                        futures.append((future, ref_obj, index))

                # 收集响应结果
                for future, ref_obj, index in futures:
                    logger.info(f" -- 正在生成 {file_handler.file_path}中的{ref_obj['obj_name']} 对象文档...")
                    response_message = future.result()  # 等待结果
                    file_dict[ref_obj['obj_name']]["md_content"] = response_message.content
                
                futures = []

            # 在对文件的循环内，将json_data写回文件
            with open(self.project_manager.project_hierarchy, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

            # 对于每个文件，转换json内容到markdown
            markdown = file_handler.convert_to_markdown_file(file_path=rel_file_path)
            # 写入markdown内容到.md文件
            file_handler.write_file(os.path.join(self.project_manager.repo_path, CONFIG['Markdown_Docs_folder'], file_handler.file_path.replace('.py', '.md')), markdown)
            logger.info(f"\n已生成 {file_handler.file_path} 的Markdown文档。\n")

            

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
        logger.info("Starting to detect changes.")
    
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
        

    def add_new_item(self, file_handler, json_data):
        file_dict = {}
        # 因为是新增的项目，所以这个文件里的所有对象都要写一个文档
        for structure_type, name, start_line, end_line, parent in file_handler.get_functions_and_classes(file_handler.read_file()):
            code_info = file_handler.get_obj_code_info(structure_type, name, start_line, end_line, parent)
            md_content = self.chat_engine.generate_doc(code_info, file_handler)
            code_info["md_content"] = md_content
            # 文件对象file_dict中添加一个新的对象
            file_dict[name] = code_info

        json_data[file_handler.file_path] = file_dict
        # 将新的项写入json文件
        with open(self.project_manager.project_hierarchy, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        logger.info(f"已将新增文件 {file_handler.file_path} 的结构信息写入json文件。")
        # 将变更部分的json文件内容转换成markdown内容
        markdown = file_handler.convert_to_markdown_file(file_path=file_handler.file_path)
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
        
        # 判断project_hierarchy.json文件中能否找到对应.py文件路径的项
        with open(self.project_manager.project_hierarchy, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # 如果找到了对应文件
        if file_handler.file_path in json_data:
            # 更新json文件中的内容
            json_data[file_handler.file_path] = self.update_existing_item(json_data[file_handler.file_path], file_handler, changes_in_pyfile)
            # 将更新后的file写回到json文件中
            with open(self.project_manager.project_hierarchy, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"已更新{file_handler.file_path}文件的json结构信息。")

            # 将变更部分的json文件内容转换成markdown内容
            markdown = file_handler.convert_to_markdown_file(file_path=file_handler.file_path)
            # 将markdown内容写入.md文件
            file_handler.write_file(os.path.join(self.project_manager.repo_path, CONFIG['Markdown_Docs_folder'], file_handler.file_path.replace('.py', '.md')), markdown)
            logger.info(f"已更新{file_handler.file_path}文件的Markdown文档。")

        # 如果没有找到对应的文件，就添加一个新的项
        else:
            self.add_new_item(file_handler,json_data)

        # 将run过程中更新的Markdown文件（未暂存）添加到暂存区
        git_add_result = self.change_detector.add_unstaged_mds()
        
        if len(git_add_result) > 0:
            logger.info(f'已添加 {[file for file in git_add_result]} 到暂存区') 


    def update_existing_item(self, file_dict, file_handler, changes_in_pyfile):
        new_obj, del_obj = self.get_new_objects(file_handler)

        # 处理被删除的对象
        for obj_name in del_obj: # 真正被删除的对象
            if obj_name in file_dict:
                del file_dict[obj_name]
                logger.info(f"已删除 {obj_name} 对象。")

        referencer_list = []

        # 生成文件的结构信息，获得当前文件中的所有对象， 这里其实就是文件更新之后的结构了
        current_objects = file_handler.generate_file_structure(file_handler.file_path) 

        current_info_dict = {obj["name"]: obj for obj in current_objects.values()}

        # 更新全局文件结构信息，比如代码起始行\终止行等
        for current_obj_name, current_obj_info in current_info_dict.items():
            if current_obj_name in file_dict:
                # 如果当前对象在旧对象列表中存在，更新旧对象的信息
                file_dict[current_obj_name]["type"] = current_obj_info["type"]
                file_dict[current_obj_name]["code_start_line"] = current_obj_info["code_start_line"]
                file_dict[current_obj_name]["code_end_line"] = current_obj_info["code_end_line"]
                file_dict[current_obj_name]["parent"] = current_obj_info["parent"]
                file_dict[current_obj_name]["name_column"] = current_obj_info["name_column"]
            else:
                # 如果当前对象在旧对象列表中不存在，将新对象添加到旧对象列表中
                file_dict[current_obj_name] = current_obj_info


        # 对于每一个对象：获取其引用者列表
        for obj_name, _ in changes_in_pyfile['added']:
            for current_object in current_objects.values(): # 引入new_objects的目的是获取到find_all_referencer中必要的参数信息。在changes_in_pyfile['added']中只有对象和其父级结构的名称，缺少其他参数
                if obj_name == current_object["name"]:  # 确保只有当added中的对象名称匹配new_objects时才添加引用者
                    # 获取每个需要生成文档的对象的引用者
                    referencer_obj = {
                        "obj_name": obj_name,
                        "obj_referencer_list": self.project_manager.find_all_referencer(
                            variable_name=current_object["name"],
                            file_path=file_handler.file_path,
                            line_number=current_object["code_start_line"],
                            column_number=current_object["name_column"]
                        )
                    }
                    referencer_list.append(referencer_obj) # 对于每一个正在处理的对象，添加他的引用者字典到全部对象的应用者列表中

        with ThreadPoolExecutor(max_workers=5) as executor:
            # 通过线程池并发执行
            futures = []
            for changed_obj in changes_in_pyfile['added']: # 对于每一个待处理的对象
                for ref_obj in referencer_list:
                    if changed_obj[0] == ref_obj["obj_name"]: # 在referencer_list中找到它的引用者字典！
                        future = executor.submit(self.update_object, file_dict, file_handler, changed_obj[0], ref_obj["obj_referencer_list"])
                        logger.info(f"正在生成 {file_handler.file_path}中的{changed_obj[0]} 对象文档...")
                        futures.append(future)

            for future in futures:
                future.result()

        # 更新传入的file参数
        return file_dict
    

    def update_object(self, file_dict, file_handler, obj_name, obj_referencer_list):
        if obj_name in file_dict: # file_dict保存的是原先的旧的对象信息
            obj = file_dict[obj_name]
            response_message = self.chat_engine.generate_doc(obj, file_handler, obj_referencer_list)
            obj["md_content"] = response_message.content



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
    
    runner.meta_info.target_repo_hierarchical_tree.print_recursive()
    topology_list = runner.meta_info.get_topology()
    for node in topology_list:
        print(node.get_full_name())
    # runner.run()
    # runner.first_generate()

    logger.info("文档任务完成。")

