from repo_agent.runner import Runner
from repo_agent.log import logger


runner = Runner()

# runner.meta_info.target_repo_hierarchical_tree.print_recursive()
runner.run()

logger.info("文档任务完成。")