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
        for file in json_data["files"]:
            for obj in file["objects"]:
                if "md_content" in obj:
                    md_contents.append(obj["md_content"])
        return md_contents
    
    def search_in_json_nested(self, file_path, search_text):
        # retrieve code from json
        try:
            with open(file_path, 'r',encoding = 'utf-8') as file:
                data = json.load(file)

                def recursive_search(data_item):
                    if isinstance(data_item, dict):
                        if 'name' in data_item and search_text.lower() in data_item['name'].lower():
                            return data_item

                        for key, value in data_item.items():
                            if isinstance(value, (dict, list)):
                                result = recursive_search(value)
                                if result:
                                    return result
                    elif isinstance(data_item, list):
                        for item in data_item:
                            result = recursive_search(item)
                            if result:
                                return result

                result = recursive_search(data)
                if result:
                    return result
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