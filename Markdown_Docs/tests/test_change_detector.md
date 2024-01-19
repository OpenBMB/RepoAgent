# ClassDef TestChangeDetector:
**TestChangeDetector**: TestChangeDetector的功能是执行一系列的测试用例，用于测试ChangeDetector类的各个方法。

**属性**: 
- test_repo_path: 测试仓库的路径
- repo: Git仓库对象

**代码描述**: 
TestChangeDetector是一个继承自unittest.TestCase的测试类，用于测试ChangeDetector类的各个方法。在setUpClass方法中，首先定义了测试仓库的路径，并创建了该路径下的测试仓库文件夹。然后，初始化了一个Git仓库，并配置了Git用户信息。接下来，创建了两个测试文件test_file.py和test_file.md，并使用Git操作将它们添加和提交到仓库中。

在test_get_staged_pys方法中，首先创建了一个新的Python文件new_test_file.py，并将其暂存到Git仓库中。然后，使用ChangeDetector类检查暂存的Python文件，并断言新文件在暂存文件列表中。

在test_get_unstaged_mds方法中，修改了一个Markdown文件但不暂存。然后，使用ChangeDetector类获取未暂存的Markdown文件，并断言修改的文件在未暂存文件列表中。

在test_add_unstaged_mds方法中，首先调用了test_get_unstaged_mds方法，确保有一个未暂存的Markdown文件。然后，使用ChangeDetector类添加未暂存的Markdown文件，并检查文件是否被暂存。最后，断言暂存操作后没有未暂存的Markdown文件。

在tearDownClass方法中，清理了测试仓库。

**注意**: 
- 在使用TestChangeDetector类之前，需要先安装Git和GitPython库。
- 在运行测试用例之前，需要确保测试仓库的路径存在且为空。
## FunctionDef setUpClass(cls):
**setUpClass**: setUpClass函数的功能是在测试类的所有测试方法执行之前进行一次性的设置。

**参数**: cls (类对象) - 表示测试类本身。

**代码描述**: setUpClass函数首先定义了测试仓库的路径，通过os.path.join方法将当前文件的目录路径与'test_repo'拼接起来。然后，通过os.path.exists方法判断测试仓库文件夹是否存在，如果不存在，则使用os.makedirs方法创建该文件夹。接下来，使用Repo.init方法初始化Git仓库，将测试仓库路径作为参数传入。然后，使用repo.git.config方法配置Git用户信息，将'user.email'和'user.name'分别设置为'ci@example.com'和'CI User'。接着，使用open方法创建两个测试文件，分别是'test_file.py'和'test_file.md'，并向其中写入内容。然后，使用repo.git.add方法将文件添加到暂存区。最后，使用repo.git.commit方法提交文件到仓库，参数'-m'表示提交信息，这里设置为'Initial commit'。

**注意**: 在使用该函数之前，需要确保已经初始化了测试仓库，并且测试仓库中存在'test_file.md'文件。
## FunctionDef test_get_staged_pys(self):
**test_get_staged_pys**: test_get_staged_pys函数的功能是获取暂存的Python文件。
**参数**: 该函数没有参数。
**代码描述**: 这个函数的作用是创建一个新的Python文件并将其暂存，然后使用ChangeDetector检查暂存的文件，并断言新文件在暂存文件列表中。
首先，函数会创建一个新的Python文件并将其暂存。它通过使用os模块的join函数将新文件的路径与测试仓库路径拼接起来，并将文件名命名为'new_test_file.py'。然后，它使用open函数以写入模式打开文件，并将字符串'print("New Python File")'写入文件中。接下来，函数使用repo对象的git属性的add方法将新文件添加到暂存区中。
然后，函数使用ChangeDetector类创建一个change_detector对象，并将测试仓库路径作为参数传递给它。接着，函数调用change_detector对象的get_staged_pys方法，获取暂存的Python文件列表，并将结果赋值给变量staged_files。
最后，函数使用断言语句来验证新文件是否在暂存文件列表中。它使用self.assertIn方法来断言'new_test_file.py'是否在暂存文件列表中的文件名中。如果断言成功，则打印出暂存的Python文件列表。
**注意**: 使用该函数前需要确保已经导入了os模块和ChangeDetector类，并且已经创建了一个名为test_repo_path的测试仓库路径。
## FunctionDef test_get_unstaged_mds(self):
**test_get_unstaged_mds**: test_get_unstaged_mds函数的功能是获取未暂存的Markdown文件。
**参数**: 该函数没有参数。
**代码说明**: 该函数首先在测试仓库中创建一个Markdown文件，并向其中添加额外的Markdown内容。然后，使用ChangeDetector类获取未暂存的文件列表。最后，通过断言判断修改的文件是否在未暂存文件列表中，并打印出未暂存的Markdown文件列表。
**注意**: 使用该函数前需要确保已经初始化了测试仓库，并且测试仓库中存在test_file.md文件。
## FunctionDef test_add_unstaged_mds(self):
**test_add_unstaged_mds**: test_add_unstaged_mds函数的功能是将未暂存的Markdown文件添加到暂存区。
**参数**: 该函数没有参数。
**代码描述**: 该函数首先调用test_get_unstaged_mds函数，确保存在一个未暂存的Markdown文件。然后，使用ChangeDetector类创建一个change_detector对象，并将未暂存的文件添加到暂存区。接着，通过调用change_detector对象的get_to_be_staged_files函数，获取暂存操作后的未暂存文件列表。最后，使用self.assertEqual函数断言暂存操作后未暂存的Markdown文件数量为0，并打印出剩余未暂存Markdown文件的数量。
**注意**: 使用该函数前，需要确保存在未暂存的Markdown文件。
## FunctionDef tearDownClass(cls):
**tearDownClass**: tearDownClass函数的作用是清理测试类的资源。
**参数**: cls - 测试类的类对象。
**代码描述**: 这个函数用于关闭测试仓库并删除测试仓库的文件。
在函数内部，首先调用cls.repo.close()关闭测试仓库，确保资源被正确释放。然后使用os.system('rm -rf ' + cls.test_repo_path)命令删除测试仓库的文件和文件夹。
**注意**: 使用这个函数时需要确保测试仓库已经被正确关闭，否则可能会导致资源泄露。另外，删除文件和文件夹的操作是不可逆的，请谨慎使用。
***
