# 🤗 Introduction

AI_doc is an Open-Source project driven by Large Language Models(LLMs) that aims to provide an intelligent way to document projects. 
It is designed to be a handy tool for developers who need to organize their code and cooperate with teammates.

# 👾 Background
In the realm of computer programming, the significance of comprehensive project documentation, including detailed explanations for each Python file, cannot be overstated. Such documentation serves as the cornerstone for understanding, maintaining, and enhancing the codebase. It provides essential context and rationale for the code, making it easier for current and future developers to comprehend the purpose, functionality, and structure of the software. It not only facilitates current and future developers in grasping the project's purpose and structure but also ensures that the project remains accessible and modifiable over time, significantly easing the learning curve for new team members.

Traditionally, creating and maintaining software documentation demanded significant human effort and expertise, a challenge for small teams without dedicated personnel. The introduction of Large Language Models (LLMs) like GPT has transformed this, enabling AI to handle much of the documentation process. This shift allows human developers to focus on verification and fine-tuning, greatly reducing the manual burden of documentation.

**🏆 Our goal is to create a super-intelligent doc assistant that saves time and formulate documents for human.**

# 🪭 Features

- **🤖 Automatically detects changes in Git repositories, tracking additions, deletions, and modifications of files.**
- **📝 Independently analyzes the code structure through AST, generating documents for individual objects.**
- **🔍 Accurate identification of inter-object invocation relationships, enriching the global perspective of document content.**
- **📚 Seamlessly replaces Markdown content based on changes, maintaining consistency in documentation.**
- **🕙 Executes multi-threaded concurrent operations, enhancing the efficiency of document generation.**
- **👭 Offer a sustainable, automated documentation update method for team collaboration.**

# 📦 Installation

## Configuring AI_doc
First, ensure that your machine is installed with Python version 3.9 or higher.
```
$ python --version
python 3.11.4
```
Next, clone the project, create a virtual environment, and install dependencies within this environment.

```
cd AI_doc
conda create -n AI_doc python=3.11.4
conda activate AI_doc
pip install -r requirements.txt
```

Then, configure the OpenAI API parameters in the config.yml file.
For details on obtaining these, please refer to [OpenAI API](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

In the `config.yml` file, configure relevant parameters like OpenAI API, the destination repository path, document language (future support), and so on.

## Run AI_doc

Please use the following command in the main function of runner.py if you are generating documentation for the first time in the target repository:

```
runner.first_generate()
```

At this point, AI_doc will automatically generate a json file that maintains the global structure information for your target repository, and create a folder named Markdown_Docs in the root directory of your target repository to store the documentation.

The paths of the global structure information json file and the documentation folder can be configured in `config.yml`.

After you have generated the global documentation for the target repository for the first time, you can configure the target repository hook with **pre-commit** and maintain an internal documentation for the project seamlessly with your team!


## Configuring the Target Repository

AI_doc currently supports generating documentation for projects, which requires some configuration in the target repository.

First, ensure that the target repository is a git repository and has been initialized.
```
git init
```
Install pre-commit in the target repository to detect changes in the git repository.

```
pip install pre-commit
```
Create a file named `.pre-commit-config.yaml` in the root directory of the target repository. An example is as follows:

```
repos:
  - repo: local
    hooks:
    - id: ai-doc
      name: AI-doc
      entry: python path/to/your/AI_doc/runner.py
      language: system
      # You can specify the file types that trigger the hook
      types: [python]
```
For specific configuration methods of hooks, please refer to [pre-commit](https://pre-commit.com/#plugins).
After configuring the yaml file, execute the following command to install the hook.
```
pre-commit install
```
This way, each time you perform a git commit, the AI_doc hook will be triggered, automatically detecting changes in the target repository and generating corresponding documentation.
Next, make some modifications to the target repository, such as adding a new file or modifying an existing one.
You just need to follow the normal git workflow: git add, git commit, git push.
The AI_doc hook will automatically trigger during git commit, detecting the files you added in the previous step and generating the corresponding documentation.

After execution, as AI_doc modifies files in the target repository, it will display 'Failed' upon completion of the hook. This is normal.
![Execution Result](assets/images/execution_result.png)
At this point, the hook has correctly performed the documentation generation operation and created a folder named Markdown_Docs in the root directory of your target repository.
Next, you just need to git add the Markdown_Docs folder to the staging area and use:
```
git commit -m "your commit message" --no-verify
git push
```
to submit your commit.

# 📖 Quick Start

# ✅ Future Work

- [x] Optimize the project structure and refine the responsibilities of the classes
- [x] Identification and maintenance of parent-child relationship hierarchy structure between objects
- [ ] Implement Black commit
- [ ] Support the selection of document language
- [x] Enable the identification of inter-object reference relationships
- [x] **Bi-direct reference** Bi-directional reference construction topology
- [ ] Open source

# 📜 License

# 📊 Citation

