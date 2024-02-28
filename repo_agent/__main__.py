import sys

from repo_agent.runner import Runner, delete_fake_files
from repo_agent.log import logger


if len(sys.argv) == 1:
    runner = Runner()

    # runner.meta_info.target_repo_hierarchical_tree.print_recursive()
    runner.run()

    logger.info("文档任务完成。")
elif len(sys.argv) == 2:
    if sys.argv[1] == "clean":
        delete_fake_files()