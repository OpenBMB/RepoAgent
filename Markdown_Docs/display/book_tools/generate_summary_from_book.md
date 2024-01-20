## _function create_readme_if_not_exist(dire)
**create_readme_if_not_exist**: create_readme_if_not_exist函数的功能是检查给定目录下是否存在README.md文件，如果不存在则创建一个。

**参数**: 
- dire: 字符串类型，表示目录的路径。

**代码描述**: 
- 首先，使用os.path.join函数将目录路径和README.md文件名拼接起来，得到README.md文件的完整路径。
- 然后，使用os.path.exists函数判断README.md文件是否存在。
- 如果README.md文件不存在，则使用open函数以写入模式打开README.md文件。
- 使用os.path.basename函数获取目录的名称，并将其作为标题写入README.md文件。
- 最后，使用with语句自动关闭文件。

**注意**: 
- 在使用该函数之前，需要确保os模块已经导入。
- 该函数只会在给定目录下创建一个README.md文件，不会对子目录进行操作。
## _function output_markdown(dire, base_dir, output_file, iter_depth)
**output_markdown**: output_markdown函数的功能是根据给定的目录生成Markdown文件的目录结构。

**参数**: 
- dire: 字符串类型，表示目录的路径。
- base_dir: 字符串类型，表示基准目录的路径。
- output_file: 文件对象，表示输出的Markdown文件。
- iter_depth: 整数类型，表示当前目录的迭代深度，默认值为0。

**代码描述**: 
- 首先，使用os.listdir函数遍历给定目录下的所有文件和子目录。
- 对于每个文件或子目录，使用os.path.join函数将目录路径和文件名拼接起来，得到文件或子目录的完整路径。
- 如果是子目录，调用create_readme_if_not_exist函数检查是否存在README.md文件。
- 然后，再次使用os.listdir函数遍历给定目录下的所有文件和子目录。
- 对于每个文件或子目录，使用os.path.join函数将目录路径和文件名拼接起来，得到文件或子目录的完整路径。
- 如果是子目录，首先检查该目录下是否存在README.md文件。
- 如果存在README.md文件，使用os.path.relpath函数获取相对路径，并将文件名和相对路径写入输出的Markdown文件。
- 如果是子目录，递归调用output_markdown函数处理子目录。
- 如果是文件，并且文件名是Markdown文件，则根据迭代深度和文件名是否为'SUMMARY.md'或'README.md'来判断是否写入输出的Markdown文件。

**注意**: 
- 在使用该函数之前，需要确保os模块已经导入。
- 该函数会遍历给定目录下的所有文件和子目录，并根据文件的后缀和迭代深度来生成Markdown文件的目录结构。
- 该函数会递归处理子目录，并将子目录的相对路径和文件名写入输出的Markdown文件。
- 该函数会忽略SUMMARY.md和README.md文件，除非迭代深度为0且文件名为README.md。

**调用示例**: 
- output_markdown('./books', './books', output_file)

**引用对象**: 
- create_readme_if_not_exist: 用于检查给定目录下是否存在README.md文件，如果不存在则创建一个。
- is_markdown_file: 用于判断给定的文件名是否为Markdown文件。
## _function markdown_file_in_dir(dire)
**markdown_file_in_dir**: markdown_file_in_dir函数的功能是在指定的目录中查找是否存在markdown文件。
**参数**: 这个函数的参数是dire，表示要搜索的目录路径。
**代码描述**: 这个函数使用os.walk()函数遍历指定目录dire下的所有文件和子目录。然后使用正则表达式re.search()匹配文件名是否以".md"或".markdown"结尾，如果匹配成功则返回True。如果遍历完所有文件后都没有匹配成功，则返回False。
**注意**: 使用这段代码时需要注意以下几点：
- 需要导入os和re模块。
- 参数dire必须是一个有效的目录路径。
**输出示例**: 假设在指定目录中存在一个名为"example.md"的markdown文件，则函数的返回值为True。
## _function is_markdown_file(filename)
**is_markdown_file**: is_markdown_file函数的功能是判断给定的文件名是否为Markdown文件。
**参数**: 这个函数的参数是filename，表示要判断的文件名。
**代码描述**: 这个函数首先使用正则表达式搜索文件名中是否包含'.md'或'.markdown'的后缀，如果没有找到匹配的结果，则返回False。如果找到了匹配的结果，根据匹配结果的长度来判断文件名的后缀是'.md'还是'.markdown'，然后根据不同的情况返回相应的结果。
**注意**: 使用这个函数时需要传入一个文件名作为参数，函数会根据文件名的后缀判断是否为Markdown文件，并返回相应的结果。
**输出示例**: 
- 对于文件名为'example.md'的情况，函数会返回'example'。
- 对于文件名为'example.markdown'的情况，函数会返回'example'。
- 对于其他文件名的情况，函数会返回False。
## _function main
**main**: main函数的功能是根据给定的书名生成Markdown文件的目录结构。

**参数**: 
- 无

**代码描述**: 
- 首先，通过sys.argv[1]获取命令行参数中的书名。
- 然后，使用os.path.join函数将书名和'src'拼接起来，得到目录的路径。
- 使用os.path.exists函数检查目录是否存在，如果不存在则使用os.makedirs函数创建目录。
- 确保目录存在后，使用os.path.join函数将目录路径和'SUMMARY.md'拼接起来，得到输出文件的路径。
- 使用open函数创建输出文件对象，并以写入模式打开。
- 向输出文件写入Markdown文件的标题。
- 调用output_markdown函数生成Markdown文件的目录结构。
- 打印提示信息。
- 返回0。

**注意**: 
- 在使用该函数之前，需要确保sys和os模块已经导入。
- 该函数会根据给定的书名生成目录的路径，并创建目录。
- 该函数会生成Markdown文件的标题，并调用output_markdown函数生成Markdown文件的目录结构。
- 该函数会打印提示信息，并返回0。

**调用示例**: 
- main()

**引用对象**: 
- output_markdown: 根据给定的目录生成Markdown文件的目录结构。

**输出示例**: 
- GitBook自动生成目录完成:)
