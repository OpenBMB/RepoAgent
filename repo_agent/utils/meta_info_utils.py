import itertools
import os

import git
from colorama import Fore, Style

from repo_agent.log import logger
from repo_agent.settings import setting

latest_verison_substring = "_latest_version.py"


def make_fake_files():
    """根据git status检测暂存区信息。如果有文件：
    1. 新增文件，没有add。无视
    2. 修改文件内容，没有add，原始文件重命名为fake_file，新建原本的文件名内容为git status中的文件内容
    3. 删除文件，没有add，原始文件重命名为fake_file，新建原本的文件名内容为git status中的文件内容
    注意: 目标仓库的文件不能以latest_verison_substring结尾
    """
    delete_fake_files()
    
    repo = git.Repo(setting.project.target_repo)
    unstaged_changes = repo.index.diff(None) #在git status里，但是有修改没提交
    untracked_files = repo.untracked_files #在文件系统里，但没在git里的文件

    jump_files = [] #这里面的内容不parse、不生成文档，并且引用关系也不计算他们
    for file_name in untracked_files:
        if file_name.endswith(".py"):
            print(f"{Fore.LIGHTMAGENTA_EX}[SKIP untracked files]: {Style.RESET_ALL}{file_name}")
            jump_files.append(file_name)
    for diff_file in unstaged_changes.iter_change_type('A'): #新增的、没有add的文件，都不处理
        if diff_file.a_path.endswith(latest_verison_substring):
            logger.error("FAKE_FILE_IN_GIT_STATUS detected! suggest to use `delete_fake_files` and re-generate document")
            exit()
        jump_files.append(diff_file.a_path)


    file_path_reflections = {}
    for diff_file in itertools.chain(unstaged_changes.iter_change_type('M'),unstaged_changes.iter_change_type('D')):  # 获取修改过的文件
        if diff_file.a_path.endswith(latest_verison_substring):
            logger.error("FAKE_FILE_IN_GIT_STATUS detected! suggest to use `delete_fake_files` and re-generate document")
            exit()
        now_file_path = diff_file.a_path #针对repo_path的相对路径
        if now_file_path.endswith(".py"):
            raw_file_content = diff_file.a_blob.data_stream.read().decode("utf-8")
            latest_file_path = now_file_path[:-3] + latest_verison_substring
            if os.path.exists(os.path.join(setting.project.target_repo,now_file_path)):
                os.rename(os.path.join(setting.project.target_repo,now_file_path), os.path.join(setting.project.target_repo, latest_file_path))
                
                print(f"{Fore.LIGHTMAGENTA_EX}[Save Latest Version of Code]: {Style.RESET_ALL}{now_file_path} -> {latest_file_path}")
            else:
                print(f"{Fore.LIGHTMAGENTA_EX}[Create Temp-File for Deleted(But not Staged) Files]: {Style.RESET_ALL}{now_file_path} -> {latest_file_path}") 
                with open(os.path.join(setting.project.target_repo,latest_file_path), "w") as writer:
                    pass
            with open(os.path.join(setting.project.target_repo,now_file_path), "w") as writer:
                writer.write(raw_file_content)
            file_path_reflections[now_file_path] = latest_file_path #real指向fake
    return file_path_reflections, jump_files


def delete_fake_files():
    """在任务执行完成以后，删除所有的fake_file
    """
    def gci(filepath):
        # 遍历filepath下所有文件，包括子目录
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                gci(fi_d)
            elif fi_d.endswith(latest_verison_substring):
                origin_name = fi_d.replace(latest_verison_substring, ".py")
                os.remove(origin_name)
                if os.path.getsize(fi_d) == 0:
                    print(f"{Fore.LIGHTRED_EX}[Deleting Temp File]: {Style.RESET_ALL}{fi_d[len(setting.project.target_repo):]}, {origin_name[len(setting.project.target_repo):]}")
                    os.remove(fi_d)
                else:
                    print(f"{Fore.LIGHTRED_EX}[Recovering Latest Version]: {Style.RESET_ALL}{origin_name[len(setting.project.target_repo):]} <- {fi_d[len(setting.project.target_repo):]}")
                    os.rename(fi_d, origin_name)

    gci(setting.project.target_repo)