# FunctionDef need_to_generate(doc_item, ignore_list):
**need_to_generate**: The function of this Function is to determine whether a given `doc_item` should be generated or not based on its item type and the ignore list.

**parameters**: 
- `doc_item: DocItem` - The `DocItem` object representing the item to be checked.
- `ignore_list: List` - A list of file paths to be ignored.

**Code Description**: 
This function first retrieves the relative file path of the `doc_item` using the `get_full_name()` method. It then checks if the item type of the `doc_item` is either a file, directory, or repository. If it is any of these types, the function returns `False`, indicating that the item should not be generated.

If the item type is not one of the above, the function assigns the `father` attribute of the `doc_item` to `doc_item` itself. This is done to traverse up the hierarchy of the `doc_item` until a file is found. 

While traversing up, the function checks if the current `doc_item` is a file. If it is, it checks if the relative file path starts with any of the file paths in the `ignore_list`. If it does, the function returns `False`, indicating that the item should not be generated. If none of the file paths in the `ignore_list` match the relative file path, the function returns `True`, indicating that the item should be generated.

If no file is found while traversing up the hierarchy, the function returns `False`, indicating that the item should not be generated.

**Note**: 
- This function assumes that the `doc_item` object has a `get_full_name()` method and an `item_type` attribute.
- The `ignore_list` should contain file paths that are relative to the root of the project.
- The function only checks if the relative file path starts with any of the file paths in the `ignore_list`. It does not check for exact matches.

**Output Example**: 
If the `doc_item` is a file and its relative file path does not start with any of the file paths in the `ignore_list`, the function will return `True`. Otherwise, it will return `False`.
***
# ClassDef Runner:
**Runner**: The function of this Class is to manage the generation and update of documentation for the project. It contains methods to generate documentation for individual objects, detect changes in the project, update the documentation accordingly, and commit the changes to the repository.

**Attributes**: 
- project_manager: An instance of the ProjectManager class that manages the project hierarchy and file operations.
- change_detector: An instance of the ChangeDetector class that detects changes in the project files.
- chat_engine: An instance of the ChatEngine class that interacts with a chatbot to generate documentation.
- meta_info: An instance of the MetaInfo class that stores the metadata and status of the documentation.
- CONFIG: A configuration dictionary that contains project-specific settings.

**Code Description**:
- The `__init__` method initializes the Runner class by creating instances of the ProjectManager, ChangeDetector, and ChatEngine classes. It also checks if the project hierarchy exists and initializes or loads the MetaInfo object accordingly.
- The `get_all_pys` method is used to retrieve a list of all Python files in a given directory.
- The `generate_doc_for_a_single_item` method generates documentation for a single object by interacting with the ChatEngine and updating the MetaInfo object.
- The `first_generate` method generates documentation for all objects in the project hierarchy. It iterates through the topology list of objects, checks if they need to be generated, and calls the `generate_doc_for_a_single_item` method.
- The `markdown_refresh` method updates the markdown files with the latest documentation information from the MetaInfo object.
- The `git_commit` method commits the changes to the repository with a specified commit message.
- The `run` method is the main function that runs the document update process. It first checks if the documentation is being generated for the first time or if there are changes in the project. It then calls the necessary methods to generate or update the documentation accordingly.
- The `add_new_item` method adds new projects to the JSON file and generates corresponding documentation.
- The `process_file_changes` method processes the changes in a file by identifying added and removed objects, updating the JSON file, and generating documentation for the changed objects.
- The `update_existing_item` method updates existing projects by comparing the current and previous versions of the file, identifying added and removed objects, and updating the JSON file and documentation accordingly.
- The `update_object` method generates documentation content and updates the corresponding field information of an object.
- The `get_new_objects` method compares the current and previous versions of the file to identify added and deleted objects.

**Note**: 
- The Runner class is responsible for managing the generation and update of documentation for the project.
- It interacts with the ProjectManager, ChangeDetector, and ChatEngine classes to perform various tasks such as generating documentation, detecting changes, and updating the documentation.
- The MetaInfo object stores the metadata and status of the documentation, including the document version and the status of each object.
- The run method is the main entry point for running the document update process. It checks if the documentation is being generated for the first time or if there are changes in the project, and calls the necessary methods to generate or update the documentation accordingly.
- The add_new_item and process_file_changes methods handle the addition and changes in project files, respectively, by updating the JSON file and generating documentation for the affected objects.
- The update_existing_item method updates existing projects by comparing the current and previous versions of the file, identifying added and removed objects, and updating the JSON file and documentation accordingly.
- The get_new_objects method compares the current and previous versions of the file to identify added and deleted objects.

