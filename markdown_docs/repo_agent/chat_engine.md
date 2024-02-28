## ClassDef ContextLengthExceededError
**ContextLengthExceededError**: The function of ContextLengthExceededError is to signal that the input size has surpassed the model's context length limit.

**Attributes**: This class does not explicitly define any attributes beyond those inherited from its superclass, `Exception`.

**Code Description**: The `ContextLengthExceededError` class is a custom exception class that extends the built-in `Exception` class in Python. It is designed specifically for use within a chat engine or similar text processing systems where there is a predefined maximum context length that the system can handle. When the input text exceeds this maximum allowable length, an instance of `ContextLengthExceededError` is raised to indicate this specific type of error.

This class is intentionally simple, containing no additional methods or attributes beyond what it inherits from `Exception`. The primary purpose of defining this class is to provide a clear and specific type of error that can be caught and handled differently from other exceptions. This allows for more granular error handling in the application, enabling developers to provide more informative error messages or take specific actions when this error occurs.

The docstring of the class provides a concise explanation of the exception's purpose, which aids in code readability and maintenance. By adhering to the convention of extending the base `Exception` class, `ContextLengthExceededError` integrates seamlessly with Python's exception handling mechanisms.

**Note**: When using `ContextLengthExceededError` in a project, it is important to catch this exception at points where input length might exceed the model's limitations. This allows for graceful handling of the error, such as prompting the user to shorten their input or logging the event for further analysis. It is a best practice to document the specific context length limit of the model in the sections of the code where this exception might be raised, to aid in clarity and maintainability.
## FunctionDef get_import_statements
**get_import_statements**: The function of get_import_statements is to retrieve all import statements from the source code of the current module.

**Parameters**: This function does not take any parameters.

**Code Description**: The `get_import_statements` function operates by first utilizing the `inspect.getsourcelines` method to obtain the source lines of the current module. This is achieved by passing `sys.modules[__name__]` to `getsourcelines`, where `__name__` represents the name of the current module, and `sys.modules` is a dictionary that maps module names to module objects. The `[0]` at the end of the `getsourcelines` call is used to access the first item in the returned tuple, which contains the list of source lines.

Once the source lines are obtained, the function iterates over each line, filtering for lines that either start with "import" or "from" after being stripped of leading and trailing whitespace. This is accomplished through a list comprehension, which checks if `line.strip().startswith("import")` or `line.strip().startswith("from")` for each line in the source lines.

The filtered lines, which are the import statements, are then returned as a list.

**Note**: This function is particularly useful for dynamic analysis of a module's dependencies, allowing developers to programmatically access the import statements used within a module. It is important to note that this function will only retrieve import statements that are statically defined in the source code of the module at the time of its execution. Dynamically generated import statements executed at runtime may not be captured.

**Output Example**:
```python
[
    "import sys",
    "from inspect import getsourcelines"
]
```
This example output shows a possible return value from the `get_import_statements` function, where the current module has two import statements: one importing the `sys` module and another importing the `getsourcelines` function from the `inspect` module.
## FunctionDef build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: The function of `build_path_tree` is to construct a hierarchical tree structure representing the relationships between different parts of a project based on references among them.

**Parameters**:
- `who_reference_me`: A list of paths indicating which objects are referenced by the current object.
- `reference_who`: A list of paths indicating which objects the current object references.
- `doc_item_path`: The path of the current documentation item, used to mark its position in the generated tree.

**Code Description**:
The `build_path_tree` function plays a crucial role in visualizing the structure and dependencies within a project. It takes two lists of paths (`who_reference_me` and `reference_who`) that represent the relationships between different components of the project, as well as the path of the current item being documented (`doc_item_path`). The function constructs a tree where each node represents a directory or file, and the structure reflects the hierarchy and references within the project.

The function begins by creating a nested dictionary structure using a recursive `tree` function, which utilizes `defaultdict` to facilitate the dynamic addition of nodes. It then iterates over both lists of paths, splitting each path into its components and incrementally building out the tree structure by traversing and adding nodes according to the parts of each path.

