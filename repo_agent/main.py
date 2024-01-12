from runner import Runner
from loguru import logger

def main():
    runner = Runner()
    
    runner.run()

    logger.info("文档任务完成。")

if __name__ == "__main__":
    main()
