## _function need_to_generate(doc_item, ignore_list)
Doc has not been generated...
## _function load_whitelist
**load_whitelist**: load_whitelist函数的功能是加载白名单数据。

**参数**：
- 无

**代码说明**：
load_whitelist函数用于加载白名单数据。首先，它会检查CONFIG["whitelist_path"]是否为None。如果不为None，则会断言CONFIG["whitelist_path"]指定的路径存在，如果不存在则会抛出异常。然后，它会使用"r"模式打开CONFIG["whitelist_path"]指定的文件，并使用json.load()方法将文件内容解析为JSON格式的数据。最后，它会返回解析后的白名单数据。

在项目中的调用关系如下：
- repo_agent/runner.py/Runner/__init__对象调用了load_whitelist函数。在该对象的代码中，首先创建了一个Runner对象，然后通过self.meta_info.white_list = load_whitelist()将加载的白名单数据赋值给self.meta_info.white_list属性。

**注意**：
- CONFIG["whitelist_path"]必须为一个存在的JSON文件路径，否则会抛出异常。

**输出示例**：
```python
[
    {
        "file_path": "path/to/file1.py",
        "allowed_methods": ["GET", "POST"]
    },
    {
        "file_path": "path/to/file2.py",
        "allowed_methods": ["GET"]
    },
    ...
]
```
## _class Runner
Doc has not been generated...
### _class_function __init__(self)
Doc has not been generated...
### _class_function get_all_pys(self, directory)
Doc has not been generated...
### _class_function generate_doc_for_a_single_item(self, doc_item)
Doc has not been generated...
### _class_function first_generate(self)
Doc has not been generated...
### _class_function markdown_refresh(self)
Doc has not been generated...
#### _sub_function recursive_check(doc_item)
Doc has not been generated...
#### _sub_function to_markdown(item, now_level)
Doc has not been generated...
### _class_function git_commit(self, commit_message)
Doc has not been generated...
### _class_function run(self)
Doc has not been generated...
### _class_function add_new_item(self, file_handler, json_data)
Doc has not been generated...
### _class_function process_file_changes(self, repo_path, file_path, is_new_file)
Doc has not been generated...
### _class_function update_existing_item(self, file_dict, file_handler, changes_in_pyfile)
Doc has not been generated...
### _class_function update_object(self, file_dict, file_handler, obj_name, obj_referencer_list)
Doc has not been generated...
### _class_function get_new_objects(self, file_handler)
Doc has not been generated...