After processing both lists, the function modifies the `doc_item_path` by appending a star symbol (`✳️`) to the last component, which marks the current documentation item within the tree. This is followed by integrating this modified path into the tree structure in a similar manner.

To convert the nested dictionary structure into a human-readable string representation, the `tree_to_string` helper function is employed. It recursively traverses the tree, indenting each level to reflect the hierarchy, and returns a string that visually represents the project's structure.

This function is integral to the documentation generation process in the `ChatEngine` class, specifically within the `generate_doc` method. It provides a visual representation of the project's structure, highlighting the current object's position and its relationships with other components. This aids in understanding the context and dependencies of the documented item within the overall project.

**Note**:
- The paths in `who_reference_me` and `reference_who` should use the operating system's file separator (`os.sep`) for compatibility.
- The function assumes that the input paths are correctly formatted and relevant to the project's structure.
- The generated tree structure is a simplified representation and may not include all details of the actual file system or project architecture.

**Output Example**:
Assuming a project structure and the current documentation item's path, the output might look like this:

```
repo_agent
    chat_engine.py
        build_path_tree
            ✳️build_path_tree
```

This example demonstrates a part of the tree structure, with the current item (`build_path_tree`) marked with a star symbol, indicating its position within the project hierarchy.
### FunctionDef tree
**Function**: tree

**Function of tree**: The function creates a recursive defaultdict structure.

**Parameters**: This function does not take any parameters.

**Code Description**: The `tree` function is designed to generate a recursive data structure using Python's `defaultdict` from the `collections` module. The key feature of this function is its ability to infinitely nest dictionaries, allowing for the creation of a tree-like structure. This is achieved by passing the `tree` function itself as the default factory to `defaultdict`. When a new key is accessed that does not exist, instead of raising a KeyError, it automatically creates another `defaultdict` with the same properties, thus allowing for the creation of deeply nested structures on the fly.

**Note**: This function is particularly useful in scenarios where one needs to build a dynamically growing tree structure, such as parsing hierarchical data or building a nested menu system. It's important to be cautious with its use, as it's easy to inadvertently create very deep or infinite structures, which can lead to issues like maximum recursion depth errors or significant memory usage.

**Output Example**:
```python
# Creating a nested structure with the tree function
nested_dict = tree()
nested_dict['Europe']['Germany']['Bavaria'] = 'Munich'

# Accessing the nested structure
print(nested_dict['Europe']['Germany']['Bavaria'])
# Output: Munich

# Attempting to access a non-existent key creates new branches automatically
print(nested_dict['Europe']['Italy']['Tuscany'])
# Output: defaultdict(<function tree at 0x...>, {})
```

In the output example, accessing `nested_dict['Europe']['Germany']['Bavaria']` returns 'Munich', demonstrating how values can be assigned to deeply nested keys. Additionally, attempting to access `nested_dict['Europe']['Italy']['Tuscany']`, a path that has not been explicitly created, does not raise an error. Instead, it shows that a new branch has been automatically created, illustrating the recursive and auto-vivifying nature of the `tree` function.
***
### FunctionDef tree_to_string(tree, indent)
**tree_to_string**: The function of `tree_to_string` is to convert a hierarchical tree structure into a formatted string representation.

**Parameters**:
- `tree`: A dictionary representing the tree structure where each key-value pair corresponds to a node and its children. The children of a node are also represented as a dictionary.
- `indent`: An integer representing the current indentation level for formatting the string representation. It defaults to 0, meaning no indentation for the root level.

**Code Description**:
The `tree_to_string` function iterates through each key-value pair in the `tree` dictionary. The keys and values represent nodes and their children, respectively. The function sorts the keys of the dictionary to ensure a consistent order in the output string.

For each key-value pair, the function appends the key to the output string `s`, prefixed by a number of spaces that corresponds to the current `indent` level. Each key is followed by a newline character to format the tree structure vertically.

If the value associated with a key is itself a dictionary (indicating the presence of child nodes), the function recursively calls itself with the child dictionary and an incremented `indent` value. This recursive call allows the function to traverse the tree depth-first and to increase the indentation level for each level of depth, thereby formatting the tree structure appropriately in the string representation.

