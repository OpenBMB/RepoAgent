# FunctionDef get_import_statements:
**get_import_statements**: The function of this function is to retrieve the import statements from the source code.

**parameters**: This function does not take any parameters.

**Code Description**: The `get_import_statements` function uses the `inspect.getsourcelines` function to retrieve the source code lines of the current module. It then filters the source lines to find the lines that start with either 'import' or 'from'. These lines are considered import statements. The function returns a list of import lines.

**Note**: This function assumes that it is being called from within the module for which the import statements need to be retrieved.

**Output Example**: If the source code contains the following import statements:
```
import sys
from os import path
```
The function will return the following list:
```
['import sys', 'from os import path']
```
***
# ClassDef ChatEngine:
**ChatEngine**: The function of this Class is to generate the documentation for functions or classes.

**attributes**: This Class has one attribute:
- `config`: It stores the configuration settings.

**Code Description**: The `ChatEngine` Class has the following methods:

1. `__init__(self, CONFIG)`: This method is the constructor of the `ChatEngine` Class. It initializes the `config` attribute with the provided `CONFIG` parameter.

2. `num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int`: This method takes a text string as input and returns the number of tokens in the string. It uses the `tiktoken` library to encode the string and then calculates the length of the encoded tokens.

3. `generate_doc(self, doc_item: DocItem, file_handler)`: This method generates the documentation for a given `doc_item` object. It takes the `doc_item` and `file_handler` as parameters. It extracts the necessary information from the `doc_item` object, such as the code type, name, content, and whether it has a return value. It also checks if the code has been referenced by other objects or if it references other objects. It then constructs a system prompt and a user prompt based on the extracted information. The system prompt includes the project structure, code type, code name, code content, and whether it has a return value. The user prompt includes the desired language for the documentation. The method then uses the OpenAI GPT-3.5 Turbo model to generate the documentation based on the prompts. It makes use of the OpenAI API to send the prompts and receive the generated documentation. The generated documentation is returned as the output.

**Note**: The code makes use of the `ProjectManager` class from the `project_manager` module to get the project structure. It also uses the `tiktoken` library to encode the text string and calculate the number of tokens. The documentation generation process involves sending prompts to the OpenAI GPT-3.5 Turbo model using the OpenAI API.

**Output Example**: Mock up a possible appearance of the code's return value.
## FunctionDef __init__(self, CONFIG):
**__init__**: The function of this Function is to initialize an instance of the ChatEngine class.

**parameters**: 
- CONFIG: A configuration object that contains the settings for the chat engine.

**Code Description**: 
The `__init__` function is the constructor method of the ChatEngine class. It is called when a new instance of the class is created. The function takes a single parameter `CONFIG`, which is an object that contains the configuration settings for the chat engine.

Inside the function, the `CONFIG` object is assigned to the `config` attribute of the instance using the `self` keyword. This allows the configuration settings to be accessed by other methods within the class.

**Note**: 
- The `__init__` function is automatically called when a new instance of the ChatEngine class is created.
- The `CONFIG` parameter should be an object that contains the necessary configuration settings for the chat engine.
## FunctionDef num_tokens_from_string(self, string, encoding_name):
**num_tokens_from_string**: The function of this Function is to return the number of tokens in a text string.
**parameters**: 
- string: A string representing the text for which the number of tokens needs to be calculated.
- encoding_name (optional): A string representing the name of the encoding to be used. The default value is "cl100k_base".

**Code Description**: 
The `num_tokens_from_string` function takes a text string and an optional encoding name as input parameters. It uses the `tiktoken.get_encoding` function to retrieve the encoding based on the provided encoding name. The function then encodes the input string using the retrieved encoding and calculates the number of tokens in the encoded string using the `len` function. Finally, it returns the number of tokens as an integer.

**Note**: 
- The encoding name parameter is optional and has a default value of "cl100k_base". If no encoding name is provided, the function will use the default encoding.
- The `tiktoken.get_encoding` function is assumed to be defined elsewhere in the codebase.

**Output Example**: 
If the input string is "Hello, world!", and the encoding name is "cl100k_base", the function will return the number of tokens in the encoded string, which could be 3.
## FunctionDef generate_doc(self, doc_item, file_handler):
**generate_doc**: The function of this Function is to generate a detailed explanation document for a given object based on its code content and combine it with its calling situation in the project.

**parameters**: 
- `doc_item` (DocItem): The DocItem object representing the target object for which the documentation needs to be generated.
- `file_handler`: The FileHandler object used to handle the file operations.

