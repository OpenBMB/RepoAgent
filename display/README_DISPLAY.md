## 前提条件

在使用 RepoAgent 对相应 repo 生成文档之后，请进入 display 文件夹。
  
```bash
cd display
```

您需要 **nodejs 10** 的环境，可以使用 nvm 来安装。

## 一键部署命令脚本

您可以在命令行输入`make help`，查看我们的自动部署脚本。

```bash
(RepoAgent) yesai@yesaideMacBook-Pro:RepoAgent/display ‹wys*›$ make help
BOOK_NAME is XAgent-Dev
MARKDOWN_DOCS_FOLDER is Markdown_Docs

Usage:
  make <task>

Tasks:
  init_env                       init nodejs 10.x env
  clear_book                     clear repo generated book
  init                           gitbook init to install plugins
  generate                       generate repo book
  serve                          serve gitbook
  help                           make help info

```

其中，`make init_env` 还在测试，您可以自己根据自身系统，安装 nodejs 10。

然后您可以依次进行 `make init` 初始化 gitbook 运行环境（make init 运行一次即可）。

环境准备妥当后，您可以多次执行 `make generate`，更改相关配置或者`book.json`后，只需重新运行`make generate` 即可重新部署。

成功后命令行输出如下所示：

```bash
init!
finish!
info: >> generation finished with success in 16.7s ! 

Starting server ...
Serving book on http://localhost:4000
```

之后您可以在 http://localhost:4000/ 看到您的可视化 gitbook repo 文档。


## Future TODO List：

[ ] 一键自动创建环境

[ ] （本地创建环境不好弄的话）docker 一键部署 gitbook 以及上传

[ ] 自动一键部署到对应 github 或 gitee 的 Repo 的对应 pages，让大家通过repo相关网址可以直接访问文档