**Output Example**:
```
Runner:
- project_manager: <ProjectManager object>
- change_detector: <ChangeDetector object>
- chat_engine: <ChatEngine object>
- meta_info: <MetaInfo object>
- CONFIG: {'repo_path': '/path/to/repo', 'project_hierarchy': 'project_hierarchy.json', ...}

Code Description:
- The Runner class manages the generation and update of documentation for the project.
- It interacts with the ProjectManager, ChangeDetector, and ChatEngine classes to perform various tasks.
- The run method is the main entry point for running the document update process.
- The add_new_item and process_file_changes methods handle the addition and changes in project files.
- The update_existing_item method updates existing projects.
- The get_new_objects method identifies added and deleted objects.

Note:
- The Runner class is responsible for managing the generation and update of documentation for the project.
- The MetaInfo object stores the metadata and status of the documentation.
- The run method is the main entry point for running the document update process.
- The add_new_item and process_file_changes methods handle the addition and changes in project files.
- The update_existing_item method updates existing projects.
- The get_new_objects method compares the current and previous versions of the file.
```
## FunctionDef __init__(self):
**__init__**: The function of this Function is to initialize the Runner object.

**parameters**: This function does not take any parameters.

**Code Description**: 
- The function initializes the `project_manager` attribute of the Runner object by creating a new instance of the ProjectManager class. The `repo_path` and `project_hierarchy` parameters are passed to the ProjectManager constructor from the CONFIG dictionary.
- The function initializes the `change_detector` attribute of the Runner object by creating a new instance of the ChangeDetector class. The `repo_path` parameter is passed to the ChangeDetector constructor from the CONFIG dictionary.
- The function initializes the `chat_engine` attribute of the Runner object by creating a new instance of the ChatEngine class. The `CONFIG` parameter is passed to the ChatEngine constructor.
- The function checks if the project hierarchy directory exists in the repository path. If it does not exist, it initializes the `meta_info` attribute of the Runner object by calling the `init_from_project_path` method of the MetaInfo class. The `repo_path` parameter is passed to the `init_from_project_path` method from the CONFIG dictionary. Then, it calls the `checkpoint` method of the MetaInfo class to create a checkpoint in the target directory path.
- If the project hierarchy directory exists, it initializes the `meta_info` attribute of the Runner object by calling the `from_checkpoint_path` method of the MetaInfo class. The `repo_path` parameter is passed to the `from_checkpoint_path` method from the CONFIG dictionary. Then, it calls the `checkpoint` method of the MetaInfo class to create a checkpoint in the target directory path.

**Note**: 
- The CONFIG dictionary is assumed to contain the necessary configuration values, including the repository path and project hierarchy.
- The Runner object is responsible for managing the project, detecting changes, and handling chat interactions.
## FunctionDef get_all_pys(self, directory):
**get_all_pys**: The function of this Function is to retrieve all Python files within a given directory.

**parameters**: 
- directory (str): The directory to search for Python files.

**Code Description**: 
This function takes a directory path as input and searches for all Python files within that directory and its subdirectories. It uses the `os.walk()` function to traverse through the directory tree and retrieve the file names. For each file, it checks if the file extension is '.py' using the `endswith()` method. If the file has a '.py' extension, its path is appended to the `python_files` list. Finally, the function returns the list of paths to all Python files found.

**Note**: 
- The function assumes that the provided directory path is valid and exists.
- The function does not perform any recursive search within symbolic links.
- The function does not differentiate between regular Python files and files with the '.py' extension but are not valid Python files.

**Output Example**: 
If the function is called with the directory path '/path/to/directory', and the directory contains the following Python files:
- /path/to/directory/file1.py
- /path/to/directory/subdirectory/file2.py
- /path/to/directory/subdirectory/file3.txt

The function will return the following list:
['/path/to/directory/file1.py', '/path/to/directory/subdirectory/file2.py']
## FunctionDef generate_doc_for_a_single_item(self, doc_item, task_len, now_task_id):
**generate_doc_for_a_single_item**: The function of this Function is to generate documentation for a single object.

**parameters**: 
- self: The instance of the Runner class.
- doc_item: An object of the DocItem class representing the item for which the documentation needs to be generated.
- task_len: An integer representing the total number of tasks.
- now_task_id: An integer representing the current task ID.

