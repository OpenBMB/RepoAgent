from __future__ import annotations

import random
import threading
import time
from typing import Any, Callable, Dict, List

from colorama import Fore, Style


class Task:
    def __init__(self, task_id: int, dependencies: List[Task], extra_info: Any = None):
        self.task_id = task_id
        self.extra_info = extra_info
        self.dependencies = dependencies
        self.status = 0  # 任务状态：0未开始，1正在进行，2已经完成，3出错了


class TaskManager:
    def __init__(self):
        """
        Initialize a MultiTaskDispatch object.

        This method initializes the MultiTaskDispatch object by setting up the necessary attributes.

        Attributes:
        - task_dict (Dict[int, Task]): A dictionary that maps task IDs to Task objects.
        - task_lock (threading.Lock): A lock used for thread synchronization when accessing the task_dict.
        - now_id (int): The current task ID.
        - query_id (int): The current query ID.
        - sync_func (None): A placeholder for a synchronization function.

        """
        self.task_dict: Dict[int, Task] = {}
        self.task_lock = threading.Lock()
        self.now_id = 0
        self.query_id = 0
        self.sync_func = None

    @property
    def all_success(self) -> bool:
        return len(self.task_dict) == 0

    def add_task(self, dependency_task_id: List[int], extra=None) -> int:
        """
        Adds a new task to the task dictionary.

        Args:
            dependency_task_id (List[int]): List of task IDs that the new task depends on.
            extra (Any, optional): Extra information associated with the task. Defaults to None.

        Returns:
            int: The ID of the newly added task.
        """
        with self.task_lock:
            depend_tasks = [self.task_dict[task_id] for task_id in dependency_task_id]
            self.task_dict[self.now_id] = Task(
                task_id=self.now_id, dependencies=depend_tasks, extra_info=extra
            )
            self.now_id += 1
            return self.now_id - 1

    def get_next_task(self, process_id: int):
        """
        Get the next task for a given process ID.

        Args:
            process_id (int): The ID of the process.

        Returns:
            tuple: A tuple containing the next task object and its ID.
                   If there are no available tasks, returns (None, -1).
        """
        with self.task_lock:
            self.query_id += 1
            for task_id in self.task_dict.keys():
                ready = (
                    len(self.task_dict[task_id].dependencies) == 0
                ) and self.task_dict[task_id].status == 0
                if ready:
                    self.task_dict[task_id].status = 1
                    print(
                        f"{Fore.RED}[process {process_id}]{Style.RESET_ALL}: get task({task_id}), remain({len(self.task_dict)})"
                    )
                    if self.query_id % 10 == 0:
                        self.sync_func()
                    return self.task_dict[task_id], task_id
            return None, -1

    def mark_completed(self, task_id: int):
            """
            Marks a task as completed and removes it from the task dictionary.

            Args:
                task_id (int): The ID of the task to mark as completed.

            """
            with self.task_lock:
                target_task = self.task_dict[task_id]
                for task in self.task_dict.values():
                    if target_task in task.dependencies:
                        task.dependencies.remove(target_task)
                self.task_dict.pop(task_id) # 从任务字典中移除


def worker(task_manager, process_id: int, handler: Callable):
    """
    Worker function that performs tasks assigned by the task manager.

    Args:
        task_manager: The task manager object that assigns tasks to workers.
        process_id (int): The ID of the current worker process.
        handler (Callable): The function that handles the tasks.

    Returns:
        None
    """
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

    def some_function():  # 随机睡一会
        time.sleep(random.random() * 3)

    # 添加任务，例如：
    i1 = task_manager.add_task(some_function, []) # type: ignore
    i2 = task_manager.add_task(some_function, []) # type: ignore
    i3 = task_manager.add_task(some_function, [i1]) # type: ignore
    i4 = task_manager.add_task(some_function, [i2, i3]) # type: ignore
    i5 = task_manager.add_task(some_function, [i2, i3]) # type: ignore
    i6 = task_manager.add_task(some_function, [i1]) # type: ignore

    threads = [threading.Thread(target=worker, args=(task_manager,)) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
