from llama_index.llms import OpenAI 


class OpenChatSummary:
    def __init__(self, api_key,api_base):
        self.llm = OpenAI(api_key=api_key, api_base=api_base)
        self.client = OpenAI(api_key=api_key, api_base=api_base,model="gpt-3.5-turbo-1106")
    def processname(self, value,structure, template):
        information = "\n\n".join(value)
        messages = f"base the following information: {information},here is the repo structure {structure},to fill the template: {template},must be in markdown format,the ouptut is only programe name ,max token no more than 15 words"
        response = self.llm.complete(messages)
        content = response
        return content
    def processdes(self, value, structure, template):
        # Step 1: Create an overview (总体概览)
        overview = f"This document will provide an overview of the project, including its structure and the template requirements. The main aspects are as follows: {', '.join(value)}."
        # Step 2: Detailed description (详细描述)
        detailed_description = "\n\n".join([f"**{item}:** Detailed information about '{item}'." for item in value])
        # Step 3: Structure and template information (项目结构和模板信息)
        structure_and_template = f"The project's structure is as follows: {structure}. The template to be filled is: {template}."
        # Step 4: Conclusion (总结)
        conclusion = "In summary, the above details provide a comprehensive view of the project, its structure, and template requirements."
        # Combining all parts
        messages = f"{overview}\n\n{detailed_description}\n\n{structure_and_template}\n\n{conclusion}\n\nNote: The response must be in markdown format and should not exceed 350 words."
        # Get response from language model
        response = self.llm.complete(messages)
        content = response
        return content
    def processlinces(self, value, template):
        information = "\n\n".join(value)
        messages = f"base the following information: {information},to fill the template: {template},must be in markdown format ,Your output must strictly adhere to the template style , the linces url is like https://choosealicense.com/licenses/XXXX, XXX is the license name"
        response = self.llm.complete(messages)
        content = response
        return content
    def processother(self, value,structure, template):
        information = "\n\n".join(value)
        messages = f"base the following information: {information},here is the repo structure {structure},to fill the template: {template},must be in markdown format ,max token no more than 450  words,Your output must strictly adhere to the template style"
        response = self.llm.complete(messages)
        content = response
        return content
    def refactor(self, value):
        information = "\n\n".join(value)
        messages = f"Reconstruct the new README based on the existing README, remove the useless information in it, and rearrange the format. The output must be in the markdwon format of README.md.Here is the existing README: {information}"
        response = self.client.complete(messages)
        content = response
        return content