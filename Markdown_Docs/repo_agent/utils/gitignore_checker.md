## _class GitignoreChecker
**GitignoreChecker**: GitignoreChecker的功能是检查给定目录下的文件和文件夹是否被.gitignore文件忽略，并返回未被忽略且具有'.py'扩展名的文件路径列表。

**attributes**: 
- directory (str): 要检查的目录路径。
- gitignore_path (str): .gitignore文件的路径。
- folder_patterns (list): 从.gitignore文件中提取的文件夹模式列表。
- file_patterns (list): 从.gitignore文件中提取的文件模式列表。

**Code Description**: 
GitignoreChecker类用于检查给定目录下的文件和文件夹是否被.gitignore文件忽略。在初始化时，需要指定要检查的目录路径和.gitignore文件的路径。如果指定的.gitignore文件不存在，则会回退到默认路径。类中定义了私有方法_load_gitignore_patterns()，用于加载和解析.gitignore文件，并将模式分为文件夹模式和文件模式。还定义了静态方法_parse_gitignore()，用于解析.gitignore文件的内容并返回模式列表。静态方法_split_gitignore_patterns()用于将.gitignore模式分为文件夹模式和文件模式。私有方法_is_ignored()用于检查给定路径是否与模式匹配。check_files_and_folders()方法用于检查给定目录下的所有文件和文件夹，并根据分割的.gitignore模式返回未被忽略且具有'.py'扩展名的文件路径列表。

**Note**: 
- 在初始化GitignoreChecker对象时，需要指定要检查的目录路径和.gitignore文件的路径。
- 如果指定的.gitignore文件不存在，则会回退到默认路径。
- check_files_and_folders()方法返回的文件路径是相对于self.directory的路径。

**Output Example**: 
假设给定目录下有以下文件和文件夹：
- 文件夹1/
- 文件夹2/
- 文件1.py
- 文件2.py
- 文件3.txt

如果.gitignore文件的内容为：
```
文件夹1/
*.txt
```

则check_files_and_folders()方法将返回以下文件路径列表：
```
['文件2.py']
```
### _class_function __init__(self, directory, gitignore_path)
**__init__**: __init__函数的功能是使用特定的目录和.gitignore文件的路径初始化GitignoreChecker。

**参数**: 
- directory (str): 要检查的目录。
- gitignore_path (str): .gitignore文件的路径。

**代码描述**: 
该函数首先将传入的目录和.gitignore文件的路径保存到self.directory和self.gitignore_path属性中。然后，函数调用_load_gitignore_patterns函数加载和解析.gitignore文件的模式，并将结果保存到self.folder_patterns和self.file_patterns属性中。

**注意**: 
在使用该代码时需要注意以下几点：
- 确保.gitignore文件存在于指定的路径或默认路径中。
- 确保.gitignore文件的编码为utf-8。

**输出示例**: 
以下是该函数可能返回的结果示例：
```python
(['folder_pattern1', 'folder_pattern2'], ['file_pattern1', 'file_pattern2'])
```
### _class_function _load_gitignore_patterns(self)
**_load_gitignore_patterns**: _load_gitignore_patterns函数的功能是加载和解析.gitignore文件，然后将模式分割为文件夹模式和文件模式。

**参数**: 该函数没有接受任何参数。

**代码描述**: 该函数首先尝试打开指定的.gitignore文件，并读取文件内容。如果文件不存在，则会回退到默认路径。然后，函数会调用_parse_gitignore函数解析.gitignore文件的内容，得到模式列表。最后，函数会调用_split_gitignore_patterns函数将模式列表分割为文件夹模式和文件模式，并将结果以元组的形式返回。

**注意**: 在使用该代码时需要注意以下几点：
- 确保.gitignore文件存在于指定的路径或默认路径中。
- 确保.gitignore文件的编码为utf-8。

