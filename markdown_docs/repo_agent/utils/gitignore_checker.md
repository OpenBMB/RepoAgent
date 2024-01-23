## _class GitignoreChecker
**GitignoreChecker**: GitignoreChecker的功能是检查文件和文件夹是否被.gitignore文件忽略。

**属性**: 
- directory (str): 要检查的目录路径。
- gitignore_path (str): .gitignore文件的路径。
- folder_patterns (list): 从.gitignore文件中提取的文件夹模式列表。
- file_patterns (list): 从.gitignore文件中提取的文件模式列表。

**代码描述**: 
GitignoreChecker类用于检查文件和文件夹是否被.gitignore文件忽略。在初始化时，需要指定要检查的目录路径和.gitignore文件的路径。该类会加载并解析.gitignore文件，并将模式分为文件夹模式和文件模式。然后，通过check_files_and_folders方法，可以检查给定目录中的所有文件和文件夹是否被忽略，并返回未被忽略且具有.py扩展名的文件路径列表。

**注意**: 
- 在初始化GitignoreChecker对象时，需要提供正确的目录路径和.gitignore文件的路径。
- .gitignore文件中的模式可以是文件夹模式（以/结尾）或文件模式。
- check_files_and_folders方法返回的文件路径是相对于指定目录路径的相对路径。

**输出示例**: 
```python
gitignore_checker = GitignoreChecker(directory='/path/to/directory', gitignore_path='/path/to/.gitignore')
not_ignored_files = gitignore_checker.check_files_and_folders()
print(not_ignored_files)
# Output: ['file1.py', 'file2.py', 'folder/file3.py']
```
### _class_function __init__(self, directory, gitignore_path)
**__init__**: __init__函数的功能是使用特定的目录和.gitignore文件的路径来初始化GitignoreChecker。

**参数**: 
- directory (str): 要检查的目录。
- gitignore_path (str): .gitignore文件的路径。

**代码描述**: 
该函数首先将传入的directory和gitignore_path赋值给self.directory和self.gitignore_path属性。然后，函数调用self._load_gitignore_patterns()方法来加载和解析.gitignore文件，并将解析后的模式分别赋值给self.folder_patterns和self.file_patterns属性。

**注意**: 
- 使用这段代码时需要确保传入的directory和gitignore_path参数是有效的字符串。
- 函数假设_load_gitignore_patterns方法已经定义并可用。


### _class_function _load_gitignore_patterns(self)
**_load_gitignore_patterns**: _load_gitignore_patterns函数的功能是加载和解析.gitignore文件，然后将模式分割为文件夹模式和文件模式。

**参数**: 该函数没有接受任何参数。

**代码描述**: 该函数首先尝试使用指定的.gitignore文件路径打开文件，并读取文件内容。如果文件不存在，则会回退到默认路径。然后，函数调用_parse_gitignore函数解析gitignore_content，并将解析后的模式传递给_split_gitignore_patterns函数进行分割。最后，函数返回一个包含文件夹模式列表和文件模式列表的元组。

**注意**: 使用这段代码时需要注意以下几点：
- 函数假设传入的gitignore_path参数是有效的.gitignore文件路径。
- 函数假设_parse_gitignore和_split_gitignore_patterns函数已经定义并可用。

