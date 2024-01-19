## _function main
**main**: main函数的功能是将指定的Markdown文档文件夹复制到指定的书籍文件夹中，并创建书籍的README.md文件。
**parameters**: 无参数。
**Code Description**: 
main函数首先通过sys.argv获取命令行参数，分别为markdown_docs_folder、book_name和repo_path。然后，main函数根据book_name创建了目标书籍文件夹dst_dir，并将repo_path和markdown_docs_folder拼接为docs_dir。

接下来，main函数检查目标书籍文件夹dst_dir是否存在，如果不存在则创建该文件夹，并打印出创建文件夹的信息。

然后，main函数遍历markdown_docs_folder文件夹中的所有文件和子文件夹。对于每个文件或子文件夹，main函数分别构建源路径src_path和目标路径dst_path。

如果src_path是一个文件夹，则使用shutil.copytree函数将该文件夹及其内容复制到dst_path，并打印出复制文件夹的信息。

如果src_path是一个文件，则使用shutil.copy2函数将该文件复制到dst_path，并打印出复制文件的信息。

接下来，main函数定义了一个名为create_book_readme_if_not_exist的内部函数，用于创建书籍的README.md文件。该函数首先构建了README.md文件的路径readme_path。然后，如果readme_path不存在，则使用open函数创建该文件，并写入书籍名称。

最后，main函数调用create_book_readme_if_not_exist函数，传入目标书籍文件夹dst_dir作为参数，以创建书籍的README.md文件。

**Note**: 
- main函数通过sys.argv获取命令行参数，确保在运行程序时传入正确的参数。
- main函数使用os.makedirs函数创建目标书籍文件夹，确保目标文件夹不存在时能够正确创建。
- main函数使用shutil.copytree函数和shutil.copy2函数分别复制文件夹和文件，确保能够正确复制文件和文件夹。
- main函数使用open函数创建README.md文件，并写入书籍名称，确保能够正确创建书籍的README.md文件。
### _sub_function create_book_readme_if_not_exist(dire)
**create_book_readme_if_not_exist**: create_book_readme_if_not_exist函数的功能是检查指定目录下是否存在README.md文件，如果不存在则创建一个。

**参数**: 
- dire: 指定目录的路径

**代码说明**:
该函数首先使用os模块的join方法将指定目录路径和文件名README.md拼接起来，得到README.md文件的完整路径readme_path。

然后，通过调用os模块的exists方法判断readme_path路径是否存在。如果不存在，说明该目录下没有README.md文件，需要创建一个。

接下来，使用open函数以写入模式打开readme_path路径对应的文件，并使用write方法写入一行文本，文本内容为"# "加上book_name变量的值。这样就创建了一个新的README.md文件，并写入了标题。

**注意**: 
- 在调用该函数之前，需要确保os模块已经导入。
- 在调用该函数时，需要传入一个有效的目录路径作为参数dire。
