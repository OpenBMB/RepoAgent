# FunctionDef build_path_tree(who_reference_me, reference_who, doc_item_path):
**build_path_tree**: The function of this Function is to build a tree-like structure representing the paths of objects in a project.

**parameters**: 
- who_reference_me: A list of paths representing the objects that reference the current object.
- reference_who: A list of paths representing the objects that the current object references.
- doc_item_path: A string representing the path of the current object.

**Code Description**: 
The function starts by defining a nested function called "tree" which returns a defaultdict with the default value set to another defaultdict. This nested function is used to create a tree-like structure.

Next, the function initializes an empty path_tree using the "tree" function.

The function then iterates over the paths in both "who_reference_me" and "reference_who" lists. For each path, it splits the path into individual parts using the os.sep separator (which represents the path separator for the current operating system). It then traverses the path_tree, creating nested defaultdicts for each part of the path.

After that, the function processes the "doc_item_path" by splitting it into parts and replacing the last part with a modified version that has a star symbol (*) prepended to it. It then traverses the path_tree again, creating nested defaultdicts for each part of the modified "doc_item_path".

Finally, the function defines another nested function called "tree_to_string" which takes a tree-like structure and converts it into a string representation. It recursively iterates over the tree, sorting the items and adding each key to the string representation. If the value associated with a key is another dictionary, it recursively calls the "tree_to_string" function to add its contents to the string representation.

The function returns the string representation of the path_tree.

**Note**: 
- The function assumes that the paths in "who_reference_me", "reference_who", and "doc_item_path" are using the operating system's path separator.
- The function uses the defaultdict class from the collections module to automatically create nested defaultdicts when accessing non-existent keys.

**Output Example**: 
```
tests
    test_structure_tree.py
        build_path_tree
            ✳️build_path_tree
```
## FunctionDef tree:
**tree**: The function of this Function is to create a nested dictionary representing a tree structure.

**parameters**: This Function does not take any parameters.

**Code Description**: 
The `tree` function initializes and returns a nested dictionary using the `defaultdict` class from the `collections` module. The `defaultdict` class allows us to specify a default value for keys that have not been set yet. In this case, the default value is another `tree` object, which means that each key in the dictionary will have a nested dictionary as its value.

**Note**: 
- This function assumes that the `defaultdict` class has been imported from the `collections` module.
- The returned nested dictionary can be used to represent a tree structure, where each key represents a node and its value represents its children.

**Output Example**: 
The output of this function is a nested dictionary representing a tree structure.
## FunctionDef tree_to_string(tree, indent):
**tree_to_string**: The function of this Function is to convert a nested dictionary representing a tree structure into a string representation.

**parameters**: 
- tree: A nested dictionary representing a tree structure.
- indent: An integer representing the number of indentation levels.

**Code Description**: 
The `tree_to_string` function takes a nested dictionary `tree` and an integer `indent` as parameters. It initializes an empty string `s` to store the string representation of the tree. 

The function iterates over the items in the `tree` dictionary, sorted by key. For each key-value pair, it appends the key to the string `s`, preceded by a number of indentation spaces determined by the `indent` parameter. 

If the value associated with the key is another dictionary, the function recursively calls itself with the value as the new `tree` parameter and increments the `indent` by 1. This allows the function to handle nested levels of the tree structure.

Finally, the function returns the string representation of the tree.

**Note**: 
- This function assumes that the input `tree` is a nested dictionary representing a tree structure.
- The `indent` parameter is optional and defaults to 0 if not provided.

**Output Example**: 
If the input `tree` is:
```
{
    'A': {
        'B': {
            'C': {},
            'D': {}
        },
        'E': {}
    },
    'F': {
        'G': {}
    }
}
```
The function will return the following string:
```
A
    B
        C
        D
    E
F
    G
```
***