**输出示例**: 假设.gitignore文件的内容为：
```
# 忽略以.pyc结尾的文件
*.pyc

# 忽略名为__pycache__的目录
__pycache__
```
则函数的返回值为(['__pycache__'], ['*.pyc'])。
### _class_function _parse_gitignore(gitignore_content)
**_parse_gitignore**: _parse_gitignore函数的功能是解析.gitignore文件的内容，并将模式作为列表返回。
**参数**: gitignore_content (str) - .gitignore文件的内容。
**代码描述**: 该函数通过遍历.gitignore文件的每一行，将非空且不以'#'开头的行作为模式添加到列表中，并返回该列表。
**注意**: 该函数假设传入的gitignore_content参数是有效的.gitignore文件内容。
**输出示例**: 
```python
gitignore_content = """
# Ignore files with .pyc extension
*.pyc

# Ignore directories named __pycache__
__pycache__
"""

_parse_gitignore(gitignore_content)
# Output: ['*.pyc', '__pycache__']
```
### _class_function _split_gitignore_patterns(gitignore_patterns)
**_split_gitignore_patterns**: _split_gitignore_patterns函数的功能是将.gitignore模式分割为文件夹模式和文件模式。
**参数**: 这个函数的参数是gitignore_patterns，一个包含.gitignore文件中的模式的列表。
**代码描述**: 这个函数首先创建两个空列表，folder_patterns和file_patterns，用于存储文件夹模式和文件模式。然后，它遍历gitignore_patterns列表中的每个模式。如果模式以'/'结尾，说明它是文件夹模式，将其去除末尾的'/'后添加到folder_patterns列表中；否则，说明它是文件模式，直接将其添加到file_patterns列表中。最后，函数返回一个包含folder_patterns和file_patterns的元组。
**注意**: 使用这段代码时需要注意以下几点：
- gitignore_patterns参数必须是一个包含.gitignore模式的列表。
- 函数返回的元组包含两个列表，一个是文件夹模式列表，一个是文件模式列表。
**输出示例**: 假设gitignore_patterns为['folder/', 'file.txt']，则函数的返回值为(['folder'], ['file.txt'])。
### _class_function _is_ignored(path, patterns, is_dir)
**_is_ignored**: _is_ignored函数的功能是检查给定的路径是否与任何模式匹配。
**参数**: 这个函数的参数。
- path (str): 要检查的路径。
- patterns (list): 要检查的模式列表。
- is_dir (bool): 如果路径是目录，则为True；否则为False。
**代码说明**: 这个函数使用给定的模式列表逐个检查路径。如果路径与任何模式匹配，则返回True；否则返回False。
- 首先，对于每个模式，使用fnmatch模块的fnmatch函数检查路径是否与模式匹配。
- 如果is_dir为True，并且模式以'/'结尾，并且路径与去掉最后一个字符的模式匹配，则返回True。
- 如果没有匹配的模式，则返回False。
**注意**: 使用该代码时需要注意以下几点：
- patterns参数应该是一个包含模式的列表。
- path参数应该是一个字符串，表示要检查的路径。
- is_dir参数是一个布尔值，用于指示路径是否是一个目录。
**输出示例**: 模拟代码返回值的可能外观。
- 如果路径与模式匹配，则返回True。
- 如果路径与模式不匹配，则返回False。
### _class_function check_files_and_folders(self)
**check_files_and_folders**: check_files_and_folders函数的功能是检查给定目录中的所有文件和文件夹是否与分割的gitignore模式匹配。返回一个列表，其中包含未被忽略且具有'.py'扩展名的文件的路径。返回的文件路径是相对于self.directory的。

**参数**: 这个函数的参数。
- 无

**代码说明**: 这个函数使用os.walk函数遍历给定目录中的所有文件和文件夹。对于每个文件和文件夹，它执行以下操作：
- 使用self._is_ignored函数检查文件夹是否被忽略。如果文件夹不被忽略，则将其添加到dirs列表中。
- 对于每个文件，它执行以下操作：
  - 使用self._is_ignored函数检查文件是否被忽略，并且文件扩展名以'.py'结尾。如果文件不被忽略且具有'.py'扩展名，则将其添加到not_ignored_files列表中。

**注意**: 使用该代码时需要注意以下几点：
- 该函数依赖于self._is_ignored函数，因此在调用该函数之前，需要确保self._is_ignored函数已经定义并可用。
- self.directory应该是一个字符串，表示要检查的目录路径。

**输出示例**: 模拟代码返回值的可能外观。
- ['/path/to/file1.py', '/path/to/file2.py', ...]
