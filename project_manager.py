class ProjectManager:
    def __init__(self, repo_path=None):
        # 初始化时需要指定仓库的路径
        self.repo_path = repo_path or self.get_default_repo_path()

    def get_default_repo_path(self):

        return "/Users/logic/Documents/VisualStudioWorkspace/XAgent-Dev/"