**Code Description**:
The function begins by obtaining the relative file path of the doc_item using the `get_full_name()` method. It then checks if the item's status is not equal to `DocItemStatus.doc_up_to_date`. If the status is not up to date, it logs a message indicating that the documentation for the object is being generated. 

Next, it creates an instance of the FileHandler class, passing the repository path and the relative file path as arguments. This FileHandler instance will be used to handle the file associated with the doc_item.

The function then calls the `generate_doc()` method of the ChatEngine class, passing the doc_item and file_handler as arguments. This method is responsible for generating the actual documentation for the object. The returned response message from the ChatEngine is appended to the `md_content` attribute of the doc_item.

After generating the documentation, the item's status is updated to `DocItemStatus.doc_up_to_date`. The function then calls the `checkpoint()` method of the MetaInfo class, passing the target directory path as an argument. This method updates the checkpoint file to indicate that the documentation for the object has been generated.

If the item's status is already up to date, the function logs a message indicating that the documentation for the object has already been generated and skips the generation process.

**Note**: 
- This function is called within the Runner class and is responsible for generating documentation for a single object.
- The `generate_doc()` method of the ChatEngine class is used to generate the documentation for the object.
- The `checkpoint()` method of the MetaInfo class is used to update the checkpoint file after generating the documentation.
## FunctionDef first_generate(self):
**first_generate**: The function of this Function is to generate documentation for all objects in the project. It iterates through a list of objects in a specific order and generates documentation for each object. The generated documentation is then synchronized back to the file system. If an error occurs during the generation process, the function will automatically resume from where it left off in the next run.

**parameters**: This function does not take any parameters.

**Code Description**: 
- The function starts by logging a message indicating the start of the documentation generation process.
- It retrieves a list of objects in a specific order from the meta_info object.
- It filters the list of objects based on an ignore list provided in the project's configuration.
- It initializes a counter to keep track of the number of objects that have been generated.
- If the function is not already in the generation process, it sets the in_generation_process flag to True.
- It then iterates through the filtered list of objects and calls the generate_doc_for_a_single_item function for each object. It also updates the already_generated counter.
- After generating documentation for all objects, it updates the document_version in the meta_info object to the commit hash of the current state of the repository.
- It sets the in_generation_process flag to False.
- It creates a checkpoint of the meta_info object by saving it to a target directory path.
- Finally, it logs a message indicating the success of the generation process and the number of documents generated.

**Note**: 
- It is important to note that the generation process must be bound to a specific version of the code. Any modifications to the target repository code during the generation process will result in an inconsistent documentation state.
- The function relies on the change_detector object to determine the current state of the repository and track any changes made to the code.
- The function also depends on the meta_info object to retrieve the list of objects to generate documentation for and to store the generated documentation.
## FunctionDef markdown_refresh(self):
**markdown_refresh**: The function of this Function is to write the latest document information into a markdown format folder, regardless of whether the markdown content has changed or not.

**parameters**: This function does not take any parameters.

**Code Description**: 
The `markdown_refresh` function first retrieves a list of all file items using the `get_all_files` method from the `meta_info` object. It then iterates over each file item in the list. 

Inside the loop, there is a nested function called `recursive_check` which takes a `doc_item` parameter of type `DocItem` and returns a boolean value. This function is used to check if a file contains any documentation. It recursively checks if the `md_content` attribute of the `doc_item` is not empty. If it is not empty, it returns `True`. If the `md_content` is empty, it iterates over the children of the `doc_item` and recursively calls the `recursive_check` function on each child. If any child returns `True`, it means that the file contains documentation, and the function returns `True`. If none of the children return `True`, it means that the file does not contain documentation, and the function returns `False`.

If the `recursive_check` function returns `False` for a file item, the loop continues to the next file item.

If the `recursive_check` function returns `True` for a file item, the relative file path is obtained using the `get_full_name` method of the file item. Then, a `FileHandler` object is created with the repository path and the relative file path. 

Next, the `convert_to_markdown_file` method of the `file_handler` object is called to convert the JSON content of the file to markdown format. The resulting markdown content is stored in the `markdown` variable.

Finally, the `write_file` method of the `file_handler` object is called to write the markdown content to a `.md` file in the specified markdown documents folder. The file path is obtained by replacing the `.py` extension of the file with `.md`. 

After processing all file items, a log message is printed indicating that the markdown document has been refreshed at the specified markdown documents folder.

**Note**: 
- This function assumes that the `meta_info` object has been properly initialized and contains the necessary file item information.
- The `FileHandler` class and its methods are not provided in the given code, so their functionality and implementation details are not known.
- The `CONFIG` variable is used to access the repository path and the markdown documents folder path, but its definition and values are not provided in the given code.

