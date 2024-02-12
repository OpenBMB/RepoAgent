## _function need_to_generate(doc_item, ignore_list)
**need_to_generate**: need_to_generate函数的功能是判断是否需要生成文档。

**参数**：
- doc_item: DocItem类型，表示文档项。
- ignore_list: List类型，表示忽略列表。

**代码描述**：
need_to_generate函数用于判断是否需要生成文档。首先，函数会检查文档项的状态，如果文档项的状态为"doc_up_to_date"，则表示文档已经是最新的，无需生成新的文档，函数直接返回False。接下来，函数会获取文档项的相对文件路径，并判断文档项的类型是否为文件、目录或仓库，如果是，则暂时不生成文档，函数返回False。然后，函数会遍历文档项的父节点链，直到找到文件节点为止。在遍历过程中，函数会判断当前文件是否在忽略列表中，或者是否在忽略列表的某个文件路径下，如果是，则跳过生成文档，函数返回False。如果遍历完父节点链仍未找到文件节点，则表示文档项不属于任何文件，函数返回False。最后，如果以上条件都不满足，则表示需要生成文档，函数返回True。

**注意**：
- need_to_generate函数用于判断是否需要生成文档。
- 需要正确设置文档项的状态和类型。
- 需要正确设置忽略列表，以排除不需要生成文档的文件。
- 函数返回True表示需要生成文档，返回False表示不需要生成文档。

**输出示例**：
以下是一个可能的代码返回值的示例：
```
True
```
## _function load_whitelist
**load_whitelist**: load_whitelist函数的功能是加载白名单数据。
**参数**：该函数没有参数。
**代码描述**：load_whitelist函数用于加载白名单数据。首先，它会检查CONFIG["whitelist_path"]是否为None。如果不为None，则会断言CONFIG["whitelist_path"]所指定的路径存在，如果路径不存在，则会抛出异常。然后，它会使用open函数打开CONFIG["whitelist_path"]指定的文件，并使用json.load函数将文件中的数据加载为JSON格式。最后，它会返回加载的白名单数据。如果CONFIG["whitelist_path"]为None，则会返回None。
**注意**：在使用该函数之前，需要确保CONFIG["whitelist_path"]的值正确设置，并且指定的文件存在且为JSON格式。
**输出示例**：返回加载的白名单数据，例如：[{"file_path": "path/to/file1", "label": "label1"}, {"file_path": "path/to/file2", "label": "label2"}, ...]
## _class Runner
Doc has not been generated...
### _function __init__(self)
Doc has not been generated...
### _function generate_doc_for_a_single_item(self, doc_item)
Doc has not been generated...
### _function first_generate(self)
Doc has not been generated...
### _function markdown_refresh(self)
**markdown_refresh**: markdown_refresh函数的作用是将目前最新的document信息写入到一个markdown格式的文件夹里。

**参数**：
- self: 当前对象

**代码描述**：
该函数首先使用self.runner_lock进行线程同步，然后获取所有的file节点列表file_item_list。接下来，对于file_item_list中的每个file_item，函数会递归检查该file_item内是否存在doc。如果不存在doc，则跳过该file_item。否则，函数会根据doc的内容生成markdown格式的文档，并将其写入到.md文件中。

函数内部定义了一个名为recursive_check的嵌套函数，用于检查一个file内是否存在doc。该函数首先判断doc_item的md_content是否为空，如果不为空，则返回True。否则，遍历doc_item的子节点，递归调用recursive_check函数，如果任意子节点存在doc，则返回True。如果遍历完所有子节点后仍未找到doc，则返回False。

函数还定义了一个名为to_markdown的嵌套函数，用于将doc_item及其子节点转换为markdown格式的文本。该函数首先根据doc_item的item_type和obj_name生成标题，然后根据doc_item的content中的params生成参数列表。接下来，函数将doc_item的最后一个md_content添加到markdown_content中，并遍历doc_item的子节点，递归调用to_markdown函数，将子节点的markdown内容添加到markdown_content中。最后，函数返回markdown_content。

在主函数中，函数遍历file_item的子节点，调用to_markdown函数生成markdown内容，并将所有子节点的markdown内容拼接为一个字符串markdown。然后，函数根据file_item的文件名生成.md文件的路径，并创建该路径的文件夹。最后，函数将markdown内容写入到.md文件中。

**注意**：
- 该函数需要在Runner类的实例上调用。
- 该函数会将目前最新的document信息写入到一个markdown格式的文件夹里。
- 如果一个file内不存在doc，则跳过该file。
- 生成的.md文件的路径是根据file的文件名生成的，文件名中的".py"会被替换为".md"。
- 生成的.md文件会保存在CONFIG['Markdown_Docs_folder']指定的文件夹中。

**输出示例**：
假设CONFIG['Markdown_Docs_folder']的值为"/path/to/markdown"，file_item的文件名为"file_name.py"，file_item的子节点有两个，分别为child1和child2。假设child1的item_type为"Type1"，obj_name为"Obj1"，md_content为["Content1"]；child2的item_type为"Type2"，obj_name为"Obj2"，md_content为["Content2"]。则调用markdown_refresh函数后，会生成两个.md文件，分别为"/path/to/markdown/file_name.md"和"/path/to/markdown/Type1_Obj1.md"，文件内容分别为：
```
# file file_name
Content1

## Type1 Obj1
Content1

# Type2 Obj2
Content2
```
#### _function recursive_check(doc_item)
**recursive_check**: recursive_check函数的功能是检查一个file内是否存在doc。