The function returns the formatted string `s` after iterating through all key-value pairs in the tree.

**Note**:
- The function assumes that the input `tree` is a properly structured dictionary that represents a tree. Each node's children must also be represented as dictionaries for the function to work correctly.
- The initial call to `tree_to_string` should typically be made with the default `indent` value unless a specific indentation is required from the outset.

**Output Example**:
Given a tree represented by the following dictionary:
```python
{
    "Fruits": {
        "Tropical": {
            "Mango": {},
            "Papaya": {}
        },
        "Temperate": {
            "Apple": {},
            "Cherry": {}
        }
    },
    "Vegetables": {
        "Leafy": {
            "Spinach": {},
            "Kale": {}
        },
        "Root": {
            "Carrot": {},
            "Potato": {}
        }
    }
}
```
The output of `tree_to_string(tree)` might look like this:
```
Fruits
    Temperate
        Apple
        Cherry
    Tropical
        Mango
        Papaya
Vegetables
    Leafy
        Kale
        Spinach
    Root
        Carrot
        Potato
```
This output represents the tree structure in a human-readable format, with indentation used to denote the hierarchy of nodes.
***
## ClassDef ChatEngine
**ChatEngine**: The function of ChatEngine is to facilitate the generation of documentation for functions or classes within a software project.

**Attributes**:
- `config`: A configuration dictionary that stores settings and preferences for the ChatEngine instance.

**Code Description**:
The ChatEngine class is designed to automate the documentation process for software projects. It primarily focuses on generating documentation based on the code structure and relationships within the project. The class is initialized with a configuration dictionary, which can include various settings such as language preferences, API keys, and model configurations for documentation generation.

One of the key methods in ChatEngine is `num_tokens_from_string`, which calculates the number of tokens in a given string based on a specified encoding. This method is crucial for understanding the complexity and size of the documentation content in terms of language model processing limits.

The `generate_doc` method is the core functionality of ChatEngine, where it takes a `DocItem` object representing a piece of code (function or class) and a file handler. It constructs a detailed documentation prompt by analyzing the code's structure, its relationships with other code entities (who references it and whom it references), and its position within the project's hierarchy. This method intelligently handles various aspects such as determining the code type (class or function), managing documentation tokens, and generating relationship descriptions between different code entities.

The class also includes private methods like `get_referenced_prompt` and `get_referencer_prompt`, which generate textual descriptions of the code's relationships with other entities in the project. These methods are essential for creating a comprehensive documentation that not only explains the code itself but also its context and interactions within the larger project structure.

Furthermore, ChatEngine handles the complexity of generating documentation by considering the limitations of the underlying language model used for documentation generation. It attempts to find an appropriate balance between the detail of the documentation and the constraints of the model, such as token limits. In cases where the documentation content exceeds these limits, ChatEngine employs strategies to reduce the content size or switch to a model that supports a larger context window.

**Note**:
- The effectiveness of the ChatEngine in generating accurate and comprehensive documentation heavily relies on the configuration settings provided during initialization. It is crucial to ensure that these settings, especially those related to the language model and API keys, are correctly configured.
- The class assumes the presence of a structured project hierarchy and inter-code relationships. Proper tagging and referencing within the project's codebase are essential for maximizing the utility of ChatEngine.

**Output Example**:
An example output of the ChatEngine's `generate_doc` method might include a detailed description of a function, its parameters, return values, and examples of usage. Additionally, it would provide information about the function's relationships with other parts of the project, such as which classes or functions call it and which ones it calls, enhancing the understanding of the function's role within the overall project architecture.

In the context of its usage within the project, ChatEngine is utilized by the `Runner` class in `repo_agent/runner.py`, indicating its role in automating documentation tasks as part of the project's build or maintenance processes. This relationship underscores the importance of ChatEngine in supporting developers by providing up-to-date and comprehensive documentation, facilitating better understanding and navigation of the project's codebase.
### FunctionDef __init__(self, CONFIG)
**__init__**: The function of `__init__` is to initialize a new instance of the ChatEngine class.