**Output Example**: 
A possible appearance of the return value of this function is:
```
markdown document has been refreshed at /path/to/markdown_docs_folder
```
***
# FunctionDef recursive_check(doc_item):
**recursive_check**: The function of this Function is to check whether a file contains any documentation by recursively checking its children.

**parameters**: 
- doc_item: A DocItem object representing a file or directory.
- ignore_list: A list of file paths to be ignored.

**Code Description**: 
The function starts by checking if the `md_content` attribute of the `doc_item` is not empty. If it is not empty, it means that the file contains documentation and the function returns True.

If the `md_content` attribute is empty, the function iterates over the children of the `doc_item`. For each child, it recursively calls the `recursive_check` function. If any of the children return True, it means that the child or its descendants contain documentation, and the function returns True.

If none of the children or their descendants contain documentation, the function returns False.

**Note**: 
- This function assumes that the `doc_item` object has a `md_content` attribute that represents the content of the file in Markdown format.
- The function relies on the `children` attribute of the `doc_item` object to iterate over its children.
- The function does not handle cases where the `doc_item` object is not a file or directory.

**Output Example**: 
If the `doc_item` object represents a file that contains documentation, the function will return True. Otherwise, it will return False.
## FunctionDef git_commit(self, commit_message):
**git_commit**: The function of this Function is to commit changes to the Git repository with a specified commit message.

**parameters**: 
- commit_message: A string representing the commit message to be associated with the changes.

**Code Description**: 
The `git_commit` function uses the `subprocess.check_call` method to execute the Git command `git commit` with the specified commit message. The `--no-verify` option is used to bypass any pre-commit hooks that may be configured in the Git repository. The `-m` option is used to specify the commit message.

If the `git commit` command fails and raises a `subprocess.CalledProcessError`, the function catches the exception and prints an error message indicating that an error occurred while trying to commit.

**Note**: 
- Make sure that the Git command-line tool is installed and accessible from the command prompt or terminal where the script is being executed.
- Ensure that the script is being executed in a Git repository directory.
- The commit message should be meaningful and descriptive to provide a clear understanding of the changes being committed.
## FunctionDef run(self):
**run**: The function of this Function is to run the document update process.

**parameters**: This Function does not take any parameters.

**Code Description**: This Function is responsible for detecting the changed Python files, processing each file, and updating the documents accordingly. It first checks if the document version is empty. If it is empty, it calls the `first_generate()` method to generate the initial documents, checkpoints the target directory path, and returns. If the document version is not empty, it checks if the process is already in the generation process. If it is not, it starts detecting changes by merging the new project hierarchy with the old hierarchy. It handles various scenarios such as creating a new file, deleting a file or object, and changing reference relationships. After merging, it sets the `in_generation_process` flag to True.

Next, it loads the task list and filters out the items that need to be generated based on the `ignore_list`. It then iterates over the task list and calls the `generate_doc_for_a_single_item()` method for each item. After generating the documents for all the items, it sets the `in_generation_process` flag to False and updates the document version to the latest commit hash. It then checkpoints the target directory path, flashes the reference relation, and logs that the documents have been forwarded to the latest version. Finally, it calls the `markdown_refresh()` method.

**Note**: It is important to note that this Function relies on the `MetaInfo` class and other helper methods such as `first_generate()`, `load_doc_from_older_meta()`, `load_task_list()`, `print_task_list()`, `generate_doc_for_a_single_item()`, `checkpoint()`, and `markdown_refresh()`.

**Output Example**: This Function does not return any value.
## FunctionDef add_new_item(self, file_handler, json_data):
**add_new_item**: The function of this Function is to add new projects to the JSON file and generate corresponding documentation.

**parameters**: 
- file_handler (FileHandler): The file handler object for reading and writing files.
- json_data (dict): The JSON data storing the project structure information.

**Code Description**: 
The `add_new_item` function takes in a `file_handler` object and a `json_data` dictionary as parameters. It is responsible for adding new projects to the JSON file and generating the corresponding documentation.

First, an empty dictionary `file_dict` is created. This dictionary will store the information of the new objects to be added to the JSON file.

Next, a loop iterates over the functions and classes obtained from the `file_handler` object. For each object, the `file_handler` object is used to retrieve the code information. This code information is then passed to the `chat_engine` object's `generate_doc` method, along with the `file_handler` object. The `generate_doc` method returns a response message, from which the markdown content is extracted.

