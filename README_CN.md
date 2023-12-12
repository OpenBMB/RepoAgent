# 🤗 介绍

AI_doc是一个由大型语言模型（LLMs）驱动的开源项目，旨在提供智能化的项目文档编写方式。
它的设计目标是成为开发人员的便捷工具，用于创建、维护清晰易懂的代码文档并在团队成员之间应用协作。

# 👾 背景
在计算机编程领域，全面的项目文档非常重要，包括对每个Python文件的详细解释。这样的文档是理解、维护和增强代码库的基石。它为代码提供了必要的上下文解读，使当前和未来的开发人员更容易理解软件的目的、功能和结构。它不仅有助于当前和未来的开发人员理解项目的目的和结构，还确保项目随着时间的推移保持可访问和可修改，极大地降低了新团队成员的学习曲线。

传统上，创建和维护软件文档需要大量的人力和专业知识，这对于没有专门人员的小团队来说是一个挑战。大型语言模型（LLMs）如GPT的引入改变了这一情况，使得AI能够处理大部分文档编写过程。这种转变使得人类开发人员可以专注于验证和微调修改，极大地减轻了文档编写的人工负担。

**🏆 我们的目标是创建一个超级智能的文档助手，节省时间并为人类生成文档。**

# 📚 特性

## AI_doc具有以下特性：

- **🤖 自动检测Git仓库中的变更，跟踪文件的添加、删除和修改。**
- **📝 通过AST独立分析代码结构，为各个对象生成文档。**
- **📚 根据变更无缝替换Markdown内容，保持文档的一致性。**
- **📦 执行多线程并发操作，提高文档生成的效率。**
- **🔍 为团队协作提供可持续、自动化的文档更新方法。**

# 📦 安装
## 配置AI_doc
首先，确保你的机器安装了python3.9以上的版本
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

在runner.py的main开始处，配置配置文件路径config_file和需要生成文档的仓库路径repo_path，建议配置绝对路径。

## 配置目标仓库

AI_doc目前支持对项目的文档生成，因此需要对目标仓库进行一定的配置。

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
你只需要正常执行git的工作流程: git add, git commit, git push
AI_doc hook会在git commit时自动触发，检测前一步你git add的文件，并生成对应的文档。

执行后，由于AI_doc更改了目标仓库的文件，会在hook执行完毕后显示Failed，这是正常的。
![Execution Result](assets/images/execution_result.png)
此时，hook已经正确执行了文档生成的操作，并在你的目标仓库的根目录下创建了一个名为Markdown_Docs的文件夹。
接下来你只需要git add Markdown_Docs文件夹将新文档添加到暂存区，并使用：
```
git commit -m "your commit message" --no-verify
git push
```
提交你的commit即可。

# 📖 快速入门

# ✅ 未来工作

- [ ] 优化项目结构并细化类的职责。
- [ ] 尝试比较中文和英文提示的效果。
- [ ] 支持选择文档语言。
- [ ] 启用对象之间关系的识别。

# 📜 许可证
