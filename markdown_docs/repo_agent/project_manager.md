## ClassDef ProjectManager
**ProjectManager**: The function of ProjectManager is to manage and retrieve the structure of a project within a repository.

**Attributes**:
- `repo_path`: The file system path to the repository containing the project.
- `project`: An instance of a jedi.Project, initialized with the repository path.
- `project_hierarchy`: The path to the project's hierarchy JSON file, which is constructed by joining the repository path, the project hierarchy directory, and the filename "project_hierarchy.json".

**Code Description**:
The `ProjectManager` class is designed to facilitate the management of a software project's structure within a repository. It is initialized with two parameters: `repo_path`, which specifies the path to the repository, and `project_hierarchy`, which denotes the relative path from the repository to the project's hierarchy directory. Upon initialization, it creates a `jedi.Project` instance for the given repository path. This is significant for understanding and navigating the project's codebase efficiently.

The class features a method, `get_project_structure`, which returns the structure of the project by recursively walking through the directory tree of the repository. This method is particularly useful for generating a textual representation of the project's file and directory structure, focusing on Python files (`.py`). It ignores hidden files and directories (those starting with a dot) and constructs a string that represents the hierarchy of Python files and directories within the project. This functionality is crucial for developers and tools that need to understand or display the project's layout.

In the context of the project, the `ProjectManager` is instantiated within the `Runner` class, which is part of the project's execution or management script. The `Runner` class uses the `ProjectManager` to access the project's structure, indicating that the `ProjectManager` plays a critical role in the broader system for managing and interacting with the project's codebase. The `Runner` class initializes the `ProjectManager` with configuration parameters that specify the repository path and the project hierarchy, demonstrating how the `ProjectManager` is integrated into the project's workflow.

**Note**:
- It is essential to ensure that the `repo_path` and `project_hierarchy` parameters are correctly set to reflect the actual structure of the project within the repository.
- The `jedi.Project` instance requires the `jedi` library, which should be installed and properly configured in the project's environment.

**Output Example**:
Assuming a project structure like this:
```
repo_agent/
    project_manager.py
    runner.py
    utils/
        helper.py
```
The output of `get_project_structure` might look like:
```
repo_agent
  project_manager.py
  runner.py
  utils
    helper.py
```
This output provides a clear, textual representation of the project's structure, focusing on Python files and directories, excluding hidden files and directories.
### FunctionDef __init__(self, repo_path, project_hierarchy)
**__init__**: The function of __init__ is to initialize a new instance of the ProjectManager class.

**Parameters**:
- **repo_path**: The file system path to the repository that the project manager will operate on.
- **project_hierarchy**: The relative path from the repository to the project hierarchy file, excluding the file name.

**Code Description**:
The `__init__` method is a special method in Python that is called when a new instance of a class is created. In the context of the ProjectManager class, this method serves to initialize the instance with specific attributes and configurations necessary for its operation.

Upon instantiation, the `__init__` method takes two parameters: `repo_path` and `project_hierarchy`. The `repo_path` parameter is expected to be a string representing the path to the repository this instance of ProjectManager will manage. This path is then used to initialize a `jedi.Project` object, which is assigned to the instance's `project` attribute. The `jedi.Project` object is likely used for interacting with the project's codebase in a way that understands the structure and syntax of the code, leveraging the Jedi library's capabilities.

The `project_hierarchy` parameter is also a string, representing the relative path from the repository's root to the location where the project hierarchy file is (or will be) stored. However, it does not include the name of the file itself. The method constructs the full path to the project hierarchy file by joining the `repo_path` with the `project_hierarchy` and appending `"project_hierarchy.json"` to it. This full path is then stored in the instance's `project_hierarchy` attribute.

This setup implies that the ProjectManager class is designed to work with projects that have a specific structure and configuration, part of which includes a JSON file named `project_hierarchy.json` that presumably contains information about the project's structure or configuration.

**Note**:
- It is important to ensure that the `repo_path` provided is valid and points to the intended repository, as this path is used for initializing the Jedi project and constructing the path to the project hierarchy file.
- The `project_hierarchy` should be provided relative to the `repo_path` and should correctly lead to the directory where the `project_hierarchy.json` file is expected to be found or created. Incorrect paths could lead to errors in locating or interacting with the project hierarchy file.
***
### FunctionDef get_project_structure(self)
**get_project_structure**: The function of `get_project_structure` is to return the structure of the project by recursively walking through the directory tree.

