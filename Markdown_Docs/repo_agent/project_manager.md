# ClassDef ProjectManager:
**ProjectManager**: The function of this Class is to manage a project by providing methods to retrieve the project structure and find all references of a variable in a given file.

**attributes**: 
- `repo_path (str)`: The path of the repository where the project is located.
- `project (jedi.Project)`: The Jedi project object representing the project.
- `project_hierarchy (str)`: The path of the project hierarchy file.

**Code Description**: 
The `ProjectManager` class has three attributes: `repo_path`, `project`, and `project_hierarchy`. The `repo_path` attribute stores the path of the repository where the project is located. The `project` attribute is an instance of the `jedi.Project` class, which represents the project. The `project_hierarchy` attribute stores the path of the project hierarchy file.

The `ProjectManager` class has two methods: `get_project_structure()` and `find_all_referencer()`.

The `get_project_structure()` method is used to retrieve the structure of the project. It internally calls the `walk_dir()` function to recursively traverse the repository directory and collect the names of directories and Python files. The collected structure is then returned as a formatted string.

The `find_all_referencer()` method is used to find all references of a variable in a given file. It takes four parameters: `variable_name`, `file_path`, `line_number`, and `column_number`. It uses the `jedi.Script` class to create a script object for the given file path. It then calls the `get_references()` method of the script object to retrieve all references of the variable at the specified line and column. The method filters out the references with the same variable name and returns a list of tuples containing the file path, line number, and column number of each reference.

If an error occurs during the execution of the `find_all_referencer()` method, an error message is printed along with the parameters that caused the error. An empty list is returned in case of an error.

**Note**: 
- The `jedi` module is used for code analysis and introspection.
- The `get_project_structure()` method assumes that the repository directory contains only directories and Python files. Other file types are ignored.
- The `find_all_referencer()` method assumes that the given file path is relative to the repository directory.

**Output Example**: 
Example output of the `get_project_structure()` method:
```
project_folder
  subfolder1
    file1.py
    file2.py
  subfolder2
    file3.py
  file4.py
```

Example output of the `find_all_referencer()` method:
```
[('subfolder1/file1.py', 10, 5), ('subfolder1/file2.py', 5, 10)]
```
## FunctionDef __init__(self, repo_path, project_hierarchy):
**__init__**: The function of this Function is to initialize a ProjectManager object.

**parameters**: 
- repo_path: The path to the repository.
- project_hierarchy: The path to the project hierarchy file.

**Code Description**: 
The `__init__` function is the constructor of the ProjectManager class. It takes in two parameters: `repo_path` and `project_hierarchy`. 

Inside the function, the `repo_path` parameter is assigned to the `repo_path` attribute of the ProjectManager object. 

Then, a new jedi.Project object is created using the `repo_path` as the argument, and assigned to the `project` attribute of the ProjectManager object. The jedi.Project object is used to interact with the project's Python code.

The `project_hierarchy` parameter is joined with the `repo_path` and the ".project_hierarchy.json" file extension to create the path to the project hierarchy file. This path is assigned to the `project_hierarchy` attribute of the ProjectManager object.

**Note**: 
- The `jedi` module is assumed to be imported before using this function.
- The `repo_path` and `project_hierarchy` attributes are assumed to be defined outside of the `__init__` function and are not shown in the provided code.

Raw code:
```
    def __init__(self, repo_path, project_hierarchy):
        self.repo_path = repo_path
        self.project = jedi.Project(self.repo_path)
        self.project_hierarchy = os.path.join(self.repo_path, project_hierarchy, ".project_hierarchy.json")
```
## FunctionDef get_project_structure(self):
**get_project_structure**: The function of this Function is to retrieve the structure of the project.

**parameters**: This Function does not take any parameters.

**Code Description**: 
The `get_project_structure` function is responsible for retrieving the structure of the project. It uses a helper function called `walk_dir` to recursively traverse the project directory and collect the names of all directories and Python files.