**Code Description**: 
The `generate_doc` function takes in a `doc_item` object and a `file_handler` object as parameters. It first extracts the necessary information from the `doc_item` object, such as the code type, code name, code content, and whether the code has a return value. It also checks if the `doc_item` object has any references or is referenced by other objects.

Next, it retrieves the project structure using the `ProjectManager` class and prepares the necessary prompts for the OpenAI GPT-3 chat-based language model. It constructs a system prompt that includes information about the code type, code name, code content, whether it has a return value, and the project structure. It also includes prompts for the references and referencers of the `doc_item` object.

The function then makes a request to the OpenAI API using the configured language model. It sends the system prompt and a user prompt to generate a response. The response contains the generated documentation for the `doc_item` object.

**Note**: 
- The function uses the OpenAI GPT-3 chat-based language model to generate the documentation.
- The function handles potential errors, such as connection errors and exceeding the model's maximum context length.
- The function limits the code length to ensure it fits within the model's maximum token limit.

**Output Example**: 
Mock up a possible appearance of the code's return value.
### FunctionDef get_referenced_prompt(doc_item):
**get_referenced_prompt**: The function of this Function is to generate a prompt that displays the objects called by the code.

**parameters**: 
- doc_item: A DocItem object that contains information about the code item.

**Code Description**: 
The `get_referenced_prompt` function takes a `DocItem` object as input and returns a string prompt that displays the objects called by the code. 

The function first checks if the `doc_item` has any referenced objects. If there are no referenced objects, an empty string is returned.

If there are referenced objects, the function creates a list called `prompt` to store the prompt lines. The initial line of the prompt is a general description of the code calling the objects.

Then, the function iterates over each referenced object in the `doc_item.reference_who` list. For each referenced object, it generates a prompt line that includes the object's name, document, and raw code. The object's name is obtained using the `get_full_name` method of the `reference_item` object. The document is extracted from the `md_content` attribute of the `reference_item` object, and if it is empty, the prompt displays "None". The raw code is obtained from the `code_content` key in the `content` attribute of the `reference_item` object, and if it is not present, an empty string is displayed.

Each prompt line is then appended to the `prompt` list, followed by a line of equal signs as a separator.

Finally, the function joins all the prompt lines in the `prompt` list with newline characters and returns the resulting string.

**Note**: 
- This function assumes that the `doc_item` object has a `reference_who` attribute that is a list of `DocItem` objects representing the referenced objects.
- The prompt generated by this function is intended to provide information about the objects called by the code, including their names, documents, and raw code.

**Output Example**: 
As you can see, the code calls the following objects, their code and docs are as following:
obj: repo_agent/chat_engine.py/get_import_statements
Document: None
Raw code:
```
def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines
```
==========
### FunctionDef get_referencer_prompt(doc_item):
**get_referencer_prompt**: The function of this Function is to generate a prompt that displays the objects that reference the given `doc_item`.

**parameters**: 
- `doc_item` (type: DocItem): The `DocItem` object for which the referencers are to be displayed.

**Code Description**: 
The `get_referencer_prompt` function first checks if the `doc_item` has any objects that reference it. If there are no referencers, an empty string is returned.

If there are referencers, a prompt is generated to display the objects that reference the `doc_item`. The prompt starts with a header message indicating that the code has been referenced by the following objects.

Then, for each referencer, the function generates a prompt containing the following information:
- Object name (`obj`): The full name of the referencer object.
- Document (`Document`): The last line of the Markdown content of the referencer object, if available. Otherwise, it displays "None".
- Raw code: The code content of the referencer object, enclosed in triple backticks. If the code content is not available, it displays "None".
- Divider: A line of equal signs (`=`) to separate each referencer prompt.

The function appends each referencer prompt to a list of prompts. Finally, it joins all the prompts with newline characters and returns the generated prompt.

**Note**: 
- The `doc_item` is an object of the `DocItem` class, which contains information about a specific code item, such as its name, type, content, and references.
- The generated prompt provides information about the objects that reference the `doc_item`, including their names, documentation, and code content.
- If the referencer object does not have any Markdown content or code content, it is indicated as "None" in the prompt.
- The prompt uses triple backticks to enclose the raw code content for better readability.

**Output Example**: 
Also, the code has been referenced by the following objects, their code and docs are as following:
obj: repo_agent/chat_engine.py/get_import_statements
Document: None
Raw code:
```
def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines
```
==========
***
