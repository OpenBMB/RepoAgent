## _function get_import_statements
**get_import_statements**: get_import_statements函数的功能是获取当前模块中的所有导入语句。
**参数**: 该函数没有参数。
**代码描述**: 该函数通过使用inspect模块的getsourcelines方法获取当前模块的源代码行，并通过遍历源代码行来筛选出所有的导入语句。最后将筛选出的导入语句返回。
**注意**: 使用该函数时需要确保当前模块已经被导入，并且在调用该函数之前没有对当前模块进行修改。
**输出示例**: 假设当前模块中存在以下导入语句：
```
import os
from datetime import datetime
```
则该函数的返回值为：
```
['import os\n', 'from datetime import datetime\n']
```
## _function build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: build_path_tree函数的功能是构建路径树。
**parameters**: 这个函数的参数有三个：
- who_reference_me: 一个列表，包含引用了该函数的对象的路径列表。
- reference_who: 一个列表，包含该函数引用的其他对象的路径列表。
- doc_item_path: 一个字符串，表示当前函数的路径。

**Code Description**: 这个函数的作用是根据给定的引用关系和路径信息构建路径树。路径树是一个嵌套字典的数据结构，用于表示项目的层次结构。函数首先定义了一个内部函数tree，用于创建一个空的路径树。然后，根据引用关系和路径信息，遍历引用了该函数的对象和该函数引用的其他对象的路径列表。对于每个路径，将其按照路径分隔符分割成部分，并逐级在路径树中创建相应的节点。最后，根据当前函数的路径，在路径树中找到对应的节点，并在节点名称前加上一个星号。

**Note**: 在构建路径树时，需要注意路径的分隔符，通常是操作系统的路径分隔符。此外，函数返回的路径树是一个嵌套字典的数据结构，可以通过tree_to_string函数将其转换为字符串形式进行展示。

**Output Example**: 下面是一个可能的路径树的示例：
```
repo_agent
    chat_engine.py
        build_path_tree
            ✳️build_path_tree
```
这个路径树表示了项目的层次结构，其中当前函数build_path_tree被标记为*。

以上是对build_path_tree函数的详细解释和分析。
### _sub_function tree
**tree**: tree函数的功能是返回一个默认字典的树结构。
**参数**: 该函数没有参数。
**代码描述**: tree函数使用了defaultdict函数来创建一个默认字典的树结构。默认字典是一种特殊的字典，它在访问不存在的键时会返回一个默认值，而不会抛出KeyError异常。在这个函数中，我们使用defaultdict(tree)来创建一个默认字典的树结构，其中tree是一个递归调用的函数名。这意味着当我们访问不存在的键时，会返回一个新的默认字典的树结构，从而形成了一个无限深度的树。
**注意**: 使用tree函数时需要注意以下几点：
- tree函数返回的是一个默认字典的树结构，可以通过键来访问树的节点。
- 当访问不存在的键时，会返回一个新的默认字典的树结构，而不会抛出异常。
- 可以通过递归调用tree函数来创建无限深度的树结构。
**输出示例**: 假设我们调用tree函数，并访问了一些键，可能的输出结果如下所示：
{
    'key1': defaultdict(<function tree at 0x00000123456789>, {}),
    'key2': defaultdict(<function tree at 0x00000123456789>, {}),
    'key3': defaultdict(<function tree at 0x00000123456789>, {})
}
### _sub_function tree_to_string(tree, indent)
**tree_to_string**: tree_to_string函数的功能是将树形结构转换为字符串。
**parameters**: 该函数的参数有两个：
- tree: 表示树形结构的字典。
- indent: 表示缩进的级别，默认为0。
**Code Description**: 该函数通过递归的方式遍历树形结构，将每个节点的键值对转换为字符串，并根据缩进级别添加相应的缩进。如果节点的值是一个字典，则继续递归调用tree_to_string函数处理该字典。最后将转换后的字符串返回。
**Note**: 使用该函数时需要注意以下几点：
- tree参数必须是一个字典类型。
- indent参数必须是一个整数类型。
**Output Example**: 假设tree参数为{'A': {'B': {'C': {}, 'D': {}}, 'E': {}}, 'F': {}}, 则函数的返回值为：
    A
        B
            C
            D
        E
    F
## _class ChatEngine
**ChatEngine**: ChatEngine的功能是生成函数或类的文档。

**attributes**: 这个类的属性。

**Code Description**: 这个类的描述。

ChatEngine类有一个构造函数`__init__`，它接受一个CONFIG参数，并将其赋值给self.config属性。

