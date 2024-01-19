## _class ProjectManager
**ProjectManager**: ProjectManager的功能是管理项目的类。

**attributes**: 这个类的属性有：
- repo_path: 项目的存储路径
- project: 项目对象
- project_hierarchy: 项目层次结构的路径

**Code Description**: 这个类用于管理项目。在初始化时，需要传入项目的存储路径和项目层次结构的路径。初始化时，会创建一个项目对象，并将项目层次结构的路径保存在project_hierarchy属性中。

get_project_structure方法用于获取项目的结构。它会遍历项目路径下的所有文件和文件夹，并将它们的名称保存在一个列表中。最后，将列表中的元素用换行符连接起来，并返回结果。

find_all_referencer方法用于查找给定文件中变量的所有引用。它接受变量名、文件路径、行号和列号作为参数。首先，它使用jedi库创建一个Script对象，并传入文件路径。然后，使用Script对象的get_references方法获取变量的所有引用。接下来，它会过滤掉引用中不包含变量名的部分，并返回每个引用的文件路径、行号和列号。

**Note**: 
- 在使用find_all_referencer方法时，需要确保传入的文件路径是相对于项目存储路径的相对路径。
- 如果在find_all_referencer方法中发生错误，会打印错误消息和相关参数，并返回一个空列表作为结果。

**Output Example**: 
```
[
    ('project_manager.py', 10, 5),
    ('project_manager.py', 15, 10),
    ('utils.py', 20, 15)
]
```
### _class_function __init__(self, repo_path, project_hierarchy)
**__init__**: __init__函数的功能是初始化ProjectManager对象。
**参数**: 
- repo_path: 项目的根目录路径。
- project_hierarchy: 项目层级结构的路径。
**代码描述**: 
__init__函数接受两个参数，repo_path和project_hierarchy，分别表示项目的根目录路径和项目层级结构的路径。
在函数内部，首先将传入的repo_path赋值给self.repo_path，以便后续使用。
然后，通过调用jedi.Project(self.repo_path)创建一个jedi.Project对象，并将其赋值给self.project，以便后续使用。jedi.Project是一个用于分析Python代码的工具，可以用于获取代码的结构和提供代码补全功能。
接下来，将传入的repo_path、project_hierarchy和".project_hierarchy.json"拼接起来，得到项目层级结构文件的完整路径，并将其赋值给self.project_hierarchy，以便后续使用。
**注意**: 
- 在使用该函数之前，需要确保os、jedi模块已经安装并导入。
**示例代码**:
```python
pm = ProjectManager('/path/to/repo', 'project_hierarchy')
```
**注意**: 
- 该函数在创建ProjectManager对象时会自动调用，无需手动调用。
- 传入的repo_path和project_hierarchy参数应该是有效的路径。
- 通过self.repo_path可以获取项目的根目录路径。
- 通过self.project可以获取jedi.Project对象，用于分析项目的代码。
- 通过self.project_hierarchy可以获取项目层级结构文件的路径。
### _class_function get_project_structure(self)
**get_project_structure**: get_project_structure函数的功能是获取项目的结构。
**参数**: 该函数没有参数。
**代码描述**: 该函数通过遍历项目目录，获取项目的结构信息，并将结果以字符串形式返回。
首先，函数内部定义了一个名为walk_dir的嵌套函数，用于遍历目录并获取项目结构信息。walk_dir函数接受两个参数，root表示当前遍历的根目录，prefix表示当前目录的前缀，用于标识目录的层级关系。
在walk_dir函数内部，首先将当前目录的名称添加到结构列表structure中，通过os.path.basename(root)获取目录的名称，并添加到structure列表中。然后，根据当前目录的名称更新前缀new_prefix，用于标识下一级目录的层级关系。
接下来，通过sorted函数对当前目录下的文件和目录进行排序，并遍历每一个文件和目录。如果遍历到的名称以'.'开头，表示该文件或目录是隐藏文件或目录，忽略不处理。如果遍历到的是目录，递归调用walk_dir函数，传入该目录的路径和新的前缀new_prefix，继续遍历该目录下的文件和目录。如果遍历到的是文件，并且文件名以'.py'结尾，将文件名添加到结构列表structure中，通过new_prefix + name的形式添加到structure列表中。
最后，定义一个空列表structure，用于存储项目的结构信息。调用walk_dir函数，传入self.repo_path作为根目录，开始遍历项目目录并获取结构信息。最后，通过'\n'.join(structure)将结构列表转换为字符串，并作为函数的返回值返回。
**注意**: 该函数依赖于os和jedi模块，需要确保这两个模块已经安装并导入。
**输出示例**: 假设项目目录结构如下：
- project
  - module1
    - file1.py
    - file2.py
  - module2
    - file3.py
  - file4.py
调用get_project_structure函数后，返回的结果为：
- project
  - module1
    - file1.py
    - file2.py
  - module2
    - file3.py
  - file4.py
#### _sub_function walk_dir(root, prefix)
**walk_dir**: walk_dir函数的功能是遍历指定目录下的所有文件和子目录，并将它们的结构保存到一个列表中。
**parameters**: walk_dir函数有两个参数：
- root：要遍历的根目录的路径。
- prefix：文件和目录的前缀，用于标识它们在目录结构中的层级关系。
**Code Description**: walk_dir函数的代码逻辑如下：
1. 将根目录的基本名称添加到结构列表中，前缀为空。
2. 创建一个新的前缀，将原前缀加上两个空格，用于标识子目录和文件的层级关系。
3. 遍历根目录下的所有文件和子目录，按名称进行排序。
4. 如果名称以'.'开头，表示是隐藏文件或目录，忽略它们。
5. 构建文件或目录的完整路径。
6. 如果是目录，递归调用walk_dir函数，传入子目录的路径和新的前缀。
7. 如果是文件且以'.py'结尾，将文件名添加到结构列表中，前缀为新的前缀。
**Note**: 使用该代码时需要注意以下几点：
- 确保传入的根目录路径存在且有效。
- 该函数会遍历根目录下的所有文件和子目录，可能会消耗较长的时间和资源，特别是在大型项目中使用时。请谨慎使用。
- 结构列表中保存的是文件和目录的相对路径，可以根据需要进行进一步处理和使用。
### _class_function find_all_referencer(self, variable_name, file_path, line_number, column_number)
**find_all_referencer**: find_all_referencer函数的功能是在给定的文件中查找变量的所有引用。
**parameters**: 这个函数的参数有：
- variable_name (str): 要搜索的变量的名称。
- file_path (str): 要搜索的文件的路径。
- line_number (int): 变量所在的行号。
- column_number (int): 变量所在的列号。
**Code Description**: 这个函数的作用是在给定的文件中查找变量的所有引用。它使用jedi库来解析代码，并通过指定的行号和列号来获取变量的引用。然后，它过滤出与变量名称匹配的引用，并返回每个引用的文件路径、行号和列号。
**Note**: 使用这段代码时需要注意以下几点：
- 需要安装jedi库。
- 需要传入正确的变量名称、文件路径、行号和列号。
**Output Example**: 以下是这段代码返回值的一个示例：
[('path/to/file.py', 10, 5), ('path/to/file.py', 15, 3), ('path/to/file.py', 20, 8)]
