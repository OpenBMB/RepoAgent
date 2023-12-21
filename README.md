# 🤗 Introduction

RepoAgent is an Open-Source project driven by Large Language Models(LLMs) that aims to provide an intelligent way to document projects. 
It is designed to be a handy tool for developers who need to organize their code and cooperate with teammates.

![RepoAgent](assets/images/RepoAgent.png)

# Quick links

- [Introduction](#-introduction)
- [Quick links](#quick-links)
- [Background](#-background)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
  - [Configuring RepoAgent](#configuring-RepoAgent)
  - [Run RepoAgent](#run-RepoAgent)
  - [Configuring the Target Repository](#configuring-the-target-repository)
- [Future Work](#-future-work)
- [Supported Language](#supported-language)
- [License](#-license)
- [Citation](#-citation)

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

First, ensure that your machine is installed with Python version 3.9 or higher.
```
$ python --version
python 3.11.4
```
Next, clone the project, create a virtual environment, and install dependencies within this environment.

```
cd RepoAgent
conda create -n RepoAgent python=3.11.4
conda activate RepoAgent
pip install -r requirements.txt
```


# 📖 Quick Start

## Configuring RepoAgent
First, configure the OpenAI API parameters in the config.yml file.
For details on obtaining these, please refer to [OpenAI API](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

In the `config.yml` file, configure other parameters like OpenAI API, the destination repository path, document language, and so on:
```yaml
api_keys:
  gpt-3.5-turbo-16k:
    - api_key: sk-XXXX
      base_url: https://example.com/v1/
      api_type: azure
      api_version: XXX
      engine: GPT-35-Turbo-16k
      # you can use any kwargs supported by openai.ChatCompletion here
    - api_key: sk-xxxxx
      organization: org-xxxxxx
      model: gpt-3.5-turbo-16k
  ...

default_completion_kwargs:
  model: gpt-3.5-turbo-16k
  temperature: 0.2
  request_timeout: 60

repo_path: /path/to/your/repo
project_hierarchy: .project_hierarchy.json # The paths of the global structure information json file
Markdown_Docs_folder: /Markdown_Docs # The folder in the root directory of your target repository to store the documentation.

language: en # Two-letter language codes (ISO 639-1 codes), e.g. `language: en` for English. Refer to Supported Language for more languages.
```

## Run RepoAgent

Enter the root directory of RepoAgent and type the following command in the terminal:
```
python -m ai_doc.runner
```

If it's your first time generating documentation for the target repository, RepoAgent will automatically create a JSON file maintaining the global structure information and a folder named Markdown_Docs in the root directory of the target repository for storing documents.

The paths of the global structure information json file and the documentation folder can be configured in `config.yml`.

Once you have initially generated the global documentation for the target repository, or if the project you cloned already contains global documentation information, you can then seamlessly and automatically maintain internal project documentation with your team by configuring the **pre-commit hook** in the target repository!


## Configuring the Target Repository

RepoAgent currently supports generating documentation for projects, which requires some configuration in the target repository.

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
      entry: python path/to/your/RepoAgent/runner.py
      language: system
      # You can specify the file types that trigger the hook
      types: [python]
```
For specific configuration methods of hooks, please refer to [pre-commit](https://pre-commit.com/#plugins).
After configuring the yaml file, execute the following command to install the hook.
```
pre-commit install
```
This way, each time you perform a git commit, the RepoAgent hook will be triggered, automatically detecting changes in the target repository and generating corresponding documentation.
Next, make some modifications to the target repository, such as adding a new file or modifying an existing one.
You just need to follow the normal git workflow: git add, git commit, git push.
The RepoAgent hook will automatically trigger during git commit, detecting the files you added in the previous step and generating the corresponding documentation.

After execution, as RepoAgent modifies files in the target repository, it will display 'Failed' upon completion of the hook. This is normal.
![Execution Result](assets/images/execution_result.png)
At this point, the hook has correctly performed the documentation generation operation and created a folder named Markdown_Docs in the root directory of your target repository.
Next, you just need to git add the Markdown_Docs folder to the staging area and use:
```
git commit -m "your commit message" --no-verify
git push
```
to submit your commit.

# ✅ Future Work

- [x] Optimize the project structure and refine the responsibilities of the classes
- [x] Identification and maintenance of parent-child relationship hierarchy structure between objects
- [ ] Implement Black commit
- [ ] Support the selection of document language
- [x] Enable the identification of inter-object reference relationships
- [x] **Bi-direct reference** Bi-directional reference construction topology
- [ ] Open source

# Supported Language
Set the target language with the two-letter language codes (ISO 639-1 codes), e.g. `language: en` for English. Here are languages we currently support:

| Code | Language   |
|------|------------|
| en   | English    |
| es   | Spanish    |
| fr   | French     |
| de   | German     |
| zh   | Chinese    |
| ja   | Japanese   |
| ru   | Russian    |
| it   | Italian    |
| ko   | Korean     |
| nl   | Dutch      |
| pt   | Portuguese |
| ar   | Arabic     |
| tr   | Turkish    |
| sv   | Swedish    |
| da   | Danish     |
| fi   | Finnish    |
| no   | Norwegian  |
| pl   | Polish     |
| cs   | Czech      |
| hu   | Hungarian  |
| el   | Greek      |
| he   | Hebrew     |
| th   | Thai       |
| hi   | Hindi      |
| bn   | Bengali    |

# 📜 License

# 📊 Citation

