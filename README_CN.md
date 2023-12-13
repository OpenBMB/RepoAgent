# 🤗 介绍

AI_doc是一个由大型语言模型（LLMs）驱动的开源项目，旨在提供智能化的项目文档编写方式。
它的设计目标是成为开发人员的便捷工具，用于创建、维护清晰易懂的代码文档并在团队成员之间应用协作。

# 👾 背景
在计算机编程领域，全面的项目文档非常重要，包括对每个Python文件的详细解释。这样的文档是理解、维护和增强代码库的基石。它为代码提供了必要的上下文解读，使当前和未来的开发人员更容易理解软件的目的、功能和结构。它不仅有助于当前和未来的开发人员理解项目的目的和结构，还确保项目随着时间的推移保持可访问和可修改，极大地降低了新团队成员的学习曲线。

传统上，创建和维护软件文档需要大量的人力和专业知识，这对于没有专门人员的小团队来说是一个挑战。大型语言模型（LLMs）如GPT的引入改变了这一情况，使得AI能够处理大部分文档编写过程。这种转变使得人类开发人员可以专注于验证和微调修改，极大地减轻了文档编写的人工负担。

**🏆 我们的目标是创建一个超级智能的文档助手，节省时间并为人类生成文档。**

# 🪭 特性

- **🤖 自动检测Git仓库中的变更，跟踪文件的添加、删除和修改。**
- **📝 通过AST独立分析代码结构，为各个对象生成文档。**
- **🔍 精准识别对象间调用关系，丰富文档内容的全局视野**
- **📚 根据变更无缝替换Markdown内容，保持文档的一致性。**
- **🕙 执行多线程并发操作，提高文档生成的效率。**
- **👭 为团队协作提供可持续、自动化的文档更新方法。**

# 📍 安装
## 配置AI_doc
首先，确保您的机器安装了python3.9以上的版本
```
$ python --version
python 3.11.4
```

接着，克隆本项目，创建一个虚拟环境，并在环境内安装依赖
```
cd AI_doc
conda create -n AI_doc python=3.11.4
conda activate AI_doc
pip install -r requirements.txt
```
下一步，在config.yml文件中配置OpenAI API 相关参数信息。
具体获取方法请参考[OpenAI API](https://beta.openai.com/docs/developer-quickstart/your-api-keys)。

在`config.yml`文件中，配置OpenAI API的相关参数信息、目标仓库的路径、文档语言（未来支持）等。

# 📖 快速开始

## 运行AI_doc
在runner.py中，如果您是第一次对目标仓库生成文档，请在main函数中使用以下命令：
```
runner.first_generate()
```
此时AI_doc会自动为您的目标仓库生成一个维护全局结构信息的json文件，并在您的目标仓库根目录下创建一个名为Markdown_Docs的文件夹，用于存放文档。
全局结构信息json文件和文档文件夹的路径都可以在`config.yml`中进行配置。

当您首次对目标仓库生成全局文档后，就可以通过**pre-commit**配置目标仓库**hook**和团队一起无缝自动维护一个项目内部文档了！

## 配置目标仓库

AI_doc目前支持对项目的文档生成和自动维护，因此需要对目标仓库进行一定的配置。

首先，确保目标仓库是一个git仓库，且已经初始化。
```
git init
```
在目标仓库中安装pre-commit，用于检测git仓库中的变更。
```
pip install pre-commit
```
在目标仓库根目录下，创建一个名为.pre-commit-config.yaml的文件，示例如下：
```
repos:
  - repo: local
    hooks:
    - id: ai-doc
      name: AI-doc
      entry: python path/to/your/AI_doc/runner.py
      language: system
      # 可以指定钩子触发的文件类型
      types: [python]
```
具体hooks的配置方法请参考[pre-commit](https://pre-commit.com/#plugins)。
配置好yaml文件后，执行以下命令，安装钩子。
```
pre-commit install
```
这样，每次git commit时，都会触发AI_doc的钩子，自动检测目标仓库中的变更，并生成对应的文档。
接着，可以对目标仓库进行一些修改，例如在目标仓库中添加一个新的文件，或者修改一个已有的文件。
您只需要正常执行git的工作流程: git add, git commit, git push
AI_doc hook会在git commit时自动触发，检测前一步您git add的文件，并生成对应的文档。

执行后，由于AI_doc更改了目标仓库的文件，会在hook执行完毕后显示Failed，这是正常的。
![Execution Result](assets/images/execution_result.png)
此时，hook已经正确执行了文档生成的操作，并在您的目标仓库的根目录下创建了一个名为Markdown_Docs的文件夹。
接下来您只需要git add Markdown_Docs文件夹将新文档添加到暂存区，并使用：
```
git commit -m "your commit message" --no-verify
git push
```
提交您的commit即可。

# ✅ 未来工作

- [x] 优化项目结构并细化类的职责
- [x] 对象间父子关系层级结构识别及维护
- [ ] 实现 Black commit
- [ ] 支持选择文档语言
- [x] 启用对象间调用关系的识别
- [x] **Bi-direct reference** 双向引用 构建 拓扑结构
- [ ] 开源

# 📜 许可证

# 📊 引用
