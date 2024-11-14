## ClassDef ProjectManager
**ProjectManager**: The function of ProjectManager is to manage and retrieve the structure of a project repository.

**attributes**: The attributes of this Class.
· repo_path: The file path to the project repository.
· project: An instance of the Jedi Project class, initialized with the repo_path.
· project_hierarchy: The file path to the project hierarchy JSON file, constructed from the repo_path and project_hierarchy parameter.

**Code Description**: The ProjectManager class is designed to facilitate the management of a project repository by providing methods to retrieve the project's directory structure and build a reference path tree. Upon initialization, the class requires two parameters: `repo_path`, which specifies the location of the project repository, and `project_hierarchy`, which indicates the name of the hierarchy to be used. The class constructs the path to the project hierarchy JSON file by combining the repo_path with the project_hierarchy name.

The `get_project_structure` method is responsible for returning the structure of the project by recursively traversing the directory tree starting from the repo_path. It constructs a string representation of the project structure, including all directories and Python files, while ignoring hidden files and directories. This method utilizes a nested function `walk_dir` to perform the recursive traversal.

The `build_path_tree` method creates a hierarchical tree structure based on two lists of paths: `who_reference_me` and `reference_who`, as well as a specific `doc_item_path`. It constructs a nested dictionary using `defaultdict` to represent the tree structure. The method modifies the last part of the `doc_item_path` to indicate a specific item with a star symbol. Finally, it converts the tree structure into a string format for easier visualization.

The ProjectManager class is instantiated within the Runner class, where it is initialized with the target repository and hierarchy name obtained from the SettingsManager. This integration allows the Runner to leverage the ProjectManager's capabilities to manage and retrieve project structure information, which is essential for the overall functionality of the application.

**Note**: When using the ProjectManager class, ensure that the provided repo_path is valid and accessible. The project_hierarchy should correspond to an existing hierarchy name to avoid file path errors.

**Output Example**: A possible output of the `get_project_structure` method might look like this:
```
project_root
  src
    main.py
    utils.py
  tests
    test_main.py
```
### FunctionDef __init__(self, repo_path, project_hierarchy)
**__init__**: __init__的功能是初始化ProjectManager类的实例。

**parameters**: 该函数的参数如下：
· parameter1: repo_path - 指定项目的存储库路径。
· parameter2: project_hierarchy - 指定项目层次结构的路径。

**Code Description**: 该__init__函数用于初始化ProjectManager类的实例。在函数内部，首先将传入的repo_path参数赋值给实例变量self.repo_path，以便在类的其他方法中使用。接着，使用jedi库创建一个新的Project对象，并将其赋值给self.project，传入的repo_path作为参数。这使得ProjectManager能够利用jedi库提供的功能来处理代码分析和自动补全等任务。最后，函数通过os.path.join方法构建项目层次结构的完整路径，将其赋值给self.project_hierarchy。该路径由repo_path、project_hierarchy参数和一个名为"project_hierarchy.json"的文件名组成，这样可以方便地访问项目的层次结构数据。

**Note**: 使用该代码时，请确保传入的repo_path是有效的文件路径，并且project_hierarchy参数指向的目录中存在"project_hierarchy.json"文件，以避免在实例化过程中出现错误。
***
### FunctionDef get_project_structure(self)
**get_project_structure**: The function of get_project_structure is to return the structure of the project by recursively walking through the directory tree.

**parameters**: The parameters of this Function.
· There are no parameters for this function.

**Code Description**: The get_project_structure function is designed to generate a string representation of the project's directory structure. It does this by defining an inner function called walk_dir, which takes two arguments: root (the current directory being processed) and prefix (a string used to format the output). The function initializes an empty list called structure to hold the formatted directory and file names.

The walk_dir function begins by appending the base name of the current directory (root) to the structure list, prefixed by the provided prefix. It then creates a new prefix by adding two spaces to the existing prefix to indicate a deeper level in the directory hierarchy. The function proceeds to iterate over the sorted list of items in the current directory, skipping any hidden files or directories (those starting with a dot).

For each item, it constructs the full path and checks if it is a directory or a Python file (ending with ".py"). If it is a directory, the function calls itself recursively with the new prefix. If it is a Python file, it appends the file name to the structure list with the new prefix.

Finally, after the walk_dir function has processed all directories and files, the get_project_structure function joins the elements of the structure list into a single string, separated by newline characters, and returns this string.

**Note**: It is important to ensure that the repo_path attribute of the class instance is correctly set to the root directory of the project before calling this function. The function will only include Python files in the output, ignoring other file types.

**Output Example**: 
```
project_name
  module1
    file1.py
    file2.py
  module2
    file3.py
  README.md
```
#### FunctionDef walk_dir(root, prefix)
**walk_dir**: walk_dir的功能是遍历指定目录及其子目录，并收集所有Python文件的结构信息。

**parameters**: 此函数的参数如下：
· parameter1: root - 要遍历的根目录的路径。
· parameter2: prefix - 用于格式化输出的前缀字符串，默认为空字符串。

**Code Description**: 
walk_dir函数用于递归遍历给定的目录（root）及其所有子目录。它首先将当前目录的名称（通过os.path.basename(root)获取）添加到结构列表中（structure），并在前缀字符串（prefix）后添加空格以便于格式化。接着，函数使用os.listdir(root)列出当前目录中的所有文件和子目录，并对这些名称进行排序。

