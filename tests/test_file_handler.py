# from pprint import pprint

from repo_agent.file_handler import FileHandler

# fh = FileHandler(
#     "/Users/jbi/Playground/Github/st01cs/RepoAgent/", "repo_agent/change_detector.py"
# )
# content = fh.read_file()
# f1 = fh.get_functions_and_classes_ts(content)
# pprint(f1)

# pprint("*" * 80)
# f2 = fh.get_functions_and_classes(content)
# pprint(f2)


def test_get_functions_and_classes():
    # Test case 1: Empty file
    fh = FileHandler(".", "test.py")
    empty_content = ""
    assert fh.get_functions_and_classes(empty_content) == []

    # Test case 2: File with a simple function
    code_with_function = """
def test_func(param1, param2):
    return param1 + param2
"""
    result = fh.get_functions_and_classes(code_with_function)
    assert len(result) == 1
    assert result[0][0] == "FunctionDef"  # Type is function
    assert result[0][1] == "test_func"  # Function name
    assert result[0][4] == ["param1", "param2"]  # Parameters

    # Test case 3: File with a class
    code_with_class = """
class TestClass:
    def __init__(self):
        pass
"""
    result = fh.get_functions_and_classes(code_with_class)
    assert len(result) == 2  # Class and __init__ method
    assert result[0][0] == "ClassDef"  # Type is class
    assert result[0][1] == "TestClass"  # Class name
    assert result[0][4] == []  # No parameters for class
    assert result[1][0] == "FunctionDef"  # Type is function
    assert result[1][1] == "__init__"  # Function name
    assert result[1][4] == ["self"]  # Parameters

    # Test case 4: File with async function
    code_with_async = """
async def async_func(param):
    return await param
"""
    result = fh.get_functions_and_classes(code_with_async)
    assert len(result) == 1
    assert result[0][0] == "FunctionDef"  # Type is async function
    assert result[0][1] == "async_func"  # Function name
    assert result[0][4] == ["param"]  # Parameters

    # Test case 5: Nested structures
    code_with_nested = """
class OuterClass:
    def outer_method(self):
        def inner_function():
            pass
        return inner_function
"""
    result = fh.get_functions_and_classes(code_with_nested)
    assert len(result) == 3  # OuterClass, outer_method, inner_function
    assert result[0][0] == "ClassDef"
    assert result[1][0] == "FunctionDef"
    assert result[2][0] == "FunctionDef"
