import os
import git 

class DataAquire:
    def __init__(self, directory):
        self.directory = directory
    def build_tree(self,files):
        tree = {}
        for file in files:
            parts = file.split('/')
            node = tree
            for part in parts:
                if part not in node:
                    node[part] = {}
                node = node[part]
        return tree

    def build_tree_string(self,node, prefix=''):
        tree_str = ''
        if not isinstance(node, dict) or not node:
            return tree_str

        last_key = list(node.keys())[-1]
        for key in node:
            connector = '└── ' if key == last_key else '├── '
            tree_str += prefix + connector + key + '\n'
            if isinstance(node[key], dict):
                extension = '    ' if key == last_key else '│   '
                tree_str += self.build_tree_string(node[key], prefix=prefix + extension)

        return tree_str
    def extract_requirements(self):
        path = os.path.join(self.directory, 'requirements.txt')
        if os.path.isfile(path):
            with open(path, 'r',encoding = "utf-8") as file:
                return file.read()
        return "无法找到 requirements.txt"

    def extract_config_guide(self):
        path = os.path.join(self.directory, 'config.yml')
        if os.path.isfile(path):
            with open(path, 'r',encoding = "utf-8") as file:
                return file.read()
        return "无法找到 config.yml"


    def extract_license(self):
        path = os.path.join(self.directory, 'LICENSE')
        if os.path.isfile(path):
            with open(path, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                # 仅选择前7行
                useful_lines = lines[:7]
                return ''.join(useful_lines)
        return "无法找到 LICENSE 文件"


    def top5(self):
        repo = git.Repo(self.directory)
        info={}
        info['commits'] = [{'commit': commit.hexsha, 'message': commit.message.strip()} for commit in repo.iter_commits()]
        top_five_messages =  [msg['message'] for msg in info['commits'][:5]]
        return top_five_messages

    def summaryinfo(self):
        with open('./compressmd/summary.md', 'r', encoding = "utf-8") as f:
            summary = f.read()
        return summary

    def tree(self):
        repo = git.Repo(self.directory)
        files = [item.path for item in repo.tree().traverse()]
        tree_string = self.build_tree_string(self.build_tree(files))
        return tree_string

if __name__ == '__main__':
    path="../../"
    data =DataAquire(path)
    print(data.summaryinfo())
