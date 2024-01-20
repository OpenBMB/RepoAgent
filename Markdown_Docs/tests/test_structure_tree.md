## _function build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: build_path_tree函数的功能是构建路径树。
**parameters**: build_path_tree函数的参数有三个：
- who_reference_me: 一个包含引用当前对象的路径列表的列表。
- reference_who: 一个包含当前对象引用的路径列表的列表。
- doc_item_path: 当前对象的路径。

**Code Description**: build_path_tree函数首先定义了一个内部函数tree，用于创建一个默认字典的树结构。然后，创建了一个名为path_tree的树结构对象。

接下来，通过遍历who_reference_me和reference_who两个列表，将路径分割成部分，并将每个部分作为键，将其添加到path_tree中的相应位置。这样，就构建了一个包含所有引用关系的路径树。

然后，将doc_item_path也分割成部分，并在最后一个部分前面加上星号。然后，将该路径添加到path_tree中的相应位置。

最后，定义了一个名为tree_to_string的内部函数，用于将树结构转换为字符串。通过递归遍历树结构，将每个键和对应的值添加到字符串中，并根据层级缩进。最后，返回转换后的字符串。

**Note**: 使用该代码时需要注意以下几点：
- 输入的路径列表应该是一个包含多个路径的列表，每个路径应该是一个字符串。
- 输入的路径应该使用操作系统的路径分隔符进行分割。
- 函数返回的是一个字符串，表示构建的路径树的结构。

**Output Example**: 
```
tests
    test_structure_tree.py
        build_path_tree
            ✳️build_path_tree
```
### _sub_function tree
**tree**: tree函数的功能是返回一个defaultdict(tree)对象。
**parameters**: 该函数没有参数。
**Code Description**: tree函数使用了defaultdict和tree两个类。defaultdict是一个字典的子类，它重写了__missing__方法，当访问一个不存在的键时，会自动调用__missing__方法返回一个默认值。tree是一个递归的数据结构，它可以无限嵌套，每一层都是一个defaultdict(tree)对象。tree函数的作用就是返回一个空的defaultdict(tree)对象。
**Note**: 使用tree函数可以方便地创建一个多层嵌套的字典结构，每一层都是一个defaultdict(tree)对象，可以用于构建树形结构的数据。
**Output Example**: 
```
defaultdict(<function tree at 0x00000123456789>, {})
```
### _sub_function tree_to_string(tree, indent)
**tree_to_string**: tree_to_string函数的功能是将树结构转换为字符串。
**参数**: 这个函数的参数。
- tree: 一个树结构，以字典的形式表示。
- indent: 可选参数，表示缩进的级别，默认为0。
**代码描述**: 这个函数通过递归的方式遍历树结构，并将每个节点转换为字符串形式。它首先对树的键进行排序，然后根据缩进级别添加相应数量的空格。如果节点的值是一个字典，则递归调用tree_to_string函数，将子树转换为字符串，并添加到结果字符串中。最后，函数返回结果字符串。
**注意**: 使用这段代码时需要注意以下几点：
- tree参数必须是一个字典形式的树结构。
- indent参数表示缩进的级别，可以根据需要进行调整。
**输出示例**: 模拟代码返回值的可能外观。
```
root
    child1
        grandchild1
        grandchild2
    child2
        grandchild3
```
