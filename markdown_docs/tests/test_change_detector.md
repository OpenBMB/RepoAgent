## _class TestChangeDetector
Doc has not been generated...
### _function setUpClass(cls)
**setUpClass**: setUpClass函数的作用是设置测试类的初始状态。

**参数**：这个函数的参数。
· cls：表示类本身的参数。

**代码描述**：setUpClass函数用于设置测试类的初始状态。在这个函数中，首先定义了测试仓库的路径，通过os.path.join函数将当前文件所在目录与'test_repo'拼接起来得到测试仓库的路径。然后，通过判断测试仓库文件夹是否存在，如果不存在则创建它。接下来，使用Repo.init函数初始化Git仓库，并使用repo.git.config函数配置Git用户信息，设置用户邮箱为'ci@example.com'，用户名为'CI User'。然后，使用open函数创建两个测试文件，分别是'test_file.py'和'ttest_file.md'，并分别写入'print("Hello, Python")'和'# Hello, Markdown'的内容。最后，模拟Git操作，使用repo.git.add函数将文件添加到Git仓库中，再使用repo.git.commit函数提交文件到Git仓库。

**注意**：在使用setUpClass函数之前，需要确保已经导入了os和Repo模块。另外，setUpClass函数只会在整个测试类执行之前执行一次，用于设置测试类的初始状态。
### _function test_get_staged_pys(self)
Doc has not been generated...
### _function test_get_unstaged_mds(self)
Doc has not been generated...
### _function test_add_unstaged_mds(self)
Doc has not been generated...
### _class_function tearDownClass(cls)
**tearDownClass**: tearDownClass函数的作用是清理测试类的资源。

**参数**：
· cls：类方法的第一个参数，表示当前类的引用。

**代码说明**：
tearDownClass函数用于清理测试类的资源。在该函数中，首先调用cls.repo.close()关闭测试仓库，然后使用os.system('rm -rf ' + cls.test_repo_path)命令删除测试仓库的文件。

**注意**：
- tearDownClass函数应该在测试类的所有测试方法执行完毕后调用，用于清理测试类的资源。
- 在调用tearDownClass函数之前，需要确保测试仓库已经创建并且测试类的相关资源已经初始化。
- 调用tearDownClass函数后，测试类的资源将被清理，不再可用。
