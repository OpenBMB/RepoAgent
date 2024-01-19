# ClassDef ProjectManager:
**ProjectManager**: ProjectManager的功能是管理项目的类。

**属性**：该类具有以下属性：
- repo_path：项目的存储路径。
- project：项目对象，使用jedi库创建。
- project_hierarchy：项目层级结构的路径。

**代码描述**：ProjectManager类是一个用于管理项目的类。它具有以下功能：

- `__init__(self, repo_path, project_hierarchy)`: 构造函数，用于初始化ProjectManager对象。接受两个参数：repo_path表示项目的存储路径，project_hierarchy表示项目的层级结构。在构造函数中，将repo_path赋值给self.repo_path属性，然后使用jedi库创建一个Project对象，并将其赋值给self.project属性。最后，将repo_path、project_hierarchy和".project_hierarchy.json"拼接起来作为self.project_hierarchy属性的值。

- `get_project_structure(self)`: 获取项目结构的函数。该函数没有参数。在函数内部定义了一个内部函数`walk_dir(root, prefix="")`，用于遍历项目目录并获取项目结构。在`walk_dir`函数中，首先将当前目录添加到结构列表中，然后遍历当前目录下的所有文件和子目录。如果遇到子目录，则递归调用`walk_dir`函数；如果遇到以".py"结尾的文件，则将文件名添加到结构列表中。最后，将结构列表转换为字符串并返回。

- `find_all_referencer(self, variable_name, file_path, line_number, column_number)`: 查找给定文件中变量的所有引用的函数。接受四个参数：variable_name表示要搜索的变量名，file_path表示要搜索的文件路径，line_number表示变量所在的行号，column_number表示变量所在的列号。在函数内部，使用jedi库的Script类创建一个Script对象，并指定要搜索的文件路径。然后，使用Script对象的`get_references`方法获取变量的所有引用。接下来，过滤出引用变量名与variable_name相同的引用，并将它们的位置信息（文件路径、行号和列号）添加到结果列表中。最后，将结果列表返回。

**注意**：在使用`find_all_referencer`函数时，需要传入正确的变量名、文件路径、行号和列号，以确保能够正确地找到变量的引用。

