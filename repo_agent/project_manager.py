import os
import jedi

class ProjectManager:
    def __init__(self, repo_path, project_hierarchy):
        self.repo_path = repo_path
        self.project = jedi.Project(self.repo_path)
        self.project_hierarchy = os.path.join(self.repo_path, project_hierarchy, ".project_hierarchy.json")

    def get_project_structure(self):
        def walk_dir(root, prefix=""):
            structure.append(prefix + os.path.basename(root))
            new_prefix = prefix + "  "
            for name in sorted(os.listdir(root)):
                if name.startswith('.'):  # 忽略隐藏文件和目录
                    continue
                path = os.path.join(root, name)
                if os.path.isdir(path):
                    walk_dir(path, new_prefix)
                elif os.path.isfile(path) and name.endswith('.py'):
                    structure.append(new_prefix + name)

        structure = []
        walk_dir(self.repo_path)
        return '\n'.join(structure)
    
    def find_all_referencer(self, variable_name, file_path, line_number, column_number):
        """
        Find all references of a variable in a given file.

        Args:
            variable_name (str): The name of the variable to search for.
            file_path (str): The path of the file to search in.
            line_number (int): The line number where the variable is located.
            column_number (int): The column number where the variable is located.

        Returns:
            list: A list of tuples containing the file path, line number, and column number of each reference.
        
        """
        script = jedi.Script(path=os.path.join(self.repo_path, file_path))
        references = script.get_references(line=line_number, column=column_number)

        try:
            # Filter out references with variable_name and return their positions
            variable_references = [ref for ref in references if ref.name == variable_name]
            return [(os.path.relpath(ref.module_path, self.repo_path), ref.line, ref.column) for ref in variable_references if not (ref.line == line_number and ref.column == column_number)]
        except Exception as e:
            # Print error message and related parameters
            print(f"Error occurred: {e}")
            print(f"Parameters: variable_name={variable_name}, file_path={file_path}, line_number={line_number}, column_number={column_number}")
            return []
    
if __name__ == "__main__":
    project_manager = ProjectManager(repo_path="",project_hierarchy="")
    print(project_manager.get_project_structure())