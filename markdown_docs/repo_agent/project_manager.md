## _class ProjectManager
**ProjectManager**: ProjectManager的功能是管理项目的类。

**属性**：
- repo_path：项目的仓库路径
- project_hierarchy：项目的层次结构

**代码描述**：
ProjectManager类是用来管理项目的。在初始化时，需要传入项目的仓库路径和项目的层次结构。在初始化过程中，会创建一个jedi.Project对象，并将仓库路径赋值给self.repo_path属性。同时，会将项目的层次结构路径赋值给self.project_hierarchy属性。

get_project_structure方法用于获取项目的结构。该方法内部定义了一个walk_dir函数，用于遍历项目的目录结构。walk_dir函数会递归地遍历项目的每个目录和文件，并将它们的路径添加到structure列表中。最后，将structure列表转换为字符串，并返回。

**注意**：
- 该类依赖于jedi和os模块，需要确保这两个模块已经导入。
- 在调用get_project_structure方法之前，需要先调用__init__方法进行初始化。

**输出示例**：
```
project_folder
  subfolder1
    file1.py
    file2.py
  subfolder2
    file3.py
    file4.py
```
### _function __init__(self, repo_path, project_hierarchy)
**__init__**: __init__函数的功能是初始化ProjectManager对象。

**参数**：该函数的参数。
· repo_path: 代码仓库的路径。
· project_hierarchy: 项目层级的路径。

**代码描述**：该函数用于初始化ProjectManager对象。在函数内部，首先将传入的repo_path赋值给self.repo_path，然后使用jedi.Project函数创建一个名为self.project的jedi.Project对象，该对象用于处理代码分析和自动补全。接下来，将传入的project_hierarchy与".project_hierarchy.json"拼接，并赋值给self.project_hierarchy，用于指定项目层级的路径。

**注意**：在使用该函数时，需要传入正确的repo_path和project_hierarchy参数，以确保能够正确初始化ProjectManager对象。
### _function get_project_structure(self)
**get_project_structure**: get_project_structure函数的功能是获取项目的结构。
**参数**：此函数的参数。
· self: 对象本身。
**代码描述**：此函数的描述。
get_project_structure函数是一个内部函数，它使用递归的方式遍历指定目录下的所有文件和文件夹，并将它们的结构保存在一个列表中。函数首先定义了一个内部函数walk_dir，用于遍历目录。walk_dir函数接受两个参数，root表示当前遍历的目录，prefix表示当前目录的前缀。在遍历过程中，函数会将目录和文件的名称添加到结构列表中，并根据当前目录的深度添加相应的前缀。如果遍历到的是一个目录，则递归调用walk_dir函数继续遍历该目录。如果遍历到的是一个文件，并且文件的扩展名是.py，则将文件名添加到结构列表中。最后，函数调用walk_dir函数来遍历指定目录，并返回结构列表的字符串表示，每个元素以换行符分隔。
**注意**：关于代码使用的注意事项。
- 函数依赖于os模块和os.path模块，因此在使用之前需要先导入这两个模块。
- 函数假设传入的repo_path参数是一个有效的目录路径。
**输出示例**：模拟代码返回值的可能外观。
```
project_folder
  file1.py
  file2.py
  subfolder1
    file3.py
    file4.py
  subfolder2
    file5.py
```
#### _sub_function walk_dir(root, prefix)
**walk_dir**: walk_dir函数的功能是遍历指定目录下的所有文件和子目录，并将它们的结构保存到一个列表中。

**参数**：该函数的参数如下：
- root：字符串类型，表示要遍历的根目录的路径。
- prefix：字符串类型，表示每个文件或子目录的前缀，用于标识它们在目录结构中的层级关系，默认为空字符串。

**代码说明**：walk_dir函数通过递归的方式遍历指定目录下的所有文件和子目录。首先，它将根目录的基本名称添加到结构列表中，使用os.path.basename(root)获取根目录的基本名称，并将其添加到结构列表中。然后，它根据指定的前缀生成新的前缀new_prefix，用于标识子目录在目录结构中的层级关系。接下来，它使用os.listdir(root)获取根目录下的所有文件和子目录的名称，并对它们进行排序。对于每个名称，如果名称以'.'开头，则忽略该文件或子目录，因为它们是隐藏文件或目录。如果名称是一个目录，则使用递归调用walk_dir函数，传入该目录的路径和新的前缀new_prefix。如果名称是一个以'.py'结尾的文件，则将其添加到结构列表中，使用new_prefix作为前缀。

**注意**：在使用walk_dir函数时，需要注意以下几点：
- 确保传入的根目录路径是存在的，并且具有正确的访问权限。
- 结构列表将按照文件和子目录在目录结构中的层级关系顺序保存，可以根据需要对其进行进一步处理或展示。
- 由于递归调用，如果目录结构非常大或层级非常深，可能会导致函数的执行时间较长或栈溢出的问题。在处理大型目录结构时，建议使用其他更高效的方法或算法。
