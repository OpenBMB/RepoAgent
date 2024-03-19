<h1 align="center"><em>RepoAgent：一个用于代码库级别代码文档生成的LLM驱动框架</em></h1>

<p align="center">
  <img src="https://img.shields.io/pypi/dm/repoagent" alt="PyPI - 下载量"/>
  <a href="https://pypi.org/project/repoagent/">
    <img src="https://img.shields.io/pypi/v/repoagent" alt="PyPI - 版本"/>
  </a>
  <a href="Pypi">
    <img src="https://img.shields.io/pypi/pyversions/repoagent" alt="PyPI - Python版本"/>
  </a>
  <img alt="GitHub授权许可" src="https://img.shields.io/github/license/LOGIC-10/RepoAgent">
  <img alt="GitHub仓库星标" src="https://img.shields.io/github/stars/LOGIC-10/RepoAgent?style=social">
  <img alt="GitHub问题" src="https://img.shields.io/github/issues/LOGIC-10/RepoAgent">
  <a href="https://arxiv.org/abs/2402.16667v1">
    <img src="https://img.shields.io/badge/cs.CL-2402.16667-b31b1b?logo=arxiv&logoColor=red" alt="arXiv"/>
  </a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/OpenBMB/RepoAgent/main/assets/images/RepoAgent.png" alt="RepoAgent"/>
</p>

<p align="center">
  <a href="https://github.com/LOGIC-10/RepoAgent/blob/main/README.md">English README</a>
   • 
  <a href="https://github.com/LOGIC-10/RepoAgent/blob/main/README_CN.md">简体中文说明</a>
</p>

## 👾 背景

在计算机编程领域，全面的项目文档的重要性，包括每个Python文件的详细解释，不言而喻。这样的文档是理解、维护和增强代码库的基石。它提供了代码的必要上下文和理由，使当前和未来的开发者更容易理解软件的目的、功能和结构。它不仅便于当前和未来的开发者理解项目的目的和结构，还确保了项目随时间的推移保持可访问和可修改，大大简化了新团队成员的学习曲线。

传统上，创建和维护软件文档需要大量的人力和专业知识，这对没有专门人员的小团队来说是一个挑战。像GPT这样的大型语言模型（LLMs）的引入改变了这一点，使得AI可以处理大部分文档化过程。这种转变允许人类开发者专注于验证和微调，极大地减少了文档化的手动负担。

**🏆 我们的目标是创建一个智能文档助手，帮助人们阅读和理解仓库并生成文档，最终帮助人们提高效率和节省时间。**

## ✨ 特性

- **🤖 自动检测Git仓库中的变化，跟踪文件的增加、删除和修改。**
- **📝 通过AST独立分析代码结构，为各个对象生成文档。**
- **🔍 准确识别对象间的双向调用关系，丰富文档内容的全局视角。**
- **📚 根据变化无缝替换Markdown内容，保持文档一致性。**
- **🕙 执行多线程并发操作，提高文档生成效率。**
- **👭 为团队协作提供可持续的自动化文档更新方法。**
- **😍 以惊人的方式展示代码文档（每个项目都有由Gitbook提供支持的文档书）。**

## 🚀 开始使用

### 安装方法

#### 使用pip（普通用户首选）

直接使用pip安装`repoagent`包：

```bash
pip install repoagent
```

#### 使用PDM进行开发环境设置

如果您想要贡献或者设置一个开发环境：

