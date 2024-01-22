## _function build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: build_path_tree函数的功能是构建路径树。

**参数**：
· who_reference_me: 引用我的路径列表
· reference_who: 我引用的路径列表
· doc_item_path: 文档项的路径

**代码说明**：
build_path_tree函数用于构建路径树。路径树是一个嵌套的字典结构，用于表示文件系统中的路径关系。

首先，函数内部定义了一个辅助函数tree，用于创建一个默认字典的树结构。

然后，函数创建了一个空的路径树path_tree。

接下来，函数通过遍历who_reference_me和reference_who两个路径列表，将路径拆分为多个部分，并将每个部分作为键，将路径树的节点更新为下一级节点。这样，路径树就会根据路径列表中的路径关系进行构建。

然后，函数处理doc_item_path，将其拆分为多个部分，并在最后一个对象的前面加上星号。然后，函数将路径树的节点更新为下一级节点，以构建路径树的最后一个对象。

最后，函数定义了一个辅助函数tree_to_string，用于将路径树转换为字符串形式。函数通过递归遍历路径树的每个节点，将节点的键和值转换为字符串，并添加相应的缩进。

最后，函数返回路径树的字符串表示。

**注意**：
- 函数依赖于os模块，需要在使用之前导入os模块。
- 函数返回的是路径树的字符串表示，可以根据需要进行进一步处理或输出。

**输出示例**：
```
├─ who_reference_me
│   ├─ path1
│   ├─ path2
│   └─ path3
├─ reference_who
│   ├─ path4
│   └─ path5
└─ ✳️doc_item_path
```
### _function tree
**tree**: tree函数的功能是返回一个defaultdict(tree)对象。
**参数**：这个函数没有参数。
**代码说明**：这个函数返回一个defaultdict(tree)对象，defaultdict是Python中的一个内置字典类型，它可以在访问不存在的键时返回一个默认值。在这个函数中，我们使用了defaultdict的一个特殊用法，即将其初始化为一个tree对象。tree对象是一个递归的数据结构，它可以用来表示树形结构。当我们访问一个不存在的键时，defaultdict(tree)会自动创建一个新的tree对象作为该键的值，这样就可以方便地构建树形结构。
**注意**：在使用这个函数时，需要先导入defaultdict和tree类。另外，由于tree对象是一个递归的数据结构，所以在使用时需要注意避免出现无限递归的情况。
**输出示例**：一个可能的返回值的示例是一个defaultdict(tree)对象。
### _sub_function tree_to_string(tree, indent)
**tree_to_string**: tree_to_string函数的作用是将树结构转换为字符串表示。
**parameters**: 该函数的参数如下：
· tree: 表示树结构的字典。
· indent: 表示缩进的级别，默认为0。
**Code Description**: 该函数通过递归的方式遍历树结构，并将每个节点的键值对转换为字符串表示。首先，函数初始化一个空字符串s。然后，对树结构进行排序，并遍历每个节点。对于每个节点，函数将键值对的键添加到字符串s中，并根据缩进级别添加相应数量的空格。如果节点的值是一个字典，则递归调用tree_to_string函数，并将缩进级别加1。最后，函数返回字符串s。
**Note**: 使用该函数时，需要确保输入的树结构是一个字典，并且字典的值只能是字典或其他可哈希的类型。
**Output Example**: 
```
root
    child1
        grandchild1
        grandchild2
    child2
        grandchild3
```
