## FunctionDef build_path_tree(who_reference_me, reference_who, doc_item_path)
**build_path_tree**: The function of `build_path_tree` is to generate a hierarchical representation of paths and document item paths, marking the specified document item path with a special symbol.

**Parameters**:
- `who_reference_me`: A list of paths that reference the document item.
- `reference_who`: A list of paths that the document item references.
- `doc_item_path`: The specific path of the document item to be marked in the tree.

**Code Description**:
The `build_path_tree` function creates a hierarchical tree structure to represent the relationships between different paths, including those that reference a document item and those that are referenced by it. It uses a nested `defaultdict` to dynamically create the tree as paths are added. The function processes two lists of paths (`who_reference_me` and `reference_who`) to build the initial tree structure. Each path is split into parts using the OS-specific path separator, and these parts are used to navigate and populate the tree.

After constructing the tree with references, the function processes the `doc_item_path` by splitting it into parts and appending a special symbol (`✳️`) to the last part, which represents the document item itself. This modified path is then added to the tree, ensuring the document item is distinctly marked.

The `tree_to_string` inner function is used to convert the tree into a string representation. It recursively traverses the tree, converting each level to a string with appropriate indentation to reflect the hierarchical structure. The keys (path parts) are sorted alphabetically at each level to ensure a consistent order in the output.

**Note**:
- The function uses the `os.sep` constant for splitting paths, which makes it platform-independent (works on Unix/Linux, Windows, etc.).
- The special symbol `✳️` is used to mark the document item in the tree. Ensure that this symbol does not conflict with any actual path names.
- The tree is represented as a nested `defaultdict`, which might not be immediately intuitive for those unfamiliar with this data structure. It allows for the dynamic addition of nodes without explicitly checking if they exist.

**Output Example**:
Given the following inputs:
- `who_reference_me`: `["tests/test_structure_tree.py", "tests/test_other.py"]`
- `reference_who`: `["src/module.py"]`
- `doc_item_path`: `"tests/test_structure_tree.py/build_path_tree"`

The possible output could look like this:
```
src
    module.py
tests
    test_other.py
    test_structure_tree.py
        build_path_tree
            ✳️build_path_tree
```
This output represents a tree where the `build_path_tree` document item is marked within its path, showing both its references and what references it in a structured and readable format.
### FunctionDef tree
**Function**: tree

**Function of tree**: The function creates a recursive defaultdict structure.

**Parameters**: This function does not take any parameters.

**Code Description**: The `tree` function is designed to generate a recursive data structure using Python's `defaultdict` from the `collections` module. The unique aspect of this function is its self-referencing nature, which allows it to create an infinitely nested dictionary. When the `tree` function is called, it returns a `defaultdict` object where the default factory is the `tree` function itself. This means that any attempt to access a non-existent key in the dictionary will result in the creation of another `defaultdict` with the same properties, allowing for dynamic and virtually unlimited nesting.

**Note**: The use of the `tree` function can be particularly useful in scenarios where one needs to build a dynamically expanding tree-like data structure, such as in the representation of file systems, organizational hierarchies, or any scenario requiring nested mappings. However, users should be cautious of the potential for creating deeply nested structures that could lead to issues like maximum recursion depth errors if not handled properly.

**Output Example**:
```python
from collections import defaultdict

# Assuming the tree function is defined as per the given code
nested_dict = tree()

# Adding items to the nested dictionary
nested_dict['level1']['level2']['level3'] = 'deep value'

# Accessing the nested value
print(nested_dict['level1']['level2']['level3'])  # Output: deep value

# Attempting to access a non-existent key creates a new defaultdict at that level
print(nested_dict['level1']['level2']['new_level'])  # Output: defaultdict(<function tree at 0x...>, {})
```

In the output example, a nested dictionary structure is created and manipulated. The example demonstrates how accessing or setting keys at any depth automatically creates the necessary nested dictionaries without explicitly initializing them. This behavior is facilitated by the recursive nature of the `tree` function.
***
### FunctionDef tree_to_string(tree, indent)
**tree_to_string**: The function of `tree_to_string` is to convert a hierarchical tree structure into a formatted string representation.

**Parameters**:
- `tree`: A dictionary representing the tree structure where each key is a node, and its value is either another dictionary (representing a subtree) or an end node.
- `indent`: An integer representing the current indentation level for formatting the output string. It defaults to 0, meaning no indentation for the root level.

**Code Description**:
The `tree_to_string` function iterates over the items of the provided `tree` dictionary. The items are sorted by keys to ensure a consistent output order. For each key-value pair, the function appends to a string `s` the key followed by a newline character. The key is prefixed with a series of spaces that correspond to the current `indent` level, where each level adds four spaces to the indentation, simulating a tree structure visually.

If the value associated with a key is itself a dictionary, indicating a subtree, the function recursively calls itself with the subtree and an incremented `indent` value. This process adds the subtree's string representation to `s` with the appropriate indentation, effectively traversing the entire tree depth-first and building a hierarchical string representation of it.

**Note**:
- The function assumes that the input `tree` is a dictionary and will not work correctly if passed other types without modification.
- The output string does not have a trailing newline character at the end. If needed, this should be added after the function call.
- The function uses recursion, which means it could reach the Python recursion limit with very deep trees.

**Output Example**:
Given a tree structure like `{'a': {'b': {}, 'c': {'d': {}}}}`, the `tree_to_string` function would return the following string representation:

```
a
    b
    c
        d
```

This output demonstrates the hierarchical nature of the input tree, with each level of depth indented further to visually represent the structure.
***
