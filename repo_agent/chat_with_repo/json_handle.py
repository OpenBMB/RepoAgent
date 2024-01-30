import json

class JsonFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json_file(self):
        # 读取 JSON 文件作为数据库
        with open(self.file_path, 'r', encoding = 'utf-8') as file:
            data = json.load(file)
        return data

    def extract_md_contents(self):
        # 从 JSON 数据中提取 Markdown 内容并返回一个列表
        json_data = self.read_json_file()
        md_contents = []
        for file ,content in json_data.items():
            if isinstance(content, dict):
                for class_name, class_info in  content.items():
                    if "md_content" in class_info:
                        md_contents.append(class_info["md_content"][0])
        return md_contents
    def extract_metadata(self):
    # 从 JSON 数据中提取特定信息并返回一个字典列表
        json_data = self.read_json_file()
        extracted_contents = []
        for file_name, functions in json_data.items():
            for function_name, function_info in functions.items():
                # 构建包含所需信息的字典
                function_dict = {
                    "type": function_info["type"] if function_info.get("type") is not None else "UnknownType",
                    "name": function_info["name"] if function_info.get("name") is not None else "UnnamedFunction",
                    "code_start_line": function_info["code_start_line"] if function_info.get("code_start_line") is not None else -1,
                    "code_end_line": function_info["code_end_line"] if function_info.get("code_end_line") is not None else -1,
                    "parent": function_info["parent"] if function_info.get("parent") is not None else "NoParent",
                    "have_return": function_info["have_return"] if function_info.get("have_return") is not None else False,
                    "code_content": function_info["code_content"] if function_info.get("code_content") is not None else "NoContent",
                    "name_column": function_info["name_column"] if function_info.get("name_column") is not None else 0,
                    "item_status": function_info["item_status"] if function_info.get("item_status") is not None else "UnknownStatus",
                }
                extracted_contents.append(function_dict)
        return extracted_contents
    
    def recursive_search(self,data_item, search_text, results):
        if isinstance(data_item, dict):
            for key, value in data_item.items():
                # 检查是否是我们要找的名称
                if key == search_text and 'code_content' in value:
                    # 如果是，添加其code_content到结果列表
                    results.append(value['code_content'])
                # 递归搜索字典或列表
                if isinstance(value, (dict, list)):
                    self.recursive_search(value, search_text, results)
        elif isinstance(data_item, list):
            for item in data_item:
                self.recursive_search(item, search_text, results)


    def search_code_contents_by_name(self,file_path, search_text):
    # retrieve code from json
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # 结果列表，用于存储所有匹配项的code_content
                results = []

                # 使用辅助函数进行递归搜索
                self.recursive_search(data, search_text, results)

                if results:
                    return results
                else:
                    return "No matching item found."

        except FileNotFoundError:
            return "File not found."
        except json.JSONDecodeError:
            return "Invalid JSON file."
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    processor = JsonFileProcessor("database.json")
    md_contents = processor.extract_md_contents()