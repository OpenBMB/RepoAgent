import json
import sys
from repo_agent.log import logger

class JsonFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json_file(self):
        # 读取 JSON 文件作为数据库
        with open(self.file_path, 'r', encoding = 'utf-8') as file:
            data = json.load(file)
        return data
    def extract_md_contents(self):
        """
        Extracts the contents of 'md_content' from a JSON file.

        Returns:
            A list of strings representing the contents of 'md_content'.
        """
        # Load JSON data from a file
        json_data = self.read_json_file()
        md_contents = []
        # Iterate through each file in the JSON data
        for file, items in json_data.items():
            # Check if the value is a list (new format)
            if isinstance(items, list):
                # Iterate through each item in the list
                for item in items:
                    # Check if 'md_content' exists and is not empty
                    if "md_content" in item and item["md_content"]:
                        # Append the first element of 'md_content' to the result list
                        md_contents.append(item["md_content"][0])
        return md_contents

    def extract_metadata(self):
        """
        Extracts metadata from JSON data.

        Returns:
            A list of dictionaries containing the extracted metadata.
        """
        # Load JSON data from a file
        json_data = self.read_json_file()
        extracted_contents = []
        # Iterate through each file in the JSON data
        for file_name, items in json_data.items():
            # Check if the value is a list (new format)
            if isinstance(items, list):
                # Iterate through each item in the list
                for item in items:
                    # Build a dictionary containing the required information
                    item_dict = {
                        "type": item.get("type", "UnknownType"),
                        "name": item.get("name", "Unnamed"),
                        "code_start_line": item.get("code_start_line", -1),
                        "code_end_line": item.get("code_end_line", -1),
                        "have_return": item.get("have_return", False),
                        "code_content": item.get("code_content", "NoContent"),
                        "name_column": item.get("name_column", 0),
                        "item_status": item.get("item_status", "UnknownStatus"),
                        # Adapt or remove fields based on new structure requirements
                    }
                    extracted_contents.append(item_dict)
            return extracted_contents

    def recursive_search(self, data_item, search_text, results):
        if isinstance(data_item, dict):
            # Direct comparison is removed as there's no direct key==search_text in the new format
            for key, value in data_item.items():
                # Recursively search through dictionary values and lists
                if isinstance(value, (dict, list)):
                    self.recursive_search(value, search_text, results)
        elif isinstance(data_item, list):
            for item in data_item:
                # Now we check for the 'name' key in each item of the list
                if isinstance(item, dict) and item.get('name') == search_text:
                    # If 'code_content' exists, append it to results
                    if 'code_content' in item:
                        results.append(item['code_content'])
                # Recursive call in case of nested lists or dicts
                self.recursive_search(item, search_text, results)

    def search_code_contents_by_name(self, file_path, search_text):
        # Attempt to retrieve code from the JSON file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                results = []  # List to store matching items' code_content
                self.recursive_search(data, search_text, results)
                return results if results else "No matching item found."
        except FileNotFoundError:
            return "File not found."
        except json.JSONDecodeError:
            return "Invalid JSON file."
        except Exception as e:
            return f"An error occurred: {e}"


if __name__ == "__main__":
    processor = JsonFileProcessor("database.json")
    md_contents = processor.extract_md_contents()