**输出示例**: 以下是该函数可能返回的结果示例：
```python
(['folder_pattern1', 'folder_pattern2'], ['file_pattern1', 'file_pattern2'])
```
### _class_function _parse_gitignore(gitignore_content)
**_parse_gitignore**: _parse_gitignore函数的功能是解析.gitignore文件的内容，并将模式作为列表返回。
**参数**: 这个函数的参数是gitignore_content，表示.gitignore文件的内容，类型为str。
**代码描述**: 这个函数通过遍历gitignore_content的每一行，将不以'#'开头且不为空的行添加到patterns列表中，并返回该列表。
**注意**: 使用这段代码时需要注意以下几点：
- gitignore_content参数必须是一个字符串。
- 返回值是一个列表，其中包含从.gitignore内容中提取出的模式。
**输出示例**: 假设.gitignore文件的内容为：
```
# This is a comment
*.txt
!important.txt
```
则函数的返回值为：['*.txt', '!important.txt']
### _class_function _split_gitignore_patterns(gitignore_patterns)
**_split_gitignore_patterns**: _split_gitignore_patterns函数的功能是将.gitignore模式分割为文件夹模式和文件模式。
**参数**: 这个函数的参数。
- gitignore_patterns (list): 一个包含.gitignore文件中模式的列表。
**代码说明**: 这个函数的功能是将.gitignore模式分割为文件夹模式和文件模式。它接受一个包含.gitignore模式的列表作为输入，并返回两个列表，一个用于文件夹模式，一个用于文件模式。
函数首先创建两个空列表，用于存储文件夹模式和文件模式。然后，它遍历输入的模式列表，并根据模式的结尾字符来判断是文件夹模式还是文件模式。如果模式以'/'结尾，则将其去除'/'后添加到文件夹模式列表中；否则，将其添加到文件模式列表中。最后，函数返回文件夹模式列表和文件模式列表。
**注意**: 使用这段代码时需要注意以下几点：
- 输入的gitignore_patterns参数必须是一个列表。
- 返回值是一个包含两个列表的元组，第一个列表是文件夹模式，第二个列表是文件模式。
**输出示例**: 假设输入的gitignore_patterns为['/folder/', 'file.txt']，则函数的返回值为(['folder'], ['file.txt'])。
### _class_function _is_ignored(path, patterns, is_dir)
**_is_ignored**: _is_ignored函数的功能是检查给定的路径是否与任何模式匹配。
**参数**: 这个函数的参数。
- path (str): 要检查的路径。
- patterns (list): 要检查的模式列表。
- is_dir (bool): 如果路径是目录，则为True；否则为False。
**代码说明**: 这个函数通过遍历模式列表，检查给定的路径是否与任何模式匹配。如果匹配到了任何模式，则返回True；否则返回False。
- 首先，对于每个模式，使用fnmatch模块的fnmatch函数来检查给定的路径是否与模式匹配。
- 如果is_dir为True，并且模式以'/'结尾，并且去掉结尾的'/'后的模式与给定的路径匹配，则返回True。
- 如果没有匹配到任何模式，则返回False。
**注意**: 使用该代码时需要注意以下几点：
- patterns参数应该是一个包含模式字符串的列表。
- path参数应该是一个字符串，表示要检查的路径。
- is_dir参数是可选的，默认为False。如果要检查的路径是一个目录，则应将is_dir参数设置为True。
**输出示例**: 模拟代码返回值的可能外观。
- 对于给定的路径和模式列表，如果路径与任何模式匹配，则返回True；否则返回False。
### _class_function check_files_and_folders(self)
**check_files_and_folders**: check_files_and_folders函数的功能是检查给定目录中的所有文件和文件夹是否与拆分的gitignore模式匹配。返回一个文件列表，这些文件既不被忽略，又具有'.py'扩展名。返回的文件路径是相对于self.directory的。

**参数**: 该函数没有参数。

**代码描述**: 该函数使用os.walk遍历给定目录下的所有文件和文件夹。首先，通过调用_is_ignored函数，将与文件夹模式匹配的文件夹从dirs列表中移除。然后，对于每个文件，将其路径与self.directory的相对路径进行比较，并检查文件是否与文件模式匹配且具有'.py'扩展名。如果满足条件，将文件的相对路径添加到not_ignored_files列表中。

**注意**: 使用该代码时需要注意以下几点：
- 确保已经设置了self.directory的值，以指定要检查的目录。
- 确保已经设置了self.folder_patterns和self.file_patterns的值，以指定要匹配的文件夹和文件模式。

**输出示例**: 
```
['folder1/file1.py', 'folder2/file2.py', 'file3.py']
```