The markdown content is then added to the `code_info` dictionary, which contains the code information of the object. The `name` of the object is used as the key in the `file_dict` dictionary, and the `code_info` dictionary is added as the value.

After iterating over all the objects, the `file_dict` dictionary is added to the `json_data` dictionary, with the `file_handler.file_path` as the key. This updates the JSON data with the new project structure information.

The updated JSON data is then written back to the JSON file.

Next, the `file_handler` object is used to convert the JSON file content into markdown format. The converted markdown content is then written to a `.md` file in the Markdown Docs folder.

Finally, log messages are generated to indicate that the structure information of the new file has been written to the JSON file, and the Markdown documentation for the new file has been generated.

**Note**: 
- This function assumes that the `file_handler` object has methods for reading and writing files, as well as retrieving code information and converting it to markdown format.
- The `chat_engine` object is assumed to have a `generate_doc` method that takes in code information and a file handler object, and returns a response message containing the generated documentation.
- The `json_data` dictionary is assumed to have the file path as the key and a dictionary of objects as the value.
- The `logger` object is assumed to have a `info` method for logging messages.
- The `CONFIG` dictionary is assumed to contain a key `'Markdown_Docs_folder'` which specifies the folder for storing the generated Markdown documentation.
## FunctionDef process_file_changes(self, repo_path, file_path, is_new_file):
**process_file_changes**: The function of this Function is to process changed files according to the absolute file path, including new files and existing files. It is called in the loop of detected changed files.

**parameters**: 
- repo_path (str): The path to the repository.
- file_path (str): The relative path to the file.
- is_new_file (bool): Indicates whether the file is new or not.

**Code Description**: 
- The function first creates a FileHandler object, passing the repository path and file path as parameters. This object will be used to perform operations on the changed file.
- It then reads the content of the file using the FileHandler's `read_file()` method and stores it in the `source_code` variable.
- The function calls the `parse_diffs()` method of the `change_detector` object (an instance of the ChangeDetector class) to get the changed lines in the file. It passes the result of the `get_file_diff()` method (which takes the file path and the `is_new_file` flag as parameters) as an argument.
- Next, the function calls the `identify_changes_in_structure()` method of the `change_detector` object to identify the changes in the file's structure. It passes the `changed_lines` and the result of the `get_functions_and_classes()` method of the `file_handler` object (which takes the `source_code` as a parameter) as arguments. The result is stored in the `changes_in_pyfile` variable.
- The function logs the detected changes using the `logger.info()` method.
- It then opens the `project_hierarchy.json` file and loads its content into the `json_data` variable.
- If the file path is found in the `json_data`, the function updates the corresponding item in the `json_data` using the `update_existing_item()` method, passing the `file_handler` and `changes_in_pyfile` as parameters.
- The function writes the updated `json_data` back to the `project_hierarchy.json` file.
- It logs that the json structure information of the file has been updated.
- The function converts the changed part of the json file to markdown content using the `convert_to_markdown_file()` method of the `file_handler` object, passing the `file_path` as a parameter. The result is stored in the `markdown` variable.
- It writes the markdown content to a `.md` file with the same name as the `.py` file, but with the extension changed, using the `write_file()` method of the `file_handler` object.
- The function logs that the markdown document of the file has been updated.
- If the file path is not found in the `json_data`, the function calls the `add_new_item()` method, passing the `file_handler` and `json_data` as parameters.
- The function calls the `add_unstaged_files()` method of the `change_detector` object to add the updated markdown files to the staging area.
- If there are files added to the staging area, the function logs the files that have been added.

**Note**: 
- This function is called in the loop of detected changed files, so it will be executed multiple times for different files.
- The function relies on the `FileHandler`, `ChangeDetector`, and `ProjectManager` classes to perform various operations on the files and project hierarchy.
- The function updates the project hierarchy JSON file with the changes detected in the file's structure.
- If the file is new, it adds a new item to the project hierarchy JSON file.
- It converts the changed part of the JSON file to a Markdown document and saves it as a `.md` file.
- The updated Markdown files are added to the staging area using Git commands.
## FunctionDef update_existing_item(self, file_dict, file_handler, changes_in_pyfile):
**update_existing_item**: The function of this Function is to update existing projects by modifying the file structure information dictionary based on the changes made in the file.

**parameters**: 
- file_dict (dict): A dictionary containing the file structure information.
- file_handler (FileHandler): The file handler object.
- changes_in_pyfile (dict): A dictionary containing information about the objects that have changed in the file.

