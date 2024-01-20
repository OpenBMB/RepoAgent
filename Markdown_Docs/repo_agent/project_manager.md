## _class ProjectManager
**ProjectManager**: ProjectManager的功能是管理项目的类。

**attributes**: 
- repo_path: 项目的存储路径
- project: 项目对象
- project_hierarchy: 项目层次结构的路径

**Code Description**: 
ProjectManager类是一个用于管理项目的类。它的构造函数接受两个参数：repo_path和project_hierarchy。repo_path是项目的存储路径，而project_hierarchy是项目层次结构的路径。在构造函数中，它会初始化repo_path和project_hierarchy属性，并创建一个jedi.Project对象来表示项目。

get_project_structure方法是ProjectManager类的一个方法，用于获取项目的结构。它内部定义了一个嵌套函数walk_dir，用于递归遍历项目路径下的所有文件和文件夹。walk_dir函数会将遍历到的文件和文件夹的名称添加到一个列表structure中。最后，get_project_structure方法会返回structure列表的字符串表示，即项目的结构。

**Note**: 
- 该类的构造函数需要传入repo_path和project_hierarchy参数。
- get_project_structure方法会返回项目的结构，以字符串形式表示。

**Output Example**: 
如果项目的结构如下所示：
- project_folder
  - file1.py
  - file2.py
  - subfolder1
    - file3.py
  - subfolder2
    - file4.py

那么get_project_structure方法的返回值将是：
```
project_folder
  file1.py
  file2.py
  subfolder1
    file3.py
  subfolder2
    file4.py
```
### _class_function __init__(self, repo_path, project_hierarchy)
**__init__**: __init__函数的功能是初始化一个ProjectManager对象。
**参数**: 这个函数的参数有两个：
- repo_path: 一个字符串，表示仓库的路径。
- project_hierarchy: 一个字符串，表示项目的层次结构。
**代码描述**: 这个函数首先将传入的repo_path赋值给self.repo_path属性，然后使用jedi.Project函数创建一个Project对象，并将其赋值给self.project属性。接下来，将传入的project_hierarchy和".project_hierarchy.json"拼接起来，并将结果赋值给self.project_hierarchy属性。
**注意**: 使用这段代码时需要注意以下几点：
- repo_path参数应该是一个有效的仓库路径。
- project_hierarchy参数应该是一个有效的项目层次结构。
### _class_function get_project_structure(self)
**get_project_structure**: get_project_structure函数的作用是获取项目的结构。
**参数**: 该函数没有参数。
**代码描述**: 该函数通过遍历项目目录，获取项目的结构信息，并将结果以字符串的形式返回。
函数内部定义了一个名为walk_dir的内部函数，用于递归遍历目录。walk_dir函数接受两个参数，root表示当前遍历的目录，prefix表示当前目录的前缀，用于控制输出的格式。在遍历过程中，如果遇到隐藏文件或目录，则忽略不处理。如果遇到子目录，则递归调用walk_dir函数进行遍历。如果遇到以.py结尾的文件，则将文件名添加到结果列表中。
在get_project_structure函数中，首先定义了一个空的列表structure，用于存储项目的结构信息。然后调用walk_dir函数，将项目根目录作为参数传入，开始遍历项目目录。最后，将结果列表转换为字符串，并使用换行符连接起来，作为函数的返回值。
**注意**: 该函数依赖于os模块和os.path模块，需要确保这两个模块已经导入。
**输出示例**: 假设项目的结构如下所示:
- project_manager.py
  - folder1
    - file1.py
    - file2.py
  - folder2
    - file3.py
  - file4.py
则函数的返回值为:
project_manager.py
  folder1
    file1.py
    file2.py
  folder2
    file3.py
  file4.py
#### _sub_function walk_dir(root, prefix)
**walk_dir**: walk_dir函数的功能是遍历指定目录下的所有文件和子目录，并将它们的结构保存到一个列表中。
**参数**: walk_dir函数接受两个参数：
- root：指定的根目录路径。
- prefix：可选参数，用于指定文件和子目录的前缀，默认为空字符串。
**代码说明**: walk_dir函数首先将根目录的基本名称添加到结构列表中，然后根据指定的前缀生成新的前缀。接下来，它遍历根目录下的所有文件和子目录。如果遇到隐藏文件或目录（以'.'开头），则忽略它们。对于每个文件或子目录，它将其路径与根目录拼接，并判断是否为目录。如果是目录，则递归调用walk_dir函数，并将新的前缀作为参数传递。如果是文件且以'.py'结尾，则将带有新前缀的文件名添加到结构列表中。
**注意**: 使用该代码时需要注意以下几点：
- 确保传递正确的根目录路径作为参数。
- 可以通过指定前缀来调整输出结果的格式。
- 该函数只会遍历根目录下的文件和子目录，不会遍历更深层次的目录。
