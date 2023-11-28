"""
这个类需要处理文件的差异和变更检测，它可能会用到 FileHandler 类来访问文件系统。
ChangeDetector 类的核心在于能够识别自上次提交以来文件的变更。
"""
import git
import os,re
from file_handler import FileHandler
import subprocess


class ChangeDetector:
    def __init__(self, repo_path):
        """
        Initializes a ChangeDetector object.

        Parameters:
        repo_path (str): The path to the repository.

        Returns:
        None
        """
        self.repo = git.Repo(repo_path)

    def get_changed_pys(self):
        """
        根据仓库仓库实例，获取仓库中变更的python文件
        
        这个函数会追踪到 Git 中以下状态的 Python 文件：
        1. 未暂存的变更：这包括新添加的文件（A）和已修改的文件（M）。这些文件的变更已经发生，但还没有被添加到 Git 的暂存区。

        2. 未跟踪的文件：这些是新创建的文件，还没有被 Git 跟踪。这些文件不在 Git 的暂存区，也不在 Git 的版本控制系统中。


        
        Returns:
            dict: 变更的python文件字典，键是文件路径，值是一个布尔值，表示这个文件是否是新建的

        输出示例：
        {'XAgent/engines/pipeline.py': False, 'XAgent/models/plan.py': True}
        """
        repo = self.repo
        changed_files = {}

        # 检测未暂存的变更
        diffs = repo.index.diff(None) + repo.index.diff('HEAD')
        for diff in diffs:
            # a_path是变更的文件路径
            if diff.change_type in ['A', 'M'] and diff.a_path.endswith('.py'):  # A表示新增，M表示修改
                is_new_file = diff.change_type == 'A'
                changed_files[diff.a_path] = is_new_file
        
        # 检测未跟踪的文件（新文件）
        untracked_files = [file for file in repo.untracked_files if file.endswith('.py') and file not in changed_files]
        for file in untracked_files:
            changed_files[file] = True

        return changed_files

    def get_file_diff(self, file_path, is_new_file):
        """
        函数的作用是获取某个文件的变更内容。对于新文件，使用 git diff --staged 获取差异。
        Args:
            file_path (str): 文件路径
            is_new_file (bool): 指示文件是否是新文件
        Returns:
            list: 变更内容列表
        """
        repo = self.repo

        if is_new_file:
            # 对于新文件，先将其添加到暂存区
            add_command = f'git -C {repo.working_dir} add "{file_path}"'
            subprocess.run(add_command, shell=True, check=True)

            # 获取暂存区的diff
            diffs = repo.git.diff('--staged', file_path).splitlines()
        else:
            # 对于非新文件，获取HEAD的diff
            diffs = repo.git.diff('HEAD', file_path).splitlines()

        return diffs

    
    def parse_diffs(self,diffs):
            """
            解析差异内容，提取出添加和删除的对象信息，对象可以是类或者函数。
            输出示例：{'added': [(86, '    '), (87, '    def to_json_new(self, comments = True):'), (88, '        data = {'), (89, '            "name": self.node_name,')...(95, '')], 'removed': []}
            在上述示例中，PipelineEngine和AI_give_params是添加的对象，没有删除的对象。
            但是这里的添加不代表是新加入的对象，因为在git diff中，对某一行的修改在diff中是以删除和添加的方式表示的。
            所以对于修改的内容，也会表示为这个对象经过了added操作。

            如果需要明确知道某个对象是被新加入的，需要使用get_added_objs()函数。
            Args:
                diffs (list): 包含差异内容的列表。由类内部的get_file_diff()函数获取。

            Returns:
                dict: 包含添加和删除行信息的字典，格式为 {'added': set(), 'removed': set()}
            """
            changed_lines = {'added': [], 'removed': []}
            line_number_current = 0
            line_number_change = 0

            for line in diffs:
                # 检测行号信息，例如 "@@ -43,33 +43,40 @@"
                line_number_info = re.match(r'@@ \-(\d+),\d+ \+(\d+),\d+ @@', line)
                if line_number_info:
                    line_number_current = int(line_number_info.group(1))
                    line_number_change = int(line_number_info.group(2))
                    continue

                if line.startswith('+') and not line.startswith('+++'):
                    changed_lines['added'].append((line_number_change, line[1:]))
                    line_number_change += 1
                elif line.startswith('-') and not line.startswith('---'):
                    changed_lines['removed'].append((line_number_current, line[1:]))
                    line_number_current += 1
                else:
                    # 对于没有变化的行，两者的行号都需要增加
                    line_number_current += 1
                    line_number_change += 1

            return changed_lines

    def identify_changes_in_structure(self,changed_lines, structures):
        """
        识别发生更改的函数或类的结构。
        输出示例：{'added': {'PipelineAutoMatNode', 'to_json_new'}, 'removed': set()}

        Args:
            changed_lines (dict): 包含发生更改的行号的字典，{'added': [(行号，变更内容)], 'removed': [(行号，变更内容)]}
            structures (list): 接收的是get_functions_and_classes包含函数或类结构的列表，每个结构由结构类型、名称、起始行号和结束行号组成。

        Returns:
            dict: 包含发生更改的结构的字典，键为更改类型，值为结构名称的集合。
                可能的更改类型为'added'（新增）和'removed'（移除）。
        """
        changes_in_structures = {'added': set(), 'removed': set()}
        for change_type, lines in changed_lines.items():
            for line_number, _ in lines:
                for structure_type, name, start_line, end_line in structures:
                    if start_line <= line_number <= end_line:
                        changes_in_structures[change_type].add(name)
        return changes_in_structures
    
if __name__ == "__main__":
    repo_path = "/Users/logic/Documents/VisualStudioWorkspace/XAgent-Dev/"
    change_detector = ChangeDetector(repo_path)
    changed_files = change_detector.get_changed_pys()
    print(changed_files)
    for file_path, is_new_file in changed_files.items():
        print(change_detector.get_file_diff(file_path))
        changed_lines = change_detector.parse_diffs(change_detector.get_file_diff(file_path))
        print("changed_lines:",changed_lines)
        file_handler = FileHandler(repo_path=repo_path, file_path=file_path)
        changes_in_pyfile = change_detector.identify_changes_in_structure(changed_lines, file_handler.get_functions_and_classes(file_handler.content))
        print("Changes in Structures:", changes_in_pyfile)

