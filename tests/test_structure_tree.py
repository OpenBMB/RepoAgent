import os
from collections import defaultdict

def build_path_tree(who_reference_me, reference_who, doc_item_path):
    def tree():
        return defaultdict(tree)
    path_tree = tree()

    for path_list in [who_reference_me, reference_who]:
        for path in path_list:
            parts = path.split(os.sep)
            node = path_tree
            for part in parts:
                node = node[part]

    # 处理 doc_item_path
    parts = doc_item_path.split(os.sep)
    parts[-1] = '✳️' + parts[-1]  # 在最后一个对象前面加上星号
    node = path_tree
    for part in parts:
        node = node[part]

    def tree_to_string(tree, indent=0):
        s = ''
        for key, value in sorted(tree.items()):
            s += '    ' * indent + key + '\n'
            if isinstance(value, dict):
                s += tree_to_string(value, indent + 1)
        return s

    return tree_to_string(path_tree)


if "__name__ == main":
    who_reference_me = [
        "repo_agent/file_handler.py/FileHandler/__init__",
        "repo_agent/runner.py/need_to_generate"
    ]
    reference_who = [
        "repo_agent/file_handler.py/FileHandler/__init__",
        "repo_agent/runner.py/need_to_generate",
    ]

    doc_item_path = 'tests/test_change_detector.py/TestChangeDetector'

    result = build_path_tree(who_reference_me,reference_who,doc_item_path)
    print(result)
