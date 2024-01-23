from __future__ import annotations
import threading
import time
import random
from typing import List, Callable, Dict, Any

from repo_agent.log import logger

class Task:
    def __init__(self, task_id: int, dependencies: List[Task],extra_info: Any = None):
        self.task_id = task_id
        self.extra_info = extra_info
        self.dependencies = dependencies
        self.status = 0 #任务状态：0未开始，1正在进行，2已经完成，3出错了


class TaskManager:
    def __init__(self):
        self.task_dict: Dict[int, Task]  = {}
        self.task_lock = threading.Lock()
        self.now_id = 0
        self.query_id = 0
        self.sync_func = None

    @property
    def all_success(self) -> bool:
        return len(self.task_dict) == 0

    def add_task(self, dependency_task_id: List[int], extra=None) -> int:
        with self.task_lock:
            denp_tasks = [self.task_dict[task_id] for task_id in dependency_task_id]
            self.task_dict[self.now_id] = Task(task_id=self.now_id, dependencies=denp_tasks, extra_info=extra)
            self.now_id += 1
            return self.now_id - 1

    def get_next_task(self, process_id: int):
        with self.task_lock:
            self.query_id += 1
            for task_id in self.task_dict.keys():
                ready = (len(self.task_dict[task_id].dependencies) == 0) and self.task_dict[task_id].status == 0
                if ready:
                    self.task_dict[task_id].status = 1
                    logger.info(f"[{process_id}] get task_id {task_id}, remain task: {len(self.task_dict)}")
                    if self.query_id % 10 == 0:
                        self.sync_func()
                    return self.task_dict[task_id], task_id
            return None, -1
        
    def mark_completed(self, task_id: int):
        with self.task_lock:
            target_task = self.task_dict[task_id]
            for task in self.task_dict.values():
                if target_task in task.dependencies:
                    task.dependencies.remove(target_task)
            self.task_dict.pop(task_id)
                


def worker(task_manager, process_id: int, handler: Callable):
    while True:
        if task_manager.all_success:
            return
        task, task_id = task_manager.get_next_task(process_id)
        if task is None: 
            time.sleep(0.5)
            continue
        # print(f"will perform task: {task_id}")
        handler(task.extra_info)
        task_manager.mark_completed(task.task_id)
        # print(f"task complete: {task_id}")


if __name__ == "__main__":

    task_manager = TaskManager()
    def some_function(): #随机睡一会
        time.sleep(random.random()*3)
    # 添加任务，例如：
    i1 = task_manager.add_task(some_function, [])
    i2 = task_manager.add_task(some_function, [])
    i3 = task_manager.add_task(some_function, [i1])
    i4 = task_manager.add_task(some_function, [i2, i3])
    i5 = task_manager.add_task(some_function, [i2, i3])
    i6 = task_manager.add_task(some_function, [i1])
    
    threads = [threading.Thread(target=worker, args=(task_manager,)) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()