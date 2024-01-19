## _function build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: build_path_tree函数的功能是构建路径树。
**parameters**: build_path_tree函数的参数有三个：
- who_reference_me: 一个包含路径的列表，表示引用我的对象的路径列表。
- reference_who: 一个包含路径的列表，表示我引用的对象的路径列表。
- doc_item_path: 表示文档项的路径。

**Code Description**: build_path_tree函数首先定义了一个内部函数tree，用于创建一个默认字典的树结构。然后，函数创建了一个path_tree变量，用于存储路径树。

接下来，函数使用两个循环遍历who_reference_me和reference_who列表中的路径。对于每个路径，函数将其拆分为多个部分，并使用这些部分构建路径树。最后，函数处理doc_item_path，将其拆分为多个部分，并在最后一个对象前面加上星号。然后，函数使用这些部分构建路径树。

函数还定义了一个内部函数tree_to_string，用于将路径树转换为字符串。该函数使用递归的方式遍历路径树，并将每个节点的键和值添加到字符串中。

最后，函数返回路径树的字符串表示。

**Note**: 在使用build_path_tree函数时，需要确保传入正确的参数，并且参数的格式符合要求。此外，函数依赖于os模块，因此需要确保os模块已经导入。

**Output Example**: 
```
who_reference_me
    path1
        subpath1
            ✳️doc_item_path
    path2
        subpath2
            ✳️doc_item_path
reference_who
    path3
        subpath3
            ✳️doc_item_path
    path4
        subpath4
            ✳️doc_item_path
```
### _sub_function tree
**tree**: tree函数的功能是返回一个默认字典的树结构。

**parameters**: tree函数没有参数。

**Code Description**: tree函数通过调用defaultdict(tree)来创建一个默认字典的树结构。默认字典是一种特殊的字典，它可以在访问不存在的键时自动创建一个默认值。在这里，我们使用tree作为默认值，这样就可以创建一个无限深度的树结构。函数返回创建的树结构。

**Note**: 使用tree函数时需要注意以下几点：
- tree函数没有参数，直接调用即可。
- 返回的树结构是一个默认字典，可以通过键值对的方式进行访问和操作。

**Output Example**: 假设调用tree函数后，返回的树结构为{'A': {'B': {'C': {}, 'D': {}}, 'E': {}}, 'F': {}}。
### _sub_function tree_to_string(tree, indent)
**tree_to_string**: tree_to_string函数的功能是将树结构转换为字符串。
**parameters**: tree_to_string函数的参数有两个：
- tree: 一个树结构，以字典的形式表示。
- indent: 可选参数，表示缩进的层数，默认为0。
**Code Description**: tree_to_string函数通过递归的方式将树结构转换为字符串。它首先遍历树的每个节点，对于每个节点，它将节点的键加入到字符串中，并根据缩进层数添加相应的缩进。然后，如果节点的值是一个字典，它会递归调用tree_to_string函数，将该字典作为新的树结构进行处理。最后，函数返回生成的字符串。
**Note**: 使用该函数时需要注意以下几点：
- tree参数必须是一个字典，表示树结构。
- indent参数表示缩进的层数，可以根据需要进行调整。
**Output Example**: 假设tree参数为{'A': {'B': {'C': {}, 'D': {}}, 'E': {}}, 'F': {}}, 则函数的返回值为：
```
A
    B
        C
        D
    E
F
```