**Parameters**: This function does not take any parameters except for the implicit `self` parameter, which is a reference to the instance of the class that contains the project's repository path.

**Code Description**: The `get_project_structure` function is designed to provide a textual representation of the project's directory structure, focusing specifically on Python files. It achieves this through a nested function named `walk_dir`, which performs the recursive directory traversal.

The `walk_dir` function takes two parameters: `root`, which is the directory path to start the traversal from, and `prefix`, which is used to maintain the indentation level for the visual representation of the directory structure. The `prefix` parameter is initialized with an empty string and gets incremented with two spaces for each level of recursion, enhancing the readability of the output.

The function begins by appending the name of the current directory (`root`) to a list named `structure`. It then iterates over all items in the directory, sorted alphabetically by their names. Hidden files and directories (those starting with a dot) are ignored to focus on relevant project files. For each item, if it is a directory, `walk_dir` is called recursively with the updated `prefix`. If the item is a Python file (determined by the `.py` extension), its name is appended to the `structure` list with the current indentation level.

After the recursive traversal is complete, the `structure` list, which now contains the formatted project structure, is joined into a single string with newline characters separating each item. This string is then returned as the function's output.

**Note**: The function relies on the `os` module for directory and file operations, including checking whether a path is a directory or a file, listing directory contents, and joining paths. It is essential that the `repo_path` attribute of the class instance calling this function is correctly set to the root directory of the project for accurate results.

**Output Example**:
```
project_root
  main.py
  utils
    __init__.py
    helper.py
  models
    __init__.py
    user.py
```
This example output represents a project with a `main.py` file in the root directory, and two subdirectories (`utils` and `models`), each containing an `__init__.py` file and another Python file. The indentation indicates the directory hierarchy.
#### FunctionDef walk_dir(root, prefix)
**walk_dir**: The function of walk_dir is to recursively walk through a directory structure, listing all Python files and directories, while ignoring hidden files and directories.

**Parameters**:
- **root**: The root directory from which the traversal begins. It is a string representing the path to the directory.
- **prefix**: An optional string parameter used to prefix directory names and filenames to indicate their level in the directory hierarchy. It defaults to an empty string.

**Code Description**:
The `walk_dir` function is designed to create a hierarchical representation of a directory structure, focusing specifically on Python files (`.py`). It takes two parameters: `root`, which specifies the starting point of the directory traversal, and `prefix`, which is used to visually represent the depth of directories and files in the structure.

Upon invocation, the function first appends the basename of the `root` directory to a global list named `structure`, prefixed by the current `prefix`. This action marks the beginning of a new level in the directory hierarchy.

The `prefix` is then extended by two spaces, creating a new `new_prefix` that will be used for items within the `root` directory, indicating their nested level.

The function iterates over all items in the `root` directory, sorted alphabetically by their names. It ignores items that start with a dot (`.`), which are typically hidden files or directories in Unix-like systems.

For each item, the function checks if it is a directory or a file:
- If the item is a directory (not hidden), `walk_dir` is called recursively with the path to the directory and the updated `new_prefix`. This recursion allows the function to traverse the directory structure depth-first.
- If the item is a file and it ends with `.py`, indicating it is a Python file, the file's name, prefixed by the `new_prefix`, is appended to the `structure` list. This inclusion of Python files in the structure list is selective, based on the file extension.

**Note**:
- The function relies on a global list named `structure` to accumulate the directory structure. Ensure this list is defined in the scope where `walk_dir` is called.
- The function is designed to ignore hidden files and directories, which may exclude relevant files if they are named accordingly.
- The `prefix` parameter is used internally to maintain the visual hierarchy of the directory structure. It is incremented with two spaces for each level of depth, but this can be adjusted if a different visual representation is desired.
- The function does not return a value; instead, it modifies the global `structure` list in place. Ensure to process or print the `structure` list after calling `walk_dir` to view the directory structure.
***
***