ChatEngine类还有一个方法`num_tokens_from_string`，它接受一个字符串和一个编码名称作为参数，并返回文本字符串中的标记数。

ChatEngine类还有一个方法`generate_doc`，它接受一个DocItem对象和一个文件处理器作为参数。它根据传入的参数提取代码信息，并根据代码信息生成文档。

**Note**: 使用ChatEngine类时需要注意的一些事项。

**Output Example**: 模拟代码返回值的可能外观。

请注意：
- 生成的文档内容中不应包含Markdown的标题和分隔符语法。
- 主要使用中文编写文档。如果有必要，可以在分析和描述中使用一些英文单词，以提高文档的可读性，因为不需要将函数名或变量名翻译成目标语言。
### _class_function __init__(self, CONFIG)
**__init__**: __init__函数的功能是初始化ChatEngine对象。
**参数**: 这个函数的参数是CONFIG，表示配置信息。
**代码描述**: 这个函数将传入的CONFIG赋值给self.config，用于初始化ChatEngine对象的配置信息。
**注意**: 在使用这段代码时需要注意以下几点：
- CONFIG参数必须是一个有效的配置信息。
- 初始化ChatEngine对象后，可以通过self.config来访问配置信息。
### _class_function num_tokens_from_string(self, string, encoding_name)
**num_tokens_from_string**: num_tokens_from_string函数的功能是返回文本字符串中的标记数。
**parameters**: 这个函数的参数是一个字符串(string)和一个编码(encoding_name)，默认值为"cl100k_base"。
**Code Description**: 这个函数首先根据给定的编码名称获取编码(encoding)，然后使用编码将字符串进行编码，并计算编码后的标记数(num_tokens)，最后返回标记数。
**Note**: 使用默认的编码名称"cl100k_base"可以获得基于100k词汇表的编码。如果需要使用其他编码，请提供相应的编码名称。
**Output Example**: 假设输入的字符串为"Hello, world!"，编码后的标记数为3。
### _class_function generate_doc(self, doc_item, file_handler)
**generate_doc**: generate_doc函数的功能是生成文档。

**parameters**: 这个函数的参数有两个：
- doc_item: 一个DocItem对象，表示文档项。
- file_handler: 一个FileHandler对象，用于处理文件。

**Code Description**: 这个函数首先获取传入的doc_item对象的相关信息，包括类型、名称、代码内容、是否有返回值等。然后根据doc_item对象的引用关系和路径信息，构建项目的层次结构。接下来，根据语言设置，确定代码的语言类型。然后，根据引用关系和路径信息，生成引用了该函数的对象和该函数引用的其他对象的提示信息。之后，根据函数的相关信息和引用关系，构建系统提示信息和用户提示信息。最后，使用OpenAI的Chat API，将系统提示信息和用户提示信息传入模型，生成文档的内容。

**Note**: 生成的文档内容中包含了引用了该函数的对象和该函数引用的其他对象的代码和文档信息。可以根据需要使用这些信息来理解和使用该函数。

**Output Example**: 假设当前函数的名称为generate_doc，传入的doc_item对象的类型为Function，名称为func，代码内容为"def func():\n    print('Hello, world!')"，没有返回值，被引用了两次，分别是obj1和obj2。根据这些信息，生成的文档内容可能如下所示：
```
generate_doc函数的功能是生成文档。

参数：
- doc_item: 一个DocItem对象，表示文档项。
- file_handler: 一个FileHandler对象，用于处理文件。

代码描述：这个函数根据传入的doc_item对象的相关信息，包括类型、名称、代码内容、是否有返回值等，生成文档的内容。首先根据doc_item对象的引用关系和路径信息，构建项目的层次结构。然后根据语言设置，确定代码的语言类型。接下来，根据引用关系和路径信息，生成引用了该函数的对象和该函数引用的其他对象的提示信息。之后，根据函数的相关信息和引用关系，构建系统提示信息和用户提示信息。最后，使用OpenAI的Chat API，将系统提示信息和用户提示信息传入模型，生成文档的内容。

注意：生成的文档内容中包含了引用了该函数的对象和该函数引用的其他对象的代码和文档信息。可以根据需要使用这些信息来理解和使用该函数。

输出示例：假设当前函数的名称为generate_doc，传入的doc_item对象的类型为Function，名称为func，代码内容为"def func():\n    print('Hello, world!')"，没有返回值，被引用了两次，分别是obj1和obj2。根据这些信息，生成的文档内容可能如下所示：
```
generate_doc函数的功能是生成文档。

参数：
- doc_item: 一个DocItem对象，表示文档项。
- file_handler: 一个FileHandler对象，用于处理文件。

