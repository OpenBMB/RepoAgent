#!/Users/yeyn/anaconda3/envs/ai-doc/bin/python
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   #修改当前工作目录

from repo_agent.runner import Runner, delete_fake_files
from repo_agent.log import logger
from repo_agent.config import CONFIG
from repo_agent.doc_meta_info import MetaInfo, DocItem
from repo_agent.utils.meta_info_utils import  make_fake_files, delete_fake_files

if len(sys.argv) == 1:
    runner = Runner()
    runner.run()
    logger.info("文档任务完成。")
elif len(sys.argv) == 2:
    if sys.argv[1] == "clean":
        delete_fake_files()
    elif sys.argv[1] == "print":
        runner = Runner()
        runner.meta_info.target_repo_hierarchical_tree.print_recursive()
    elif sys.argv[1] == "diff":
        runner = Runner()
        if runner.meta_info.in_generation_process: # 如果不是在生成过程中，就开始检测变更
            print("this command only support pre-check")
            exit()
        file_path_reflections, jump_files = make_fake_files()
        new_meta_info = MetaInfo.init_meta_info(file_path_reflections, jump_files)
        new_meta_info.load_doc_from_older_meta(runner.meta_info)
        delete_fake_files()

        ignore_list = CONFIG.get("ignore_list", [])
        DocItem.check_has_task(new_meta_info.target_repo_hierarchical_tree, ignore_list)
        if new_meta_info.target_repo_hierarchical_tree.has_task:
            print("the following docs will be generated/updated:")
            new_meta_info.target_repo_hierarchical_tree.print_recursive(diff_status = True, ignore_list = ignore_list)
        else:
            print("no docs will be generated/updated, check your source-code update")