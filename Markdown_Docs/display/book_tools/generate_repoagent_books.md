## _function main
**main**: main函数的功能是将指定的Markdown文档文件夹复制到指定的书籍文件夹中，并创建书籍的README.md文件。
**parameters**: 该函数没有参数。
**Code Description**: 
- 首先，从命令行参数中获取Markdown文档文件夹的路径、书籍名称和仓库路径。
- 然后，创建书籍文件夹的目标路径dst_dir，该路径为'./books'下的书籍名称文件夹下的'src'文件夹。
- 接着，获取Markdown文档文件夹的源路径docs_dir，该路径为仓库路径下的Markdown文档文件夹。
- 如果目标路径dst_dir不存在，则创建该路径，并打印提示信息。
- 遍历Markdown文档文件夹中的每个文件或文件夹：
  - 获取源路径src_path和目标路径dst_path。
  - 如果源路径src_path是一个文件夹，则使用shutil.copytree函数将其复制到目标路径dst_path，并打印提示信息。
  - 如果源路径src_path是一个文件，则使用shutil.copy2函数将其复制到目标路径dst_path，并打印提示信息。
- 定义了一个名为create_book_readme_if_not_exist的内部函数，用于创建书籍的README.md文件。
- 调用create_book_readme_if_not_exist函数，传入目标路径dst_dir作为参数，如果书籍的README.md文件不存在，则创建该文件，并写入书籍名称作为标题。
**Note**: 
- 在使用该函数之前，需要在命令行中传入三个参数，分别为Markdown文档文件夹的路径、书籍名称和仓库路径。
- 该函数会将Markdown文档文件夹中的所有文件和文件夹复制到指定的书籍文件夹中，并创建书籍的README.md文件。
- 如果目标路径dst_dir已经存在，则不会再次创建该路径。
- 如果书籍的README.md文件已经存在，则不会再次创建该文件。
### _sub_function create_book_readme_if_not_exist(dire)
**create_book_readme_if_not_exist**: create_book_readme_if_not_exist函数的功能是检查指定目录下是否存在README.md文件，如果不存在则创建一个，并在文件中写入书名。
**参数**: 这个函数的参数是dire，表示目录路径。
**代码描述**: 这个函数首先通过os.path.join函数将目录路径和README.md文件名拼接起来，得到README.md文件的完整路径。然后通过os.path.exists函数判断该路径下是否存在README.md文件。如果不存在，则使用open函数以写入模式打开README.md文件，并使用write函数向文件中写入书名。
**注意**: 使用这段代码时需要注意目录路径的正确性，确保指定的目录存在。另外，书名需要提前定义并传入函数中。