Inside the `get_project_structure` function, an empty list called `structure` is initialized. Then, the `walk_dir` function is called with the `repo_path` attribute of the ProjectManager object as the root directory. The `walk_dir` function appends the names of directories and Python files to the `structure` list.

After the `walk_dir` function completes, the `structure` list is joined with newline characters using the `join` method, and the resulting string is returned.

**Note**: 
- The `os` module is assumed to be imported before using this function.
- The `repo_path` attribute is assumed to be defined outside of the `get_project_structure` function and is not shown in the provided code.

**Output Example**: 
If the project structure is as follows:
```
project/
  ├── dir1/
  │   ├── file1.py
  │   └── file2.py
  ├── dir2/
  │   ├── file3.py
  │   └── file4.py
  └── file5.py
```
The return value of `get_project_structure` would be:
```
project
  dir1
    file1.py
    file2.py
  dir2
    file3.py
    file4.py
  file5.py
```
### FunctionDef walk_dir(root, prefix):
**walk_dir**: The function of this Function is to recursively traverse a directory and append the structure of the directory to a list.

**parameters**: 
- root: The root directory to start the traversal from.
- prefix: The prefix to be added to each directory or file name in the structure.

**Code Description**: 
The `walk_dir` function takes in a `root` directory and an optional `prefix` parameter. It appends the structure of the directory to a list called `structure`. 

The function starts by appending the basename of the `root` directory to the `structure` list, with the `prefix` added in front. 

Then, a new prefix is created by adding two spaces to the current `prefix`. This new prefix will be used for the subdirectories and files within the `root` directory.

Next, the function iterates over the sorted list of names in the `root` directory using the `os.listdir` function. For each name, it performs the following checks:

1. If the name starts with a dot (indicating a hidden file or directory), it is ignored and the loop moves on to the next name.
2. If the name corresponds to a subdirectory, the `walk_dir` function is called recursively with the subdirectory path as the new `root` and the new prefix as the `prefix`.
3. If the name corresponds to a file and ends with the ".py" extension, it is appended to the `structure` list with the new prefix added in front.

This process continues until all directories and files within the `root` directory have been traversed.

**Note**: 
- The `walk_dir` function relies on the `os` module, so make sure to import it before using this function.
- The `structure` list is assumed to be defined outside of the `walk_dir` function and is not shown in the provided code.
## FunctionDef find_all_referencer(self, variable_name, file_path, line_number, column_number):
**find_all_referencer**: The function of this Function is to find all references of a given variable in a specified file.

**parameters**: 
- variable_name (str): The name of the variable to search for.
- file_path (str): The path of the file to search in.
- line_number (int): The line number where the variable is located.
- column_number (int): The column number where the variable is located.

**Code Description**: 
This function takes in the name of a variable, the path of a file, and the line and column numbers where the variable is located. It uses the Jedi library to analyze the Python code in the specified file and find all references to the variable. 

First, it creates a Jedi Script object using the file path provided. Then, it calls the `get_references` method of the Script object, passing in the line and column numbers. This returns a list of references to the variable in the file.

Next, the function filters out the references that have the same variable name as the one provided. It creates a new list, `variable_references`, by iterating over the references and only keeping the ones with matching variable names. 

Finally, the function returns a list of tuples, where each tuple contains the file path, line number, and column number of a reference to the variable. It uses the `os.path.relpath` function to get the relative path of each reference's module, relative to the repository path. It also excludes the reference that matches the original line and column numbers, as it is the location of the variable declaration.

**Note**: 
- This function requires the Jedi library to be installed.
- The `self.repo_path` attribute is assumed to be the path to the repository where the file is located.

**Output Example**: 
If the variable name is "my_variable" and there are two references to it in the file "example.py" at line 10, column 5 and line 15, column 8, the function would return the following list:
[("example.py", 10, 5), ("example.py", 15, 8)]
***