**Code Description**: 
The function first calls the `get_new_objects` method to get the new and deleted objects in the file. It then iterates over the deleted objects and removes them from the `file_dict` dictionary. 

Next, it creates an empty list called `referencer_list` to store information about the objects that reference the added objects. 

The function generates the current file structure information by calling the `generate_file_structure` method of the `file_handler` object. It creates a dictionary called `current_info_dict` to store the current objects' information using their names as keys.

The function then updates the global file structure information in the `file_dict` dictionary. For each object in the `current_info_dict`, if the object exists in the `file_dict`, its information is updated. If the object does not exist in the `file_dict`, it is added to the dictionary.

Next, the function iterates over the added objects in the `changes_in_pyfile` dictionary. For each added object, it searches for the object's information in the `current_objects` dictionary. If a match is found, it calls the `find_all_referencer` method of the `project_manager` object to get a list of all the objects that reference the added object. It then adds the object's name and the referencer list to the `referencer_list`.

The function uses a `ThreadPoolExecutor` to concurrently update the objects in the `file_dict` dictionary. For each added object, it retrieves the corresponding referencer list from the `referencer_list` and submits a task to the executor to update the object using the `update_object` method. 

Finally, the function returns the updated `file_dict` dictionary.

**Note**: 
- The function assumes that the `get_new_objects`, `generate_file_structure`, and `find_all_referencer` methods are defined in the respective classes.
- The function uses a thread pool with a maximum of 5 workers to update the objects concurrently.

**Output Example**: 
```python
{
    "object1": {
        "type": "class",
        "code_start_line": 10,
        "code_end_line": 20,
        "parent": "module1",
        "name_column": 5
    },
    "object2": {
        "type": "function",
        "code_start_line": 30,
        "code_end_line": 40,
        "parent": "module1",
        "name_column": 10
    },
    ...
}
```
## FunctionDef update_object(self, file_dict, file_handler, obj_name, obj_referencer_list):
**update_object**: The function of this Function is to generate documentation content and update the corresponding field information of the object.

**parameters**: 
- file_dict (dict): A dictionary containing the old object information.
- file_handler: The file handler.
- obj_name (str): The object name.
- obj_referencer_list (list): The list of object referencers.

**Code Description**: 
The `update_object` function takes in a dictionary `file_dict` containing the old object information, a `file_handler`, the name of the object `obj_name`, and a list of object referencers `obj_referencer_list`. 

The function first checks if the `obj_name` exists in the `file_dict`. If it does, it retrieves the object from the dictionary and assigns it to the variable `obj`. 

Next, it calls the `generate_doc` method of the `chat_engine` object, passing in the `obj`, `file_handler`, and `obj_referencer_list` as arguments. The `generate_doc` method is responsible for generating the documentation content based on the object and its referencers.

The response message returned by the `generate_doc` method is then assigned to the `md_content` field of the `obj` dictionary.

**Note**: 
- This function is used to update the documentation content and field information of an object based on its existing information and referencers.
- The `file_dict` parameter should be a dictionary containing the old object information, where the keys are the object names and the values are dictionaries representing the object information.
- The `file_handler` parameter should be an instance of the file handler class.
- The `obj_name` parameter should be a string representing the name of the object to be updated.
- The `obj_referencer_list` parameter should be a list of object referencers.
## FunctionDef get_new_objects(self, file_handler):
**get_new_objects**: The function of this Function is to compare the current version and the previous version of a .py file and retrieve the added and deleted objects.

**parameters**: 
- file_handler (FileHandler): The file handler object used to retrieve the modified file versions.

**Code Description**:
The function first retrieves the current version and the previous version of the .py file using the `get_modified_file_versions()` method of the `file_handler` object. 

Then, it uses the `get_functions_and_classes()` method of the `file_handler` object to parse the current and previous versions of the .py file and retrieve the functions and classes.

The function creates sets of the names of the functions and classes in the current and previous versions.

It then calculates the added objects by subtracting the previous objects from the current objects, and calculates the deleted objects by subtracting the current objects from the previous objects.

Finally, the function returns a tuple containing the added and deleted objects.

**Note**: 
- The `file_handler` object must be an instance of the `FileHandler` class.
- The `get_modified_file_versions()` method of the `file_handler` object should return the current and previous versions of the .py file.
- The `get_functions_and_classes()` method of the `file_handler` object should return a list of tuples, where each tuple contains the type and name of a function or class.

**Output Example**:
new_obj: ['add_context_stack', '__init__']
del_obj: []
***
