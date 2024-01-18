# ClassDef ProjectManager:
**ProjectManager**: The function of this Class is to manage the project hierarchy and provide functionality to retrieve the project structure and find all references of a variable in a given file.

**attributes**: 
- repo_path (str): The path of the repository.
- project (jedi.Project): The Jedi project associated with the repository.
- project_hierarchy (str): The path of the project hierarchy file.

**Code Description**: 
The `ProjectManager` class is responsible for managing the project hierarchy and providing methods to retrieve the project structure and find all references of a variable in a given file.

The `__init__` method initializes the `ProjectManager` object by setting the `repo_path` attribute to the provided repository path, creating a Jedi project associated with the repository, and setting the `project_hierarchy` attribute to the path of the project hierarchy file.

The `get_project_structure` method is used to retrieve the project structure. It defines a nested function `walk_dir` that recursively traverses the repository directory and appends the directory and file names to the `structure` list. The method then calls `walk_dir` with the repository path as the root directory and returns the project structure as a string.

The `find_all_referencer` method is used to find all references of a variable in a given file. It takes the variable name, file path, line number, and column number as arguments. It creates a Jedi script object with the file path and uses the `get_references` method to retrieve all references of the variable at the specified location. The method filters out the references with the same variable name and returns a list of tuples containing the file path, line number, and column number of each reference.

**Note**: 
- This class requires the `jedi` library to be installed.
- The `get_project_structure` method only includes directories and Python files in the project structure.
- The `find_all_referencer` method assumes that the provided file path is relative to the repository path.

**Output Example**: 
- `get_project_structure`:
  ```
  RepoAgent
    assets
      images
    display
      book_template
      book_tools
        generate_repoagent_books.py
        generate_summary_from_book.py
      books
      scripts
    examples
      init.py
    repo_agent
      __init__.py
      __pycache__
      change_detector.py
      chat_engine.py
      config.py
      doc_meta_info.py
      file_handler.py
      project_manager.py
      prompt.py
      runner.py
      utils
        __pycache__
        gitignore_checker.py
    setup.py
    tests
      __init__.py
      test_change_detector.py
  ```

- `find_all_referencer`:
  ```
  [
    ('repo_agent/chat_engine.py', 10, 5),
    ('repo_agent/chat_engine.py', 15, 10),
    ('repo_agent/chat_engine.py', 20, 15)
  ]
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
**get_project_structure**: The function of this Function is to retrieve the hierarchical structure of a project.

**parameters**: This Function does not take any parameters.

**Code Description**: This Function uses a recursive approach to traverse the project directory and retrieve the hierarchical structure. It starts by calling the `walk_dir` function with the root directory path. The `walk_dir` function takes two parameters: `root` and `prefix`. 

Inside the `walk_dir` function, the base name of the current directory is appended to the `structure` list with the provided `prefix`. Then, a new prefix is created by adding two spaces to the current prefix. 

Next, the function iterates over the sorted list of names in the current directory. If a name starts with a dot, indicating a hidden file or directory, it is ignored. If the name corresponds to a directory, the `walk_dir` function is recursively called with the path of the subdirectory and the new prefix. If the name corresponds to a Python file (ends with '.py'), it is appended to the `structure` list with the new prefix.

After traversing the entire project directory, the `structure` list is joined with newline characters and returned as a string.

**Note**: This Function ignores hidden files and directories (those starting with a dot) and only includes Python files in the project structure.

**Output Example**:
```
RepoAgent
  assets
    images
  display
    book_template
    book_tools
      generate_repoagent_books.py
      generate_summary_from_book.py
    books
    scripts
  examples
    init.py
  repo_agent
    __init__.py
    __pycache__
    change_detector.py
    chat_engine.py
    config.py
    doc_meta_info.py
    file_handler.py
    project_manager.py
    prompt.py
    runner.py
    utils
      __pycache__
      gitignore_checker.py
  setup.py
  tests
    __init__.py
    test_change_detector.py
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
