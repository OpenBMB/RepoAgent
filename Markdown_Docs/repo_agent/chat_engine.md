## _function get_import_statements
**get_import_statements**: get_import_statements函数的功能是获取当前对象的导入语句列表。
**参数**: 这个函数没有参数。
**代码描述**: 这个函数首先使用inspect模块的getsourcelines函数获取当前对象的源代码行列表。然后，它使用列表推导式从源代码行列表中筛选出以'import'或'from'开头的行，将它们保存在import_lines列表中。最后，函数返回import_lines列表，即当前对象的导入语句列表。
**注意**: 使用这段代码时需要注意以下几点：
- 该函数没有参数，直接调用即可。
- 当前对象的导入语句列表是根据源代码动态生成的，因此在不同的环境中可能会有所不同。
**输出示例**: 下面是一个可能的返回值的示例：
```
['import sys\n', 'import inspect\n', 'import os\n']
```
## _function build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: build_path_tree函数的功能是构建路径树。
**参数**: build_path_tree函数接受三个参数:
- who_reference_me: 一个包含字符串路径的列表，表示引用当前对象的对象的路径列表。
- reference_who: 一个包含字符串路径的列表，表示当前对象引用的对象的路径列表。
- doc_item_path: 一个字符串，表示当前对象的文档路径。

**代码描述**: build_path_tree函数首先定义了一个内部函数tree，用于创建一个默认字典的树结构。然后，它创建了一个空的路径树path_tree。接下来，它遍历who_reference_me和reference_who两个路径列表，将每个路径按照分隔符(os.sep)分割成多个部分，然后将这些部分逐级添加到路径树中。接着，它处理doc_item_path，将其按照分隔符分割成多个部分，并在最后一个对象前面加上星号，然后将这些部分逐级添加到路径树中。最后，它定义了一个内部函数tree_to_string，用于将路径树转换为字符串表示。最后，它返回了路径树的字符串表示。

**注意**: 在使用build_path_tree函数时，需要确保传入正确的参数，包括who_reference_me、reference_who和doc_item_path。此外，需要注意路径的分隔符应该与操作系统相匹配。

**输出示例**:
```
├─ who_reference_me
│   ├─ path1
│   └─ path2
├─ reference_who
│   ├─ path3
│   └─ path4
└─ doc_item_path
    └─ ✳️path5
```
### _sub_function tree
**tree**: tree函数的功能是返回一个defaultdict(tree)对象。
**参数**: 该函数没有参数。
**代码描述**: 该函数的代码非常简单，只有一行代码。它使用了collections模块中的defaultdict类来创建一个默认值为tree的字典对象，并将其作为返回值返回。
**注意**: 使用该函数时需要先导入collections模块。
**输出示例**: 以下是该函数可能返回的结果示例:
```
defaultdict(<function tree at 0x00000123456789>, {})
```
### _sub_function tree_to_string(tree, indent)
**tree_to_string**: tree_to_string函数的功能是将树结构转换为字符串表示。
**参数**: 这个函数的参数。
- tree: 一个字典类型的树结构。
- indent: 可选参数，表示缩进的级别，默认为0。
**代码描述**: 这个函数通过递归的方式遍历树结构，并将每个节点的键值对转换为字符串表示。首先，函数会对树结构按键进行排序。然后，对于每个键值对，函数会根据缩进级别生成相应数量的空格，并将键添加到字符串s中。如果值是一个字典类型，则递归调用tree_to_string函数，并将缩进级别加1。最后，函数返回字符串s。
**注意**: 使用这段代码时需要注意以下几点：
- tree参数必须是一个字典类型的树结构。
- indent参数表示缩进的级别，可以根据需要进行调整。
**输出示例**: 对于给定的树结构，函数返回的字符串可能如下所示：
```
root
    node1
        leaf1
        leaf2
    node2
        leaf3
    node3
        leaf4
        leaf5
```
这个示例中，树结构包含一个根节点root，根节点下有三个子节点node1、node2和node3。其中，node1下有两个叶子节点leaf1和leaf2，node2下有一个叶子节点leaf3，node3下有两个叶子节点leaf4和leaf5。函数将树结构转换为字符串表示时，根节点和子节点之间使用不同级别的缩进进行区分，叶子节点不再缩进。
## _class ChatEngine
**ChatEngine**: ChatEngine的功能是生成函数或类的文档。
**attributes**: 这个类的属性。
**Code Description**: 这个类的描述。
ChatEngine是一个用于生成函数或类文档的类。它具有以下方法和属性：

- `__init__(self, CONFIG)`: 这是ChatEngine类的构造函数。它接受一个CONFIG参数，并将其赋值给self.config属性。

- `num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int`: 这个方法接受一个字符串参数和一个编码名称参数，并返回文本字符串中的标记数。

- `generate_doc(self, doc_item: DocItem, file_handler)`: 这个方法接受一个DocItem对象和一个文件处理器参数，并生成文档。

**Note**: 在使用这个类的代码中，需要注意以下几点：

- 在实例化ChatEngine对象时，需要传入一个CONFIG参数。
- 在调用num_tokens_from_string方法时，需要传入一个字符串参数和一个可选的编码名称参数。
- 在调用generate_doc方法时，需要传入一个DocItem对象和一个文件处理器参数。

