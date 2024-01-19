## _class TestChangeDetector
**TestChangeDetector**: TestChangeDetector的功能是执行一系列的测试用例，用于测试ChangeDetector类的各个方法。

**属性**: 
- test_repo_path: 测试仓库的路径
- repo: Git仓库对象

**代码描述**: 
TestChangeDetector是一个继承自unittest.TestCase的测试类，用于测试ChangeDetector类的各个方法。在setUpClass()方法中，首先定义了测试仓库的路径，并创建了测试仓库文件夹。然后，初始化了Git仓库，并配置了Git用户信息。接下来，创建了一些测试文件，并使用Git操作将文件添加和提交到仓库中。

在test_get_staged_pys()方法中，首先创建了一个新的Python文件并暂存，然后使用ChangeDetector类检查暂存文件，并断言新文件在暂存文件列表中。

在test_get_unstaged_mds()方法中，修改了一个Markdown文件但不暂存，然后使用ChangeDetector类获取未暂存的Markdown文件，并断言修改的文件在未暂存文件列表中。

在test_add_unstaged_mds()方法中，首先调用了test_get_unstaged_mds()方法，确保有一个未暂存的Markdown文件。然后使用ChangeDetector类添加未暂存的Markdown文件，并检查文件是否被暂存。

在tearDownClass()方法中，清理了测试仓库。

**注意**: 
- 在使用TestChangeDetector类之前，需要先安装并导入unittest和os模块。
- 在执行测试用例之前，需要确保已经安装了Git，并配置了正确的Git用户信息。
- 在执行测试用例之后，可以调用tearDownClass()方法清理测试仓库。
### _class_function setUpClass(cls)
**setUpClass**: setUpClass函数的功能是在测试类中设置一些类级别的变量和操作。

**参数**: cls (类对象) - 表示当前测试类的类对象。

**代码描述**: setUpClass函数首先定义了一个测试仓库的路径，该路径是当前文件所在目录下的test_repo文件夹。然后，如果测试仓库文件夹不存在，则创建它。接下来，使用Repo.init方法初始化了一个Git仓库，并使用repo.git.config方法配置了Git用户信息。然后，创建了两个测试文件test_file.py和test_file.md，并向其中分别写入了一些内容。最后，使用repo.git.add和repo.git.commit方法模拟了Git操作，将文件添加和提交到仓库中。

**注意**: 在使用setUpClass函数之前，需要确保已经创建了测试仓库，并且在测试仓库中存在test_file.md文件。
### _class_function test_get_staged_pys(self)
**test_get_staged_pys**: test_get_staged_pys函数的功能是获取暂存的Python文件。
**参数**: 该函数没有参数。
**代码描述**: 该函数首先创建一个新的Python文件并将其暂存。然后，使用ChangeDetector类检查暂存文件，并将结果保存在staged_files变量中。最后，断言新文件在暂存文件列表中，并打印出暂存的Python文件列表。
**注意**: 在使用该函数之前，需要确保已经初始化了test_repo_path变量，并且已经导入了os和ChangeDetector类。
### _class_function test_get_unstaged_mds(self)
**test_get_unstaged_mds**: test_get_unstaged_mds函数的功能是获取未暂存的Markdown文件。
**参数**: 该函数没有参数。
**代码描述**: 该函数首先在测试仓库中创建一个Markdown文件，并向其中添加额外的内容。然后，使用ChangeDetector类获取未暂存的文件列表。最后，断言修改的文件在未暂存文件列表中，并打印出未暂存的Markdown文件列表。
**注意**: 使用该函数前需要确保已经创建了测试仓库，并且在测试仓库中存在test_file.md文件。
### _class_function test_add_unstaged_mds(self)
**test_add_unstaged_mds**: test_add_unstaged_mds函数的功能是将未暂存的Markdown文件添加到暂存区。
**参数**: 该函数没有参数。
**代码描述**: 该函数首先调用test_get_unstaged_mds函数，确保存在一个未暂存的Markdown文件。然后，使用ChangeDetector类创建一个change_detector对象，并将未暂存的文件添加到暂存区。接着，通过调用change_detector对象的get_to_be_staged_files函数，获取暂存操作后的未暂存文件列表。最后，使用self.assertEqual函数断言暂存操作后的未暂存文件列表长度为0。此外，函数还打印了暂存操作后剩余的未暂存Markdown文件数。
**注意**: 在使用该函数之前，需要确保存在未暂存的Markdown文件。
### _class_function tearDownClass(cls)
**tearDownClass**: tearDownClass函数的作用是清理测试类的资源。
**参数**: cls - 类方法的第一个参数，表示当前类。
**代码描述**: tearDownClass函数用于清理测试类的资源。在函数内部，首先调用cls.repo.close()关闭测试仓库，然后使用os.system('rm -rf ' + cls.test_repo_path)命令删除测试仓库的路径。
**注意**: 使用该函数时需要确保已经创建了测试仓库，并且在测试类的最后调用该函数以释放资源。
