import os

import jedi


class ProjectManager:
    def __init__(self, repo_path, project_hierarchy):
        self.repo_path = repo_path
        self.project = jedi.Project(self.repo_path)
        self.project_hierarchy = os.path.join(
            self.repo_path, project_hierarchy, "project_hierarchy.json"
        )

    def get_project_structure(self):
            """
            Returns the structure of the project by recursively walking through the directory tree.

            Returns:
                str: The project structure as a string.
            """
            def walk_dir(root, prefix=""):
                structure.append(prefix + os.path.basename(root))
                new_prefix = prefix + "  "
                for name in sorted(os.listdir(root)):
                    if name.startswith("."):  # 忽略隐藏文件和目录
                        continue
                    path = os.path.join(root, name)
                    if os.path.isdir(path):
                        walk_dir(path, new_prefix)
                    elif os.path.isfile(path) and name.endswith(".py"):
                        structure.append(new_prefix + name)

            structure = []
            walk_dir(self.repo_path)
            return "\n".join(structure)
    
    def build_path_tree(self, who_reference_me, reference_who, doc_item_path):
        from collections import defaultdict

        def tree():
            return defaultdict(tree)

        path_tree = tree()

        # 构建 who_reference_me 和 reference_who 的树
        for path_list in [who_reference_me, reference_who]:
            for path in path_list:
                parts = path.split(os.sep)
                node = path_tree
                for part in parts:
                    node = node[part]

        # 处理 doc_item_path
        parts = doc_item_path.split(os.sep)
        parts[-1] = "✳️" + parts[-1]  # 在最后一个对象前面加上星号
        node = path_tree
        for part in parts:
            node = node[part]

        def tree_to_string(tree, indent=0):
            s = ""
            for key, value in sorted(tree.items()):
                s += "    " * indent + key + "\n"
                if isinstance(value, dict):
                    s += tree_to_string(value, indent + 1)
            return s

        return tree_to_string(path_tree)


if __name__ == "__main__":
    project_manager = ProjectManager(repo_path="", project_hierarchy="")
    print(project_manager.get_project_structure())
