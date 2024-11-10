## FunctionDef build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: The function of build_path_tree is to create a hierarchical representation of file paths based on provided references and a specific document item path.

**parameters**: The parameters of this Function.
· parameter1: who_reference_me - A list of file paths that reference the current entity.
· parameter2: reference_who - A list of file paths that reference another entity.
· parameter3: doc_item_path - A specific file path that needs to be highlighted in the output.

**Code Description**: The build_path_tree function constructs a nested dictionary structure representing a tree of file paths. It begins by defining an inner function, tree, which initializes a defaultdict that allows for the creation of nested dictionaries automatically. The variable path_tree is then assigned the result of calling this inner function.

The function processes two lists of paths: who_reference_me and reference_who. For each path in these lists, it splits the path into its components using the operating system's path separator (os.sep). It then traverses the path_tree structure, creating nested dictionaries for each part of the path.

After processing the reference paths, the function handles the doc_item_path. It splits this path into components as well, but modifies the last component by prefixing it with a star symbol (✳️) to indicate it as a special item. The function again traverses the path_tree to include this modified path.

Finally, the function defines another inner function, tree_to_string, which recursively converts the tree structure into a string representation. This function sorts the keys at each level and adds indentation based on the depth of the tree. The resulting string representation of the path_tree is returned as the output of the build_path_tree function.

**Note**: It is important to ensure that the input paths are formatted correctly and that the os module is imported for the path separator to function properly. The output string will visually represent the hierarchy of paths, with the doc_item_path clearly marked.

**Output Example**: 
Assuming the following inputs:
who_reference_me = ["folder1/fileA.txt", "folder1/folder2/fileB.txt"]
reference_who = ["folder3/fileC.txt"]
doc_item_path = "folder1/folder2/fileB.txt"

The output of the function could look like this:
folder1
    fileA.txt
    folder2
        ✳️fileB.txt
folder3
    fileC.txt
### FunctionDef tree
**tree**: tree函数的功能是返回一个默认字典，该字典的默认值是一个新的tree函数。

**parameters**: 该函数没有参数。

**Code Description**: tree函数使用了Python的collections模块中的defaultdict。defaultdict是一个字典子类，它提供了一个默认值，当访问一个不存在的键时，会自动创建一个新的值。在这个实现中，tree函数返回一个defaultdict，其中的默认值是调用tree函数本身。这意味着每当访问一个不存在的键时，defaultdict会自动创建一个新的defaultdict。这种递归的结构可以用于构建树形数据结构，其中每个节点可以有多个子节点，且子节点的数量和名称是动态生成的。

**Note**: 使用此代码时，请注意避免无限递归的情况。由于tree函数返回的defaultdict的默认值是tree函数本身，因此在访问不存在的键时，会不断创建新的defaultdict，直到达到某种条件或限制。

**Output Example**: 调用tree函数后，可能会得到如下结构：
```
defaultdict(<function tree at 0x...>, {
    'key1': defaultdict(<function tree at 0x...>, {
        'subkey1': defaultdict(<function tree at 0x...>, {}),
        'subkey2': defaultdict(<function tree at 0x...>, {})
    }),
    'key2': defaultdict(<function tree at 0x...>, {})
})
``` 
在这个例子中，'key1'和'key2'是顶层键，而'subkey1'和'subkey2'是'key1'下的子键。
***
### FunctionDef tree_to_string(tree, indent)
**tree_to_string**: tree_to_string 函数的功能是将树形结构转换为字符串格式，便于可视化展示。

**parameters**: 此函数的参数如下：
· parameter1: tree - 一个字典类型的树形结构，其中包含键值对，键为节点名称，值为子节点（可以是字典或其他类型）。
· parameter2: indent - 一个整数，表示当前节点的缩进级别，默认为0。

**Code Description**: tree_to_string 函数通过递归的方式遍历给定的树形结构，并将其格式化为字符串。函数首先初始化一个空字符串 s，用于存储最终的结果。接着，函数对树中的每个键值对进行排序，并逐个处理每个键。对于每个键，函数会在字符串中添加相应数量的空格（由 indent 参数控制），然后添加键的名称，并换行。如果该键对应的值是一个字典，函数会递归调用自身，增加缩进级别（indent + 1），以处理子树。最终，函数返回构建好的字符串，展示了树形结构的层次关系。

**Note**: 使用此函数时，请确保传入的 tree 参数为字典类型，并且其值可以是字典或其他类型。缩进参数 indent 应为非负整数，以确保输出格式正确。

**Output Example**: 假设输入的树形结构为：
{
    "根节点": {
        "子节点1": {},
        "子节点2": {
            "孙节点1": {}
        }
    },
    "另一个根节点": {}
}
调用 tree_to_string 函数后，返回的字符串可能如下所示：
根节点
    子节点1
    子节点2
        孙节点1
另一个根节点
***