**输出示例**：以下是`get_project_structure`函数的输出示例：
```
project_folder
  subfolder1
    file1.py
    file2.py
  subfolder2
    file3.py
    file4.py
  file5.py
```
## FunctionDef __init__(self, repo_path, project_hierarchy):
**__init__**: __init__函数的功能是初始化ProjectManager对象。
**参数**: 
- repo_path: 字符串类型，表示项目的根路径。
- project_hierarchy: 字符串类型，表示项目层级结构的文件名。
**代码描述**: 
__init__函数接受两个参数，repo_path和project_hierarchy，用于初始化ProjectManager对象的属性。在函数内部，将repo_path赋值给self.repo_path，表示项目的根路径。然后，使用repo_path初始化一个jedi.Project对象，并将其赋值给self.project，用于后续的代码分析和处理。接下来，使用os.path.join函数将repo_path、project_hierarchy和".project_hierarchy.json"拼接在一起，生成项目层级结构文件的路径，并将其赋值给self.project_hierarchy，表示项目层级结构文件的路径。
**注意**: 
- 该函数依赖于jedi模块和os模块，需要确保这两个模块已经导入。
**输出示例**: 无
Raw code:```
    def __init__(self, repo_path, project_hierarchy):
        self.repo_path = repo_path
        self.project = jedi.Project(self.repo_path)
        self.project_hierarchy = os.path.join(self.repo_path, project_hierarchy, ".project_hierarchy.json")
```
## FunctionDef get_project_structure(self):
**get_project_structure**: get_project_structure函数的功能是获取项目的结构。
**参数**: 该函数没有参数。
**代码描述**: 该函数通过递归遍历指定路径下的所有文件和文件夹，将项目的结构保存在一个列表中，并返回该列表的字符串形式。
**代码分析**: 
1. 首先，定义了一个内部函数walk_dir，用于递归遍历指定路径下的文件和文件夹。
2. walk_dir函数接受两个参数，root表示当前遍历的路径，prefix表示当前路径的前缀。
3. 在walk_dir函数中，首先将当前路径的文件夹名添加到结构列表中，使用os.path.basename(root)获取文件夹名，并添加到结构列表中。
4. 然后，根据当前路径的前缀，生成新的前缀new_prefix，用于下一级文件夹的前缀。
5. 使用os.listdir(root)获取当前路径下的所有文件和文件夹的名称，并使用sorted函数对其进行排序。
6. 遍历当前路径下的每个文件和文件夹的名称，如果名称以'.'开头，则忽略隐藏文件和目录。
7. 如果是文件夹，则递归调用walk_dir函数，传入文件夹的路径和新的前缀new_prefix。
8. 如果是以'.py'结尾的文件，则将文件名添加到结构列表中，使用new_prefix作为前缀。
9. 最后，定义一个空的结构列表structure，调用walk_dir函数，传入self.repo_path作为根路径，将项目的结构保存在structure列表中。
10. 使用'\n'.join(structure)将结构列表转换为字符串，并返回该字符串。
**注意**: 
- 该函数依赖于os模块和os.path模块，需要确保这两个模块已经导入。
- 该函数会忽略隐藏文件和目录，只获取以'.py'结尾的文件。
**输出示例**: 
```
project_folder
  sub_folder1
    file1.py
    file2.py
  sub_folder2
    file3.py
    file4.py
```
### FunctionDef walk_dir(root, prefix):
**walk_dir**: walk_dir函数的功能是遍历指定目录下的所有文件和子目录，并将它们的结构保存到一个列表中。
**parameters**: walk_dir函数有两个参数：
- root：字符串类型，表示要遍历的根目录的路径。
- prefix：字符串类型，表示每一级目录的前缀，用于在结构列表中显示层级关系，默认为空字符串。
**Code Description**: walk_dir函数的代码逻辑如下：
1. 将当前目录的名称添加到结构列表中，前面加上前缀。
2. 根据指定的根目录，遍历该目录下的所有文件和子目录。
3. 对于每一个文件或子目录，判断是否以'.'开头，如果是则忽略。
4. 如果是子目录，则递归调用walk_dir函数，传入子目录的路径和新的前缀。
5. 如果是文件且以'.py'结尾，则将文件名添加到结构列表中，前面加上新的前缀。
**Note**: 使用该代码时需要注意以下几点：
- 需要提供正确的根目录路径作为参数。
- 结构列表将保存所有文件和子目录的层级关系，可以根据需要进行进一步处理。
## FunctionDef find_all_referencer(self, variable_name, file_path, line_number, column_number):
**find_all_referencer**: find_all_referencer函数的功能是在给定的文件中查找变量的所有引用。

**参数**：
- variable_name (str): 要搜索的变量的名称。
- file_path (str): 要搜索的文件的路径。
- line_number (int): 变量所在的行号。
- column_number (int): 变量所在的列号。

**代码说明**：
该函数首先使用jedi.Script函数创建一个脚本对象script，脚本对象的路径为self.repo_path和file_path的拼接结果。然后使用script.get_references方法获取变量的所有引用。

接下来，函数会过滤掉引用名称不等于variable_name的引用，并返回它们的位置信息。最后，函数会将每个引用的文件路径、行号和列号组成一个元组，并以列表的形式返回。

**注意**：
- 该函数依赖于jedi库，需要先安装该库。
- 如果发生异常，函数会打印错误消息和相关参数，并返回一个空列表。

**输出示例**：
假设variable_name为"count"，file_path为"example.py"，line_number为10，column_number为5，函数可能返回的结果如下：
[("example.py", 15, 8), ("example.py", 20, 12), ("example.py", 25, 3)]
***
