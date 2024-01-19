## _function create_readme_if_not_exist(dire)
**create_readme_if_not_exist**: create_readme_if_not_exist函数的功能是在指定目录下创建README.md文件，如果该文件不存在的话。
**参数**: 这个函数的参数是dire，表示指定的目录路径。
**代码描述**: 这个函数首先使用os.path.join函数将dire和'README.md'拼接成一个路径字符串，表示README.md文件的路径。然后，它使用os.path.exists函数检查该路径是否存在，如果不存在则使用open函数创建一个名为readme_file的文件对象，并以写入模式打开README.md文件。接着，它使用os.path.basename函数获取dire的基本名称，并将该名称作为标题写入README.md文件中。
**注意**: 使用这段代码时需要注意以下几点：
- 需要提供正确的目录路径作为参数dire。
- 如果指定目录下已经存在README.md文件，则不会再次创建该文件。
- 创建README.md文件时，需要确保指定的目录路径是可写的。
- README.md文件的内容将以Markdown格式写入文件中，以便于阅读和展示。
## _function output_markdown(dire, base_dir, output_file, iter_depth)
**output_markdown**: output_markdown函数的功能是将目录结构生成为Markdown格式的文档。
**参数**: 这个函数的参数有dire、base_dir、output_file和iter_depth。
**代码描述**: 这个函数首先遍历指定目录下的所有文件和文件夹，如果是文件夹则调用create_readme_if_not_exist函数创建README.md文件。然后再次遍历目录，如果是文件夹则检查是否存在README.md文件，如果存在则在输出文件中创建一个指向该文件的Markdown链接。然后递归调用output_markdown函数处理嵌套的文件夹。如果是文件且是Markdown文件，则在输出文件中创建一个指向该文件的Markdown链接。
**注意**: 使用这段代码时需要注意以下几点：
- 需要提供正确的目录路径作为参数dire和base_dir。
- 需要提供一个可写的输出文件对象作为参数output_file。
- 可以选择性地提供一个整数值作为参数iter_depth，用于控制Markdown链接的缩进层级。
## _function markdown_file_in_dir(dire)
**markdown_file_in_dir**: markdown_file_in_dir函数的功能是在给定的目录中查找是否存在markdown文件。
**parameters**: 这个函数的参数是dire，表示要搜索的目录路径。
**Code Description**: 这个函数使用os.walk()函数遍历dire目录及其子目录中的所有文件和文件夹。然后使用正则表达式搜索文件名，如果文件名以".md"或".markdown"结尾，则返回True。如果遍历完所有文件后仍未找到匹配的文件，则返回False。
**Note**: 使用这个函数时，需要确保dire参数是一个有效的目录路径。
**Output Example**: 假设在给定的目录中存在一个名为"example.md"的markdown文件，则函数的返回值为True。
## _function is_markdown_file(filename)
**is_markdown_file**: is_markdown_file函数的功能是判断给定的文件名是否是Markdown文件。
**参数**: 这个函数的参数是文件名（filename）。
**代码描述**: 这个函数首先使用正则表达式搜索文件名中是否包含".md"或".markdown"的后缀，如果没有找到匹配的结果，则返回False。如果找到匹配的结果，函数会根据匹配结果的长度来判断文件名的后缀是".md"还是".markdown"。如果后缀是".md"，则返回去掉后缀的文件名；如果后缀是".markdown"，则返回去掉后缀的文件名。
**注意**: 使用这段代码时需要注意以下几点：
- 函数只能判断文件名是否是Markdown文件，不能判断文件内容是否符合Markdown格式。
- 文件名的后缀必须是".md"或".markdown"，且后缀必须是文件名的最后几个字符。
**输出示例**: 假设文件名为"example.md"，则函数返回"example"；假设文件名为"example.markdown"，则函数返回"example"。
## _function main
**main**: main函数的功能是生成书籍的摘要文件。
**参数**: 无参数。
**代码描述**: main函数首先获取命令行参数中的书籍名称，然后根据书籍名称创建一个文件夹。接着检查文件夹是否存在，如果不存在则创建该文件夹。然后，main函数创建一个名为SUMMARY.md的文件，并写入摘要的标题。最后，调用output_markdown函数生成摘要内容并写入文件中。
**注意**: 在使用该代码时需要确保命令行参数中传入了正确的书籍名称。
**输出示例**: 
```
# Summary

[摘要内容]
```

main函数是一个用于生成书籍摘要文件的函数。它首先通过sys.argv[1]获取命令行参数中的书籍名称。然后，它使用os.path.join函数将书籍名称与'./books'、'src'拼接成一个路径字符串，表示书籍文件夹的路径。接着，它使用os.path.exists函数检查该路径是否存在，如果不存在则使用os.makedirs函数创建该路径。然后，main函数使用os.path.join函数将书籍文件夹路径与'SUMMARY.md'拼接成一个路径字符串，表示摘要文件的路径。接下来，它使用open函数创建一个名为output的文件对象，并以写入模式打开摘要文件。然后，它使用output.write函数将摘要的标题写入文件中。最后，它调用output_markdown函数生成摘要的内容，并将内容写入文件中。

在使用main函数时，需要确保命令行参数中传入了正确的书籍名称。否则，程序将无法正确创建摘要文件。摘要文件的内容将以Markdown格式写入文件中，以便于阅读和展示。
