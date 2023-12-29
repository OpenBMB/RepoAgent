"""
这个类需要处理文件的差异和变更检测，它可能会用到 FileHandler 类来访问文件系统。
ChangeDetector 类的核心在于能够识别自上次提交以来文件的变更。
"""
import git
import re, os
from repo_agent.file_handler import FileHandler
import subprocess
from repo_agent.config import CONFIG


class ChangeDetector:
    def __init__(self, repo_path):
        """
        Initializes a ChangeDetector object.

        Parameters:
        repo_path (str): The path to the repository.

        Returns:
        None
        """
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def get_staged_pys(self):
        """
        Get added python files in the repository that have been staged.

        This function only tracks the changes of Python files in Git that have been staged,
        i.e., the files that have been added using `git add`.

        Returns:
            dict: A dictionary of changed Python files, where the keys are the file paths and the values are booleans indicating whether the file is newly created or not.
        
        """
        repo = self.repo
        staged_files = {}

        # Detect Staged Changes
        # Please note! The logic of the GitPython library is different from git. Here, the R=True parameter is used to reverse the version comparison logic.
        # In the GitPython library, repo.index.diff('HEAD') compares the staging area (index) as the new state with the original HEAD commit (old state). This means that if there is a new file in the current staging area, it will be shown as non-existent in HEAD, i.e., "deleted".
        # R=True reverses this logic, correctly treating the last commit (HEAD) as the old state and comparing it with the current staging area (new state) (Index). In this case, a new file in the staging area will correctly show as added because it does not exist in HEAD.
        diffs = repo.index.diff("HEAD", R=True)

        for diff in diffs:
            if diff.change_type in ["A", "M"] and diff.a_path.endswith(".py"):
                is_new_file = diff.change_type == "A"
                staged_files[diff.a_path] = is_new_file

        return staged_files


    def get_file_diff(self, file_path, is_new_file):
        """
        The function's purpose is to retrieve the changes made to a specific file. For new files, it uses git diff --staged to get the differences.
        Args:
            file_path (str): The relative path of the file
            is_new_file (bool): Indicates whether the file is a new file
        Returns:
            list: List of changes made to the file
        """
        repo = self.repo

        if is_new_file:
            # For new files, first add them to the staging area.
            add_command = f'git -C {repo.working_dir} add "{file_path}"'
            subprocess.run(add_command, shell=True, check=True)

            # Get the diff from the staging area.
            diffs = repo.git.diff("--staged", file_path).splitlines()
        else:
            # For non-new files, get the diff from HEAD.
            diffs = repo.git.diff("HEAD", file_path).splitlines()

        return diffs

    def parse_diffs(self, diffs):
        """
        Parse the difference content, extract the added and deleted object information, the object can be a class or a function.
        Output example: {'added': [(86, '    '), (87, '    def to_json_new(self, comments = True):'), (88, '        data = {'), (89, '            "name": self.node_name,')...(95, '')], 'removed': []}
        In the above example, PipelineEngine and AI_give_params are added objects, and there are no deleted objects.
        But the addition here does not mean that it is a newly added object, because in git diff, the modification of a line is represented as deletion and addition in diff.
        So for the modified content, it will also be represented as this object has undergone an added operation.

        If you need to know clearly that an object is newly added, you need to use the get_added_objs() function.
        Args:
            diffs (list): A list containing difference content. Obtained by the get_file_diff() function inside the class.

        Returns:
            dict: A dictionary containing added and deleted line information, the format is {'added': set(), 'removed': set()}
        """
        changed_lines = {"added": [], "removed": []}
        line_number_current = 0
        line_number_change = 0

        for line in diffs:
            # 检测行号信息，例如 "@@ -43,33 +43,40 @@"
            line_number_info = re.match(r"@@ \-(\d+),\d+ \+(\d+),\d+ @@", line)
            if line_number_info:
                line_number_current = int(line_number_info.group(1))
                line_number_change = int(line_number_info.group(2))
                continue

            if line.startswith("+") and not line.startswith("+++"):
                changed_lines["added"].append((line_number_change, line[1:]))
                line_number_change += 1
            elif line.startswith("-") and not line.startswith("---"):
                changed_lines["removed"].append((line_number_current, line[1:]))
                line_number_current += 1
            else:
                # 对于没有变化的行，两者的行号都需要增加
                line_number_current += 1
                line_number_change += 1

        return changed_lines
    
    
    # TODO: The key issue is that the changed line numbers correspond to the old function names (i.e., those removed) and the new function names (i.e., those added), and the current implementation does not handle this correctly.
    # We need a way to associate the changed line numbers with their function or class names before and after the change. One method is to build a mapping before processing changed_lines, which can map the names after the change back to the names before the change based on the line number.
    # Then, in the identify_changes_in_structure function, this mapping can be used to correctly identify the changed structure.
    def identify_changes_in_structure(self, changed_lines, structures):
        """
        Identify the structure of the function or class where changes have occurred: Traverse all changed lines, for each line, it checks whether this line is between the start line and the end line of a structure (function or class).
        If so, then this structure is considered to have changed, and its name and the name of the parent structure are added to the corresponding set in the result dictionary changes_in_structures (depending on whether this line is added or deleted).

        Output example: {'added': {('PipelineAutoMatNode', None), ('to_json_new', 'PipelineAutoMatNode')}, 'removed': set()}

        Args:
            changed_lines (dict): A dictionary containing the line numbers where changes have occurred, {'added': [(line number, change content)], 'removed': [(line number, change content)]}
            structures (list): The received is a list of function or class structures from get_functions_and_classes, each structure is composed of structure type, name, start line number, end line number, and parent structure name.

        Returns:
            dict: A dictionary containing the structures where changes have occurred, the key is the change type, and the value is a set of structure names and parent structure names.
                Possible change types are 'added' (new) and 'removed' (removed).
        """
        changes_in_structures = {"added": set(), "removed": set()}
        for change_type, lines in changed_lines.items():
            for line_number, _ in lines:
                for (
                    structure_type,
                    name,
                    start_line,
                    end_line,
                    parent_structure,
                ) in structures:
                    if start_line <= line_number <= end_line:
                        changes_in_structures[change_type].add((name, parent_structure))
        return changes_in_structures
    
    # TODO:可能有错，需要单元测试覆盖； 可能有更好的实现方式
    def get_to_be_staged_files(self):
        """
        This method retrieves all unstaged files in the repository that meet one of the following conditions:
        1. The file, when its extension is changed to .md, corresponds to a file that is already staged.
        2. The file's path is the same as the 'project_hierarchy' field in the CONFIG.

        It returns a list of the paths of these files.

        :return: A list of relative file paths to the repo that are either modified but not staged, or untracked, and meet one of the conditions above.
        """
        # 已经更改但是暂未暂存的文件，这里只能是.md文件，因为作者不提交的.py文件（即使发生变更）我们不做处理。
        to_be_staged_files = []
        # staged_files是已经暂存的文件，通常这里是作者做了更改后git add 的.py文件 或其他文件
        staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
        print(f"staged_files:{staged_files}")

        project_hierarchy = CONFIG['project_hierarchy']
        # diffs是所有未暂存更改文件的列表。这些更改文件是相对于工作区（working directory）的，也就是说，它们是自上次提交（commit）以来在工作区发生的更改，但还没有被添加到暂存区（staging area）
        # 比如原本存在的md文件现在由于代码的变更发生了更新，就会标记为未暂存diff
        diffs = self.repo.index.diff(None)
        # untracked_files是一个包含了所有未跟踪文件的列表。比如说用户添加了新的.py文件后项目自己生成的对应.md文档。它们是在工作区中存在但还没有被添加到暂存区（staging area）的文件。
        # untracked_files中的文件路径是绝对路径
        untracked_files = self.repo.untracked_files
        print(f"untracked_files:{untracked_files}")
        print(f"repo_path:{self.repo_path}")

        # 处理untrack_files中的内容
        for untracked_file in untracked_files:
            # 连接repo_path和untracked_file以获取完整的绝对路径
            abs_untracked_file = os.path.join(self.repo_path, '/'+untracked_file)
            # 获取相对于仓库根目录的相对路径
            rel_untracked_file = os.path.relpath(abs_untracked_file, self.repo_path)
            print(f"rel_untracked_file:{rel_untracked_file}")

            # 判断这个文件的类型：
            if rel_untracked_file.endswith('.md'):
                # 把rel_untracked_file从CONFIG['Markdown_Docs_folder']中拆离出来。判断是否能跟暂存区中的某一个.py文件对应上
                rel_untracked_file = os.path.relpath(rel_untracked_file, CONFIG['Markdown_Docs_folder'])
                corresponding_py_file = os.path.splitext(rel_untracked_file)[0] + '.py'
                print(f"corresponding_py_file in untracked_files:{corresponding_py_file}")
                if corresponding_py_file in staged_files:
                    # 如果是，那么就把这个md文件也加入到unstaged_files中
                    to_be_staged_files.append(os.path.join(self.repo_path.lstrip('/'), CONFIG['Markdown_Docs_folder'], rel_untracked_file))
            elif rel_untracked_file == project_hierarchy:
                to_be_staged_files.append(rel_untracked_file) 

        # 处理已追踪但是未暂存的内容
        unstaged_files = [diff.b_path for diff in diffs]
        print(f"unstaged_files:{unstaged_files}") # 虽然是从根目录开始的，但是最前头缺少一个 ' / ' ，所以还是会被解析为相对路径
        for unstaged_file in unstaged_files:
            # 连接repo_path和unstaged_file以获取完整的绝对路径
            abs_unstaged_file = os.path.join(self.repo_path, '/'+unstaged_file)
            # 获取相对于仓库根目录的相对路径
            rel_unstaged_file = os.path.relpath(abs_unstaged_file, self.repo_path)
            print(f"rel_unstaged_file:{rel_unstaged_file}")
            # 如果它是md文件
            if unstaged_file.endswith('.md'):
                # 把rel_unstaged_file从CONFIG['Markdown_Docs_folder']中拆离出来。判断是否能跟暂存区中的某一个.py文件对应上
                rel_unstaged_file = os.path.relpath(rel_unstaged_file, CONFIG['Markdown_Docs_folder'])
                corresponding_py_file = os.path.splitext(rel_unstaged_file)[0] + '.py'
                print(f"corresponding_py_file:{corresponding_py_file}")
                if corresponding_py_file in staged_files:
                    # 如果是，那么就把这个md文件也加入到unstaged_files中
                    to_be_staged_files.append(os.path.join(self.repo_path.lstrip('/'), CONFIG['Markdown_Docs_folder'], rel_unstaged_file))
            elif unstaged_file == project_hierarchy:
                to_be_staged_files.append(unstaged_file) 

        return to_be_staged_files

    
    def add_unstaged_files(self):
        """
        Add unstaged files which meet the condition to the staging area.
        """
        unstaged_files_meeting_conditions = self.get_to_be_staged_files()
        for file_path in unstaged_files_meeting_conditions:
            add_command = f'git -C {self.repo.working_dir} add "{file_path}"'
            subprocess.run(add_command, shell=True, check=True)
        return unstaged_files_meeting_conditions
    
    
if __name__ == "__main__":

    repo_path = "/path/to/your/repo/"
    change_detector = ChangeDetector(repo_path)
    changed_files = change_detector.get_staged_pys()
    print(f"\nchanged_files:{changed_files}\n\n")
    for file_path, is_new_file in changed_files.items():
        changed_lines = change_detector.parse_diffs(
            change_detector.get_file_diff(file_path, is_new_file)
        )
        # print("changed_lines:",changed_lines)
        file_handler = FileHandler(repo_path=repo_path, file_path=file_path)
        changes_in_pyfile = change_detector.identify_changes_in_structure(
            changed_lines,
            file_handler.get_functions_and_classes(file_handler.read_file()),
        )
        print(f"Changes in {file_path} Structures:{changes_in_pyfile}\n")