**参数**：该函数接受一个DocItem类型的参数doc_item，表示要检查的文档项。

**代码描述**：recursive_check函数首先判断传入的doc_item的md_content属性是否为空列表，如果不为空，则说明该文档项存在文档，函数返回True。接着，函数遍历doc_item的children属性，对每个子文档项递归调用recursive_check函数。如果递归调用返回True，则说明子文档项或其子孙文档项存在文档，函数返回True。如果遍历完所有子文档项后仍未返回True，则说明该文档项及其子孙文档项均不存在文档，函数返回False。

**注意**：在使用recursive_check函数时，需要注意以下几点：
- 参数doc_item必须是DocItem类型的对象。
- 函数返回值为布尔类型，表示文档项是否存在文档。

**输出示例**：以下是一个可能的函数返回值的示例：
```python
True
```
#### _function to_markdown(item, now_level)
**to_markdown**: to_markdown函数的功能是将DocItem对象转换为Markdown格式的文档内容。
**参数**：该函数接受两个参数：
· item: DocItem类型，表示要转换为Markdown的文档项对象。
· now_level: int类型，表示当前的层级。
**代码描述**：to_markdown函数通过递归的方式将DocItem对象及其子对象转换为Markdown格式的文档内容。首先，函数会根据当前层级生成对应数量的"#"字符，并与文档项的类型和名称拼接在一起，形成Markdown的标题。然后，函数会判断文档项的参数是否存在，如果存在则将参数列表拼接在标题后面。接下来，函数会将文档项的最新版本的文档内容拼接在标题下面。最后，函数会递归调用自身，将文档项的子对象转换为Markdown格式的文档内容，并将其拼接在当前文档内容的末尾。最终，函数会返回生成的Markdown文档内容。
**注意**：在使用to_markdown函数时，需要注意以下几点：
- 需要传入一个有效的DocItem对象作为参数。
- 需要传入一个有效的层级值作为参数。
- 函数会根据文档项的类型和名称生成Markdown的标题。
- 函数会将文档项的参数列表拼接在标题后面。
- 函数会将文档项的最新版本的文档内容拼接在标题下面。
- 函数会递归调用自身，将文档项的子对象转换为Markdown格式的文档内容。
**输出示例**：以下是一个可能的函数返回值的示例：
```python
## _class_function to_markdown
Doc has not been generated...
```
```python
### _class_function to_markdown
Doc has not been generated...
```
```python
#### _class_function to_markdown
Doc has not been generated...
```
```python
##### _class_function to_markdown
Doc has not been generated...
```
```python
###### _class_function to_markdown
Doc has not been generated...
```
```python
####### _class_function to_markdown
Doc has not been generated...
```
```python
######## _class_function to_markdown
Doc has not been generated...
```
```python
######### _class_function to_markdown
Doc has not been generated...
```
```python
########## _class_function to_markdown
Doc has not been generated...
```
```python
########### _class_function to_markdown
Doc has not been generated...
```
```python
############ _class_function to_markdown
Doc has not been generated...
```
```python
############# _class_function to_markdown
Doc has not been generated...
```
```python
############## _class_function to_markdown
Doc has not been generated...
```
```python
############### _class_function to_markdown
Doc has not been generated...
```
```python
################ _class_function to_markdown
Doc has not been generated...
```
```python
################# _class_function to_markdown
Doc has not been generated...
```
```python
################## _class_function to_markdown
Doc has not been generated...
```
```python
################### _class_function to_markdown
Doc has not been generated...
```
```python
#################### _class_function to_markdown
Doc has not been generated...
```
```python
##################### _class_function to_markdown
Doc has not been generated...
```
```python
###################### _class_function to_markdown
Doc has not been generated...
```
```python
####################### _class_function to_markdown
Doc has not been generated...
```
```python
######################## _class_function to_markdown
Doc has not been generated...
```
```python
######################### _class_function to_markdown
Doc has not been generated...
```
```python
########################## _class_function to_markdown
Doc has not been generated...
```
```python
########################### _class_function to_markdown
Doc has not been generated...
```
```python
############################ _class_function to_markdown
Doc has not been generated...
```
```python
############################# _class_function to_markdown
Doc has not been generated...
```
```python
############################## _class_function to_markdown
Doc has not been generated...
```
```python
############################### _class_function to_mark
### _function git_commit(self, commit_message)
**git_commit**: git_commit函数的功能是将更改提交到Git仓库。
**参数**：此函数的参数。
· commit_message：提交的消息。
**代码说明**：此函数使用subprocess模块调用git命令将更改提交到Git仓库。它接受一个commit_message参数，该参数是提交的消息。在函数内部，它使用subprocess.check_call函数来执行git commit命令，并传递了一些选项和参数。如果提交过程中出现错误，会捕获subprocess.CalledProcessError异常，并打印出错误消息。
**注意**：在使用此函数时，需要确保已经安装了Git，并且当前工作目录是一个Git仓库。提交消息应该是有意义的，以便在查看提交历史时能够理解每个提交的目的。
### _function run(self)
Doc has not been generated...
### _class_function process_file_changes(self, repo_path, file_path, is_new_file)
Doc has not been generated...