**Output Example**: 这是代码返回值的一个示例。
### _class_function __init__(self, CONFIG)
**__init__**: __init__函数的作用是初始化ChatEngine对象。
**参数**: 这个函数的参数。
- CONFIG: 配置参数，用于初始化ChatEngine对象。
**代码描述**: 这个函数用于初始化ChatEngine对象，并将传入的配置参数赋值给对象的config属性。
**详细代码分析和描述**: 
在这个函数中，我们首先接收一个名为CONFIG的参数，该参数用于初始化ChatEngine对象。然后，我们将传入的CONFIG参数赋值给对象的config属性。这样，我们就可以在ChatEngine对象的其他方法中使用这个配置参数了。

**注意**: 
- 在创建ChatEngine对象时，需要传入一个有效的配置参数。
- 通过调用__init__函数，可以创建一个已经初始化的ChatEngine对象。
### _class_function num_tokens_from_string(self, string, encoding_name)
**num_tokens_from_string**: num_tokens_from_string函数的功能是返回文本字符串中的标记数量。
**参数**: 这个函数的参数。
- string: str类型，表示要计算标记数量的文本字符串。
- encoding_name: str类型，表示要使用的编码名称，默认为"cl100k_base"。
**代码描述**: 这个函数通过使用指定的编码将文本字符串编码为标记列表，并返回标记列表的长度，即标记数量。
- 首先，函数使用tiktoken.get_encoding(encoding_name)获取指定名称的编码。
- 然后，函数使用获取到的编码对文本字符串进行编码，并将结果保存在encoding变量中。
- 最后，函数返回编码后的标记列表的长度，即标记数量。
**注意**: 使用这段代码时需要注意以下几点：
- 参数string必须是一个有效的文本字符串。
- 参数encoding_name必须是一个有效的编码名称，否则会引发异常。
**输出示例**: 模拟代码返回值的可能外观。
例如，如果输入字符串为"Hello, world!"，编码名称为"cl100k_base"，则代码的返回值可能为7。
### _class_function generate_doc(self, doc_item, file_handler)
**generate_doc**: generate_doc函数的功能是生成代码文档。
**parameters**: generate_doc函数的参数包括doc_item和file_handler。
**Code Description**: generate_doc函数用于生成代码文档。首先，它从doc_item中获取代码信息，包括代码类型、代码名称、代码内容、是否有返回值等。然后，它判断代码是否被其他对象引用。接下来，它根据代码的引用情况和项目的层级结构生成项目结构信息。之后，它根据配置文件中的语言设置，确定代码的语言类型。然后，它根据代码的类型和是否有返回值，生成相应的提示信息。接着，它获取代码的引用和被引用情况，并生成相应的提示信息。最后，它使用OpenAI的API将系统提示和用户提示发送给模型，获取生成的文档内容。
**Note**: 使用时需要注意代码的长度限制，如果超过限制，需要使用更大的模型进行处理。
#### _sub_function get_referenced_prompt(doc_item)
**get_referenced_prompt**: get_referenced_prompt函数的功能是获取引用了该代码的对象的相关信息。
**参数**: 这个函数的参数是一个DocItem对象，表示文档项。
**代码描述**: 这个函数首先判断文档项的reference_who属性的长度是否为0，如果是0则返回空字符串。接着，函数会遍历文档项的reference_who属性，对于每一个引用了该代码的对象，函数会生成一个包含对象的全名、文档和原始代码的字符串，并将其添加到prompt列表中。最后，函数将prompt列表中的字符串用换行符连接起来并返回。
**注意**: 该函数依赖于DocItem对象的reference_who属性，如果该属性为空，则函数会返回空字符串。
**输出示例**: 假设有两个引用了该代码的对象，其相关信息如下：
obj: repo_agent/chat_engine.py/get_import_statements
Document: None
Raw code:```
def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines

```==========
obj: repo_agent/chat_engine.py/ChatEngine/generate_doc
Document: None
Raw code:```
def generate_doc():
    doc_item = DocItem()
    doc_item.reference_who = [get_referenced_prompt]
    return doc_item

```==========
则函数的返回值为：
As you can see, the code calls the following objects, their code and docs are as following:
obj: repo_agent/chat_engine.py/get_import_statements
Document: None
Raw code:```
def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines

```==========
obj: repo_agent/chat_engine.py/ChatEngine/generate_doc
Document: None
Raw code:```
def generate_doc():
    doc_item = DocItem()
    doc_item.reference_who = [get_referenced_prompt]
    return doc_item

```==========
#### _sub_function get_referencer_prompt(doc_item)
**get_referencer_prompt**: get_referencer_prompt函数的功能是获取引用了某个对象的所有对象的代码和文档信息。
**参数**: 这个函数的参数是一个DocItem对象，表示待查询的对象。
**代码描述**: 这个函数首先判断待查询对象是否被其他对象引用，如果没有被引用则返回空字符串。然后，函数会遍历所有引用了待查询对象的对象，获取它们的全名、文档信息和原始代码，并将它们拼接成一个字符串列表。最后，函数将字符串列表用换行符连接起来并返回。
**注意**: 使用这段代码时需要注意以下几点：
- 参数doc_item必须是一个有效的DocItem对象。
- 如果待查询对象没有被其他对象引用，则返回的字符串为空。
**输出示例**: 下面是一个可能的返回值的示例：
```
Also, the code has been referenced by the following objects, their code and docs are as following:
obj: repo_agent/chat_engine.py/get_import_statements
Document: None
Raw code:```
def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines

```==========
```