**Parameters**:
- `CONFIG`: A configuration object or dictionary containing settings and parameters required by the ChatEngine.

**Code Description**:
The `__init__` method is a special method in Python, commonly known as a constructor. This method is automatically called when a new instance of a class is created. In the context of the ChatEngine class, the `__init__` method is designed to perform initial setup for the instance.

The method takes a single parameter, `CONFIG`, which is expected to be a configuration object or a dictionary. This parameter allows for flexible and dynamic initialization of the ChatEngine instance, as it can carry various configuration settings required for the operation of the chat engine. These settings might include, but are not limited to, API keys, database connection information, or custom settings specific to the chat engine's functionality.

Within the body of the `__init__` method, the provided `CONFIG` parameter is assigned to an instance variable named `config`. This assignment makes the configuration settings accessible throughout the instance, allowing other methods within the ChatEngine class to utilize these settings as needed.

**Note**:
It is important to ensure that the `CONFIG` parameter provided during the instantiation of the ChatEngine class contains all the necessary configuration settings. Missing or incorrect configuration could lead to unexpected behavior or errors in the chat engine's operation. Additionally, the structure and content of the `CONFIG` object should be well-documented, making it easier for developers to understand and use the ChatEngine class effectively.
***
### FunctionDef num_tokens_from_string(self, string, encoding_name)
**num_tokens_from_string**: The function of num_tokens_from_string is to return the number of tokens in a text string.

**Parameters**:
- **string (str)**: The text string to be tokenized.
- **encoding_name (str)**: The name of the encoding to use for tokenization, with a default value of "cl100k_base".

**Code Description**:
The `num_tokens_from_string` function is a method within the `ChatEngine` class, designed to calculate the number of tokens that a given string can be divided into, based on a specified encoding. This process begins by retrieving the encoding details using the `tiktoken.get_encoding` function, which takes the `encoding_name` as its argument. Once the encoding is obtained, the string is encoded using the `encode` method of the retrieved encoding object. The length of the resulting encoded list represents the number of tokens the input string contains. This value is then returned as the function's output.

In the context of the `ChatEngine` class, this method plays a crucial role in understanding and processing natural language inputs. By determining the number of tokens in a string, the `ChatEngine` can make informed decisions about handling user inputs, such as generating responses or performing further natural language processing tasks.

The `num_tokens_from_string` method is utilized by the `generate_doc` method within the same `ChatEngine` class. The `generate_doc` method is responsible for generating documentation for different components of the project, including functions and classes. It uses `num_tokens_from_string` to calculate the total number of tokens in the system and user prompts, which is essential for managing the input size for machine learning models that generate the documentation. This relationship highlights the method's utility in managing and optimizing the generation of dynamic content based on natural language inputs.

**Note**:
It is important to ensure that the encoding name provided as a parameter to this function matches one of the encodings supported by the `tiktoken` library. Using an unsupported encoding name will result in an error. The default encoding, "cl100k_base", is typically suitable for a wide range of applications, but different encodings can be specified to better suit specific needs or languages.

**Output Example**:
Suppose the input string is "Hello, world!" and the default encoding "cl100k_base" is used. If this encoding translates the input string into 3 tokens, the function would return:

```
3
```

This output indicates that the string "Hello, world!" consists of 3 tokens according to the specified encoding.
***
### FunctionDef generate_doc(self, doc_item, file_handler)
**generate_doc**: The function of `generate_doc` is to generate documentation for a given documentation item within a software project's repository.

**Parameters**:
- `doc_item`: An instance of `DocItem` representing the documentation item for which documentation is to be generated.
- `file_handler`: A file handler object that provides methods for file operations and access to repository paths.

**Code Description**:
The `generate_doc` function is a method within the `ChatEngine` class, designed to automate the documentation process for software projects. It takes a documentation item (`doc_item`) and a file handler as inputs and generates documentation based on the content and references associated with the `doc_item`.

The function begins by extracting information from the `doc_item`, such as the type of code (class or function), the name, the actual code content, and whether it has a return value. It also retrieves lists of objects that the current item references (`reference_who`) and objects that reference the current item (`who_reference_me`), along with their respective names.