- **安装PDM**：如果您还没有安装，请[安装PDM](https://pdm-project.org/latest/#installation)。
- **使用CodeSpace或克隆仓库**：

    - **使用CodeSpace**
    获取RepoAgent环境的最简单方式。点击下面链接使用GitHub Codespace，然后进行下一步。
  
    [![在GitHub Codespaces中打开](https://github.com/codespaces/badge.svg)](https://codespaces.new/LOGIC-10/RepoAgent?quickstart=1)
  
    - **克隆仓库**
  
    ```bash
    git clone https://github.com/LOGIC-10/RepoAgent.git
    cd RepoAgent
    ```

- **使用PDM设置**

    - 初始化Python虚拟环境。确保在`/RepoAgent`目录下运行下面的命令：
    
      ```bash
      pdm venv create --name repoagent
      ```
    
    - [激活虚拟环境](https://pdm-project.org/latest/usage/venv/#activate-a-virtualenv)
    
    - 使用PDM安装依赖
    
      ```bash
       pdm install
      ```

### 配置RepoAgent

在配置RepoAgent具体参数之前，请先确保已经在命令行配置 OpenAI API 作为环境变量：

```sh
export OPENAI_API_KEY=YOUR_API_KEY # on Linux/Mac

set OPENAI_API_KEY=YOUR_API_KEY # on Windows
$Env:OPENAI_API_KEY = "YOUR_API_KEY" # on Windows (PowerShell)
```

如果需要修改运行参数，使用 `repoagent configure` 

```sh
Enter the path to target repository: 
Enter the project hierarchy file name [.project_doc_record]: 
Enter the Markdown documents folder name [markdown_docs]: 
Enter files or directories to ignore, separated by commas []: 
Enter the language (ISO 639 code or language name, e.g., 'en', 'eng', 'English') [Chinese]: 
Enter the maximum number of threads [4]: 
Enter the maximum number of document tokens [1024]: 
Enter the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) [INFO]: 
Enter the model [gpt-3.5-turbo]: 
Enter the temperature [0.2]: 
Enter the request timeout (seconds) [60.0]: 
Enter the base URL [https://api.openai.com/v1]: 
```

## 运行RepoAgent

进入RepoAgent根目录并在终端尝试以下命令：
```sh
repoagent run # 这条命令会生成文档或自动更新文档 (pre-commit-hook 会自动调用它)
```

run 命令支持以下可选标志（如果设置，将覆盖配置默认值）：

- `-m`, `--model` TEXT：指定用于完成的模型。默认值：`gpt-3.5-turbo`
- `-t`, `--temperature` FLOAT：设置模型的生成温度。较低的值使模型更确定性。默认值：`0.2`
- `-r`, `--request-timeout` INTEGER：定义 API 请求的超时时间（秒）。默认值：`60`
- `-b`, `--base-url` TEXT：API 调用的基础 URL。默认值：`https://api.openai.com/v1`
- `-tp`, `--target-repo-path` PATH：目标仓库的文件系统路径。用作文档生成的根路径。默认值：`path/to/your/target/repository`
- `-hp`, `--hierarchy-path` TEXT：项目层级文件的名称或路径，用于组织文档结构。默认值：`.project_doc_record`
- `-mdp`, `--markdown-docs-path` TEXT：Markdown 文档将被存储或生成的文件夹路径。默认值：`markdown_docs`
- `-i`, `--ignore-list` TEXT：在文档生成过程中要忽略的文件或目录列表，用逗号分隔。
- `-l`, `--language` TEXT：文档的 ISO 639 代码或语言名称。默认值：`Chinese`
- `-ll`, `--log-level` [DEBUG|INFO|WARNING|ERROR|CRITICAL]：设置应用程序的日志级别。默认值：`INFO`

你也可以尝试以下功能

```sh
repoagent clean # 此命令将删除与repoagent相关的缓存
repoagent print-hierarchy # 此命令将打印repoagent解析出的目标仓库
repoagent diff # 此命令将检查基于当前代码更改将更新/生成哪些文档
```

如果您是第一次对目标仓库生成文档，此时RepoAgent会自动生成一个维护全局结构信息的json文件，并在目标仓库根目录下创建一个文件夹用于存放文档。
全局结构信息json文件和文档文件夹的路径都可以在`config.yml`中进行配置。

当您首次完成对目标仓库生成全局文档后，或您clone下来的项目已经包含了全局文档信息后，就可以通过**pre-commit**配置目标仓库**hook**和团队一起无缝自动维护一个项目内部文档了！

### 配置目标仓库

RepoAgent目前支持对项目的文档生成和自动维护，因此需要对目标仓库进行一定的配置。

首先，确保目标仓库是一个git仓库，且已经初始化。
```
git init
```
在目标仓库中安装pre-commit，用于检测git仓库中的变更。
```
pip install pre-commit
```
在目标仓库根目录下，创建一个名为`.pre-commit-config.yaml`的文件，示例如下：
```
repos:
  - repo: local
    hooks:
    - id: repo-agent
      name: RepoAgent
      entry: repoagent
      language: system
      pass_filenames: false # 阻止pre commit传入文件名作为参数
      # 可以指定钩子触发的文件类型，但是目前只支持python
      types: [python]
```
具体hooks的配置方法请参考[pre-commit](https://pre-commit.com/#plugins)。
配置好yaml文件后，执行以下命令，安装钩子。
```
pre-commit install
```
这样，每次git commit时，都会触发RepoAgent的钩子，自动检测目标仓库中的变更，并生成对应的文档。
接着，可以对目标仓库进行一些修改，例如在目标仓库中添加一个新的文件，或者修改一个已有的文件。
您只需要正常执行git的工作流程: git add, git commit -m "your commit message", git push
RepoAgent hook会在git commit时自动触发，检测前一步您git add的文件，并生成对应的文档。

执行后，RepoAgent会自动更改目标仓库中的已暂存文件并正式提交commit，执行完毕后会显示绿色的Passed，如下图所示：
![Execution Result](https://raw.githubusercontent.com/OpenBMB/RepoAgent/main/assets/images/ExecutionResult.png)

生成的文档将存放在目标仓库根目录下的指定文件夹中，生成的文档效果如下图所示：
![Documentation](https://raw.githubusercontent.com/OpenBMB/RepoAgent/main/assets/images/Doc_example.png)
![Documentation](https://raw.githubusercontent.com/OpenBMB/RepoAgent/main/assets/images/8_documents.png)


我们使用默认模型**gpt-3.5-turbo**对一个约**27万行**的中大型项目[**XAgent**](https://github.com/OpenBMB/XAgent)生成了文档。您可以前往XAgent项目的Markdown_Docs文件目录下查看生成效果。如果您希望得到更好的文档效果，我们建议您使用更先进的模型，如**gpt-4-1106** 或 **gpt-4-0125-preview**。

**最后，您可以通过自定义Prompt来灵活调整文档的输出格式、模板等方面的效果。 我们很高兴您探索更科学的自动化Technical Writing Prompts并对社区作出贡献。**

### 探索 chat with repo

我们将与仓库对话视为所有下游应用的统一入口，作为连接RepoAgent与人类用户和其他AI智能体之间的接口。我们未来的研究将探索适配各种下游应用的接口，并实现这些下游任务的独特性和现实要求。

在这里，我们展示了我们的下游任务之一的初步原型：自动issue问题解答和代码解释。您可以通过在终端运行以下代码启动服务。

```sh
repoagent chat_with_repo
```

# ✅ 未来工作

- [x] 支持通过`pip install repoagent`将项目作为包进行安装配置
- [ ] 通过全局文档信息自动生成仓库README.md文件
- [ ] **多编程语言支持** 支持更多编程语言，如Java、C或C++等
- [ ] 本地模型支持如 Llama、chatGLM、Qianwen 等


# 🥰 精选案例

以下是采用了RepoAgent的开源项目精选案例。

- [MiniCPM](https://github.com/OpenBMB/MiniCPM): 一个端侧大语言模型，大小为2B，效果可与7B模型媲美。
- [ChatDev](https://github.com/OpenBMB/ChatDev): 用于软件开发的协作式AI智能体。
- [XAgent](https://github.com/OpenBMB/XAgent): 一个用于解决复杂任务的自主大型语言模型智能体。
- [EasyRL4Rec](https://github.com/chongminggao/EasyRL4Rec): 一个用户友好的推荐系统强化学习库。

# 📊 引用我们
```bibtex
@misc{luo2024repoagent,
      title={RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation}, 
      author={Qinyu Luo and Yining Ye and Shihao Liang and Zhong Zhang and Yujia Qin and Yaxi Lu and Yesai Wu and Xin Cong and Yankai Lin and Yingli Zhang and Xiaoyin Che and Zhiyuan Liu and Maosong Sun},
      year={2024},
      eprint={2402.16667},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

