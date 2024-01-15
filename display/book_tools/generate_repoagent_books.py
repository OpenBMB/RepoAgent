import os
import shutil

import sys


def main():
    markdown_docs_folder = sys.argv[1]
    book_name = sys.argv[2]
    repo_path = sys.argv[3]

    # mkdir the book folder
    dst_dir = os.path.join('./books', book_name, 'src')
    docs_dir = os.path.join(repo_path, markdown_docs_folder)

    # check the dst_dir
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print("mkdir %s" % dst_dir)

    # cp the Markdown_Docs_folder to dst_dir
    for item in os.listdir(docs_dir):
        src_path = os.path.join(docs_dir, item)
        dst_path = os.path.join(dst_dir, item)

        # check the src_path
        if os.path.isdir(src_path):
            # if the src_path is a folder, use shutil.copytree to copy
            shutil.copytree(src_path, dst_path)
            print("copytree %s to %s" % (src_path, dst_path))
        else:
            # if the src_path is a file, use shutil.copy2 to copy
            shutil.copy2(src_path, dst_path)
            print("copy2 %s to %s" % (src_path, dst_path))

    def create_book_readme_if_not_exist(dire):
        readme_path = os.path.join(dire, 'README.md')

        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as readme_file:
                readme_file.write('# {}\n'.format(book_name))

    # create book README.md if not exist
    create_book_readme_if_not_exist(dst_dir)


if __name__ == '__main__':
    main()