A significant part of the function involves building a project structure tree that visually represents the hierarchical relationship of the documentation item within the project. This is achieved by calling the `build_path_tree` function with the lists of references and the documentation item's path.

The function then generates prompts for referenced objects and referencers, providing insights into how the current item interacts with other parts of the project. These prompts include the names, documentation, and raw code of the referenced and referencer objects.

Additionally, the function configures language settings based on the project's configuration and prepares a system prompt that includes detailed instructions for generating the documentation. This prompt incorporates the project structure, code information, and reference relationships.

The documentation generation process involves sending the prepared prompts to an AI model, which returns the generated documentation. The function handles potential issues such as exceeding the maximum token limit by adjusting the input or switching to a model that supports a larger input.

Throughout the process, the function makes several attempts to generate the documentation, handling connection errors and retrying as necessary. If successful, the generated documentation is returned; otherwise, the function may return `None` or raise an error after exhausting all attempts.

**Note**:
- The function relies on external configurations and models for language processing and documentation generation. Ensure that the project's configuration is correctly set up with valid API keys and model settings.
- The function handles complex relationships between documentation items, including references and referencers. Accurate and comprehensive documentation requires that these relationships are correctly established in the `DocItem` instances.

**Output Example**:
Due to the dynamic nature of the documentation generation process, the output is contingent on the input `doc_item` and the project's structure. The generated documentation will typically include a description of the item, its parameters or attributes, usage examples, and information about its relationships within the project.
#### FunctionDef get_referenced_prompt(doc_item)
**get_referenced_prompt**: The function of `get_referenced_prompt` is to generate a detailed prompt string that lists all the objects referenced by a given documentation item, including their names, documentation content, and raw code.

**Parameters**:
- `doc_item`: This parameter is of type `DocItem` and represents the documentation item for which the referenced prompt is being generated.

**Code Description**:
The `get_referenced_prompt` function begins by checking if the `doc_item` parameter has any referenced objects in its `reference_who` attribute. If there are no referenced objects, the function returns an empty string, indicating that there are no references to display.

If there are referenced objects, the function constructs a prompt string that starts with a predefined message indicating that the code calls certain objects, and their code and documentation will follow. For each referenced object, the function appends to the prompt string the full name of the object (obtained through the `get_full_name` method of the referenced object), the last entry of its markdown documentation content (if available), and its raw code content. The raw code content is included only if the `code_content` key exists in the referenced object's `content` dictionary. Each referenced object's information is separated by a series of equal signs (`=`) for clear visual separation.

The function iterates over all objects referenced by the `doc_item`, appending each object's detailed information to the prompt string. Finally, the function returns the complete prompt string, which includes the documentation and code for all referenced objects.

**Note**:
- This function is crucial for generating documentation that includes references to other parts of the project. It helps in understanding the dependencies and relationships between different components of the project.
- The function assumes that the `reference_who` attribute of the `doc_item` parameter correctly lists all objects that the documentation item references. It is important to maintain accurate reference tracking within the project to ensure the generated prompt is complete and accurate.
- The inclusion of raw code in the prompt is designed to provide a comprehensive view of the referenced objects, but it may also include sensitive information. Consider this when using the function in environments where code confidentiality is a concern.

**Output Example**:
```
As you can see, the code calls the following objects, their code and docs are as following:
obj: repo_agent/doc_meta_info.py/DocItem
Document: 
**DocItem**: The function of DocItem is to represent a documentation item within a software project's repository...
Raw code:```
class DocItem:
    item_type: DocItemType = DocItemType._class_function
    ...
```==========
obj: repo_agent/doc_meta_info.py/DocItem/get_full_name
Document: 
**get_full_name**: The function of `get_full_name` is to generate a string representation of the hierarchical path...
Raw code:```
    def get_full_name(self, strict = False):
        ...
```==========
```
This output example demonstrates how the function generates a prompt that includes detailed information about each object referenced by the documentation item, facilitating a deeper understanding of the project's structure and dependencies.
***
#### FunctionDef get_referencer_prompt(doc_item)
**get_referencer_prompt**: The function of `get_referencer_prompt` is to generate a string prompt detailing objects that have called the given documentation item, including their documentation and raw code.

