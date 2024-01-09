import os
import re
import sys


def create_readme_if_not_exist(dire):
    readme_path = os.path.join(dire, 'README.md')

    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as readme_file:
            dirname = os.path.basename(dire)
            readme_file.write('# {}\n'.format(dirname))


# def output_markdown(dire, base_dir, output_file, iter_depth=0):
#     for filename in os.listdir(dire):
#         print('add readme ', filename)
#         file_or_path = os.path.join(dire, filename)
#         if os.path.isdir(file_or_path):
#             create_readme_if_not_exist(file_or_path)
#
#     for filename in os.listdir(dire):
#         print('deal with ', filename)
#         file_or_path = os.path.join(dire, filename)
#         if os.path.isdir(file_or_path):
#             # create_readme_if_not_exist(file_or_path)
#
#             if markdown_file_in_dir(file_or_path):
#                 output_file.write('  ' * iter_depth + '- ' + filename + '\n')
#                 output_markdown(file_or_path, base_dir, output_file,
#                                 iter_depth + 1)
#         else:
#             if is_markdown_file(filename):
#                 if (filename not in ['SUMMARY.md',
#                                      'README.md']
#                         or iter_depth != 0):
#                     output_file.write('  ' * iter_depth +
#                                       '- [{}]({})\n'.format(is_markdown_file(filename),
#                                                             os.path.join(os.path.relpath(dire, base_dir),
#                                                                          filename)))

def output_markdown(dire, base_dir, output_file, iter_depth=0):
    for filename in os.listdir(dire):
        print('add readme ', filename)
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path):
            create_readme_if_not_exist(file_or_path)

    for filename in os.listdir(dire):
        print('deal with ', filename)
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path):
            # Check if README.md exists in the directory
            readme_path = os.path.join(file_or_path, 'README.md')
            if os.path.exists(readme_path):
                # If README.md exists, create a markdown link to it
                relative_path = os.path.join(os.path.relpath(file_or_path, base_dir), 'README.md')
                output_file.write('  ' * iter_depth + '- [{}]({})\n'.format(filename, relative_path))
            # Recursively call output_markdown for nested directories
            output_markdown(file_or_path, base_dir, output_file, iter_depth + 1)
        else:
            if is_markdown_file(filename):
                if filename not in ['SUMMARY.md', 'README.md'] or iter_depth != 0 and filename not in ['README.md']:
                    relative_path = os.path.join(os.path.relpath(dire, base_dir), filename)
                    output_file.write('  ' * iter_depth + '- [{}]({})\n'.format(is_markdown_file(filename), relative_path))



def markdown_file_in_dir(dire):
    for root, dirs, files in os.walk(dire):
        for filename in files:
            if re.search('.md$|.markdown$', filename):
                return True
    return False


def is_markdown_file(filename):
    match = re.search('.md$|.markdown$', filename)
    if not match:
        return False
    elif len(match.group()) is len('.md'):
        return filename[:-3]
    elif len(match.group()) is len('.markdown'):
        return filename[:-9]


def main():
    book_name = sys.argv[1]

    # mkdir the book folder
    dir_input = os.path.join('./books', book_name, 'src')

    # check the dst_dir
    if not os.path.exists(dir_input):
        print(dir_input)
        os.makedirs(dir_input)
    # Ensure the directory exists or create it
    if not os.path.exists(dir_input):
        os.makedirs(dir_input)

    # Then proceed to create the file
    output_path = os.path.join(dir_input, 'SUMMARY.md')
    output = open(output_path, 'w')
    # output = open(os.path.join(dir_input, 'SUMMARY.md'), 'w')
    output.write('# Summary\n\n')
    output_markdown(dir_input, dir_input, output)

    print('GitBook auto summary finished:) ')
    return 0


if __name__ == '__main__':
    main()
