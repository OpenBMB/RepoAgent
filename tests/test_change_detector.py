import unittest
import os
from repo_agent.change_detector import ChangeDetector
from git import Repo

class TestChangeDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 定义测试仓库的路径
        cls.test_repo_path = os.path.join(os.path.dirname(__file__), 'test_repo')

        # 如果测试仓库文件夹不存在，则创建它
        if not os.path.exists(cls.test_repo_path):
            os.makedirs(cls.test_repo_path)

        # 初始化 Git 仓库
        cls.repo = Repo.init(cls.test_repo_path)

        # 配置 Git 用户信息
        cls.repo.git.config('user.email', 'ci@example.com')
        cls.repo.git.config('user.name', 'CI User')

        # 创建一些测试文件
        with open(os.path.join(cls.test_repo_path, 'test_file.py'), 'w') as f:
            f.write('print("Hello, Python")')
        
        with open(os.path.join(cls.test_repo_path, 'test_file.md'), 'w') as f:
            f.write('# Hello, Markdown')

        # 模拟 Git 操作：添加和提交文件
        cls.repo.git.add(A=True)
        cls.repo.git.commit('-m', 'Initial commit')

    def test_get_staged_pys(self):
        # 创建一个新的 Python 文件并暂存
        new_py_file = os.path.join(self.test_repo_path, 'new_test_file.py')
        with open(new_py_file, 'w') as f:
            f.write('print("New Python File")')
        self.repo.git.add(new_py_file)

        # 使用 ChangeDetector 检查暂存文件
        change_detector = ChangeDetector(self.test_repo_path)
        staged_files = change_detector.get_staged_pys()

        # 断言新文件在暂存文件列表中
        self.assertIn('new_test_file.py', [os.path.basename(path) for path in staged_files])

        print(f"\ntest_get_staged_pys: Staged Python files: {staged_files}")


    def test_get_unstaged_mds(self):
        # 修改一个 Markdown 文件但不暂存
        md_file = os.path.join(self.test_repo_path, 'test_file.md')
        with open(md_file, 'a') as f:
            f.write('\nAdditional Markdown content')

        # 使用 ChangeDetector 获取未暂存的 Markdown 文件
        change_detector = ChangeDetector(self.test_repo_path)
        unstaged_files = change_detector.get_to_be_staged_files()

        # 断言修改的文件在未暂存文件列表中
        self.assertIn('test_file.md', [os.path.basename(path) for path in unstaged_files])

        print(f"\ntest_get_unstaged_mds: Unstaged Markdown files: {unstaged_files}")


    def test_add_unstaged_mds(self):
        # 确保有一个未暂存的 Markdown 文件
        self.test_get_unstaged_mds()

        # 使用 ChangeDetector 添加未暂存的 Markdown 文件
        change_detector = ChangeDetector(self.test_repo_path)
        change_detector.add_unstaged_files()

        # 检查文件是否被暂存
        unstaged_files_after_add = change_detector.get_to_be_staged_files()

        # 断言暂存操作后没有未暂存的 Markdown 文件
        self.assertEqual(len(unstaged_files_after_add), 0)

        remaining_unstaged_files = len(unstaged_files_after_add)
        print(f"\ntest_add_unstaged_mds: Number of remaining unstaged Markdown files after add: {remaining_unstaged_files}")


    @classmethod
    def tearDownClass(cls):
        # 清理测试仓库
        cls.repo.close()
        os.system('rm -rf ' + cls.test_repo_path)

if __name__ == '__main__':
    unittest.main()