**Parameters**:
- `doc_item`: A `DocItem` instance representing the documentation item for which the referencer prompt is being generated.

**Code Description**:
The `get_referencer_prompt` function starts by checking if the `doc_item` has any objects that reference it, indicated by the `who_reference_me` attribute of the `DocItem` class. If there are no such objects, the function returns an empty string, indicating that there are no referencers to document.

If there are objects that reference the `doc_item`, the function constructs a prompt starting with a predefined message indicating that the code has been called by other objects. It then iterates over each object in the `who_reference_me` list of the `doc_item`. For each referencer object, it generates a detailed prompt that includes:
- The full name of the referencer object obtained via the `get_full_name` method.
- The most recent markdown documentation of the referencer object, if available, or 'None' if not.
- The raw code content of the referencer object, if available in its `content` dictionary under the key 'code_content', or 'None' if not.

Each referencer object's details are appended to a list, which is then joined into a single string with newline characters for separation, and returned.

This function is crucial for generating documentation that provides insights into how different parts of the project are interconnected. By detailing which objects call a given documentation item, it helps developers understand dependencies and the impact of changes in the codebase.

**Note**:
- The function assumes that each `DocItem` object has a correctly populated `who_reference_me` list. This list should be maintained as part of the documentation generation and updating process.
- The output of this function is intended for inclusion in documentation files, where it can provide valuable context about the usage and importance of different code elements.

**Output Example**:
Assuming `doc_item` is referenced by two objects, the output might look like this:

```
Also, the code has been called by the following objects, their code and docs are as following:
obj: repo_agent/chat_engine.py/ChatEngine
Document: 
None
Raw code:```
class ChatEngine:
    def __init__(self):
        pass
```
==========
obj: repo_agent/utils.py/UtilityFunction
Document: 
**UtilityFunction**: This function helps with...
Raw code:```
def UtilityFunction():
    pass
```
==========
```

This output provides a clear and detailed view of the objects referencing the `doc_item`, including their documentation and code, which is invaluable for understanding the context and relationships within the project.
***
#### FunctionDef get_relationship_description(referencer_content, reference_letter)
**get_relationship_description**: The function of get_relationship_description is to generate a description of the relationship between different components in a project from a functional perspective, based on the provided parameters.

**Parameters**:
- **referencer_content**: This parameter is expected to be a truthy value if there is content that references other components within the project. It indicates the presence of callers in the relationship.
- **reference_letter**: This parameter is expected to be a truthy value if there is a reference to the component from other parts of the project. It indicates the presence of callees in the relationship.

**Code Description**:
The `get_relationship_description` function plays a crucial role in providing insights into the functional relationships within a project. It evaluates the presence of referencer content and reference letters to determine the nature of the relationship between components. The function operates under the following logic:
- If both `referencer_content` and `reference_letter` are provided and truthy, it implies that the component in question has both callers and callees within the project. In this case, the function prepares a description that requests the inclusion of the reference relationship from both perspectives.
- If only `referencer_content` is truthy, this indicates that the component has callers but not necessarily callees. The function then generates a description focusing on the relationship with its callers.
- Conversely, if only `reference_letter` is truthy, it suggests that the component is referenced by other components (callees) but does not reference others. The function returns a description centered on the relationship with its callees.
- If neither parameter is truthy, it indicates that there is no functional relationship to describe, and the function returns an empty string.

**Note**:
It is important for developers to accurately provide the `referencer_content` and `reference_letter` parameters based on the actual relationships within the project. Misinterpretation or incorrect values can lead to inaccurate descriptions of the project's architecture and functionality.

**Output Example**:
- If both parameters are truthy: "And please include the reference relationship with its callers and callees in the project from a functional perspective"
- If only `referencer_content` is truthy: "And please include the relationship with its callers in the project from a functional perspective."
- If only `reference_letter` is truthy: "And please include the relationship with its callees in the project from a functional perspective."
- If neither parameter is truthy: "" (an empty string)
***
***