代码描述：这个函数根据传入的doc_item对象的相关信息，包括类型、名称、代码内容、是否有返回值等，生成文档的内容。首先根据doc_item对象的引用关系和路径信息，构建项目的层次结构。然后根据语言设置，确定代码的语言类型。接下来，根据引用关系和路径信息，生成引用了该函数的对象和该函数引用的其他对象的提示信息。之后，根据函数的相关信息和引用关系，构建系统提示信息和用户提示信息。最后，使用OpenAI的Chat API，将系统提示信息和用户提示信息传入模型，生成文档的内容。

注意：生成的文档内容中包含了引用了该函数的对象和该函数引用的其他对象的代码和文档信息。可以根据需要使用这些信息来理解和使用该函数。

输出示例：假设当前函数的名称为generate_doc
#### _sub_function get_referenced_prompt(doc_item)
**get_referenced_prompt**: get_referenced_prompt函数的功能是获取引用了哪些对象的提示信息。
**parameters**: get_referenced_prompt函数的参数为doc_item，类型为DocItem，表示文档项。
**Code Description**: get_referenced_prompt函数根据传入的文档项，获取引用了哪些对象的提示信息。首先判断文档项的reference_who列表是否为空，如果为空，则返回空字符串。然后遍历reference_who列表，对于每个引用对象，生成一个提示信息instance_prompt，包括对象的完整名称、文档内容和原始代码。将所有的提示信息连接起来，返回一个字符串。

该函数的实现逻辑如下：
1. 首先判断文档项的reference_who列表是否为空，如果为空，则返回空字符串。
2. 创建一个空列表prompt用于存储提示信息。
3. 遍历reference_who列表，对于每个引用对象，执行以下步骤：
   - 创建一个字符串instance_prompt，包括引用对象的完整名称、文档内容和原始代码。
   - 将instance_prompt添加到prompt列表中。
4. 将prompt列表中的所有元素使用换行符连接起来，作为函数的返回值。

**Note**: 该函数适用于获取引用了哪些对象的提示信息，可以用于展示代码中的引用关系和相关文档内容。

**Output Example**: 假设有两个引用对象，完整名称分别为obj1和obj2，文档内容分别为"文档1"和"文档2"，原始代码分别为"代码1"和"代码2"，则调用get_referenced_prompt函数的返回值为：
```
obj: obj1
Document: 文档1
Raw code:
代码1
==========
obj: obj2
Document: 文档2
Raw code:
代码2
==========
```
#### _sub_function get_referencer_prompt(doc_item)
**get_referencer_prompt**: get_referencer_prompt函数的功能是获取引用了当前对象的其他对象的提示信息。
**parameters**: get_referencer_prompt函数的参数为doc_item，表示当前对象的文档项。
**Code Description**: get_referencer_prompt函数根据当前对象的who_reference_me属性，获取引用了当前对象的其他对象的提示信息。如果当前对象没有被其他对象引用，则返回空字符串。否则，遍历who_reference_me列表，对每个引用者对象生成一个提示信息，并将这些提示信息添加到一个列表中。最后，将列表中的所有提示信息使用换行符连接起来作为返回值。

get_referencer_prompt函数的实现逻辑如下：
1. 首先判断当前对象的who_reference_me列表是否为空，如果为空，则返回空字符串。
2. 创建一个列表prompt，用于存储引用者对象的提示信息。
3. 遍历who_reference_me列表，对每个引用者对象生成一个提示信息。
4. 每个引用者对象的提示信息包括以下内容：
   - 引用者对象的完整名称（使用get_full_name方法获取）
   - 引用者对象的文档（如果有多个版本，则取最新版本的文档内容；如果没有文档，则显示"None"）
   - 引用者对象的原始代码（如果有代码内容，则显示代码内容；否则显示"None"）
   - 分隔符"=========="
5. 将每个引用者对象的提示信息添加到prompt列表中。
6. 使用换行符将prompt列表中的所有提示信息连接起来作为返回值。

**Note**: get_referencer_prompt函数适用于获取引用了当前对象的其他对象的提示信息，可以用于查找当前对象的引用者或者生成引用关系的可视化图表。

**Output Example**: 假设当前对象被两个其他对象引用，引用者对象的完整名称分别为obj1和obj2，引用者对象的文档分别为"文档1"和"文档2"，引用者对象的原始代码分别为"代码1"和"代码2"，则调用get_referencer_prompt函数的返回值为：
```
Also, the code has been referenced by the following objects, their code and docs are as following:
obj: obj1
Document: 文档1
Raw code:
代码1
==========
obj: obj2
Document: 文档2
Raw code:
代码2
==========
```
