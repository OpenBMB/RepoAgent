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
    def processdes(self, value,structure, template):
        information = "\n\n".join(value)
        messages = f"base the following information: {information},here is the repo structure {structure},to fill the template: {template},must be in markdown format, max token no more than 350 words"
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