在遍历每个名称时，函数会检查名称是否以点（.）开头，以此来忽略隐藏文件和目录。如果名称不是隐藏的，函数会构造该名称的完整路径（path）。如果该路径是一个目录，函数会递归调用walk_dir，传入新的前缀（new_prefix）。如果该路径是一个文件且文件名以“.py”结尾，函数则将该文件的名称添加到结构列表中，前面加上新的前缀。

该函数的设计使得它能够有效地收集指定目录下所有Python文件的结构信息，并以层级方式展示。

**Note**: 使用此代码时，请确保传入的根目录路径是有效的，并且具有读取权限。此外，函数会忽略所有以点开头的文件和目录，因此如果需要处理这些文件，需调整相关逻辑。
***
***
### FunctionDef build_path_tree(self, who_reference_me, reference_who, doc_item_path)
**build_path_tree**: The function of build_path_tree is to construct a hierarchical representation of file paths based on two reference lists and a specific document item path.

**parameters**: The parameters of this Function.
· who_reference_me: A list of file paths that reference the current object.
· reference_who: A list of file paths that are referenced by the current object.
· doc_item_path: A specific file path that needs to be highlighted in the tree structure.

**Code Description**: The build_path_tree function creates a nested dictionary structure representing a tree of file paths. It utilizes the `defaultdict` from the `collections` module to facilitate the creation of this tree. The function begins by defining an inner function, `tree`, which initializes a new `defaultdict` that can recursively create nested dictionaries.

The function then processes the two input lists, `who_reference_me` and `reference_who`. For each path in these lists, it splits the path into its components using the operating system's path separator (`os.sep`). It traverses the tree structure, creating a new node for each part of the path.

Next, the function processes the `doc_item_path`. It splits this path into components as well, but modifies the last component by prefixing it with a star symbol (✳️) to indicate that it is the item of interest. This modified path is then added to the tree in the same manner as the previous paths.

Finally, the function defines another inner function, `tree_to_string`, which converts the nested dictionary structure into a formatted string representation. This function recursively traverses the tree, indenting each level of the hierarchy for clarity. The resulting string is returned as the output of the build_path_tree function.

**Note**: It is important to ensure that the paths provided in `who_reference_me` and `reference_who` are valid and correctly formatted. The function assumes that the paths are well-structured and uses the operating system's path separator for splitting.

**Output Example**: 
Given the following inputs:
- who_reference_me: ["folder1/fileA.txt", "folder1/folder2/fileB.txt"]
- reference_who: ["folder3/fileC.txt"]
- doc_item_path: "folder1/folder2/fileB.txt"

The output of the function might look like this:
```
folder1
    fileA.txt
    folder2
        ✳️fileB.txt
folder3
    fileC.txt
```
#### FunctionDef tree
**tree**: tree函数的功能是返回一个默认字典，该字典的默认值是一个新的tree函数。

**parameters**: 该函数没有参数。

**Code Description**: tree函数使用了Python的defaultdict类。defaultdict是collections模块中的一个字典子类，它提供了一个默认值，当访问的键不存在时，会自动调用一个指定的工厂函数来生成这个默认值。在这个函数中，tree函数本身被用作工厂函数，这意味着每当访问一个不存在的键时，defaultdict将会创建一个新的tree对象。这种递归的结构使得返回的字典可以用于构建树形结构，其中每个节点都可以有多个子节点，且子节点的数量和内容是动态生成的。

**Note**: 使用该函数时，请注意避免无限递归的情况。由于tree函数返回的是一个defaultdict，其默认值也是tree函数本身，因此在访问未定义的键时会不断创建新的defaultdict，可能导致内存消耗过大。

**Output Example**: 调用tree函数后，可能的返回值如下：
```
defaultdict(<function tree at 0x...>, {})
```
此返回值表示一个空的defaultdict，且其默认值是tree函数本身。若访问一个不存在的键，例如`my_tree['a']`，则会创建一个新的defaultdict，作为'a'的值。
***
#### FunctionDef tree_to_string(tree, indent)
**tree_to_string**: tree_to_string的功能是将树形结构转换为字符串格式，便于可视化展示。

**parameters**: 此函数的参数如下：
· parameter1: tree - 一个字典类型的树形结构，其中键表示节点，值可以是子节点的字典或其他类型。
· parameter2: indent - 一个整数，表示当前节点的缩进级别，默认为0。

**Code Description**: tree_to_string函数通过递归的方式将树形结构转换为字符串。首先，函数初始化一个空字符串s。然后，它对传入的tree字典进行排序，并遍历每一个键值对。在遍历过程中，函数将当前键（节点）添加到字符串s中，并根据indent参数添加相应数量的空格以实现缩进。如果当前值是一个字典，表示该节点有子节点，函数会递归调用tree_to_string，将子节点转换为字符串并添加到s中。最终，函数返回构建好的字符串s。

**Note**: 使用此函数时，请确保传入的tree参数是一个有效的字典结构，并且可以包含嵌套的字典。indent参数用于控制输出的格式，通常不需要手动设置，除非在特定情况下需要调整缩进。

**Output Example**: 假设输入的tree为如下结构：
{
    "根节点": {
        "子节点1": {},
        "子节点2": {
            "孙节点1": {}
        }
    }
}
调用tree_to_string(tree)将返回：
根节点
    子节点1
    子节点2
        孙节点1
***
***
