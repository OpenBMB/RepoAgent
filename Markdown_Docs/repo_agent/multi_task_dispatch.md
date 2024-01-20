## _class Task
**Task**: Task的功能是表示一个任务，并管理任务的状态和依赖关系。
**属性**: 
- task_id: 任务的唯一标识符，类型为int。
- extra_info: 任务的额外信息，类型为任意类型，默认为None。
- dependencies: 任务的依赖关系，类型为Task对象的列表。
- status: 任务的状态，0表示未开始，1表示正在进行，2表示已经完成，3表示出错了。
**代码描述**: Task类是一个表示任务的类，它有一个构造函数__init__，用于初始化任务的属性。构造函数接受三个参数：task_id表示任务的唯一标识符，dependencies表示任务的依赖关系，extra_info表示任务的额外信息，默认为None。构造函数将这些参数赋值给对应的属性。status属性默认为0，表示任务未开始。
**注意**: 
- Task类用于表示一个任务，并管理任务的状态和依赖关系。
- 任务的状态可以通过status属性进行访问和修改。
- 任务的依赖关系可以通过dependencies属性进行访问和修改。
- 任务的额外信息可以通过extra_info属性进行访问和修改。
## _class TaskManager
**TaskManager**: TaskManager的功能是管理任务的类。

**属性**: 
- task_dict: 一个字典，用于存储任务的字典，键为任务ID，值为Task对象。
- task_lock: 一个线程锁，用于保证多线程操作时的数据安全。
- now_id: 一个整数，表示当前任务的ID。
- query_id: 一个整数，表示查询任务的ID。
- sync_func: 一个函数，用于同步任务。

**代码描述**: 
TaskManager类是一个任务管理器，用于管理任务的添加、获取、标记完成等操作。它具有以下功能：

- all_success属性：返回一个布尔值，表示是否所有任务都已完成。
- add_task方法：添加一个任务到任务字典中，并返回任务的ID。可以指定依赖的任务ID列表和额外信息。
- get_next_task方法：获取下一个可执行的任务，并返回任务对象和任务ID。可以指定进程ID。
- mark_completed方法：标记任务为已完成，并更新其他任务的依赖关系。

**注意**: 
- TaskManager类是线程安全的，使用了线程锁来保证多线程操作时的数据安全。
- 任务ID是自增的，每次添加任务时会自动分配一个新的ID。
- 任务的依赖关系通过任务ID来表示，可以根据依赖关系来确定任务的执行顺序。

**输出示例**:
```python
task_manager = TaskManager()
task_id = task_manager.add_task([1, 2], extra="additional info")
task, task_id = task_manager.get_next_task(1)
task_manager.mark_completed(task_id)
```
### _class_function __init__(self)
**__init__**: __init__函数的功能是初始化TaskManager对象的属性。
**参数**: 该函数没有参数。
**代码描述**: __init__函数通过给TaskManager对象的属性赋初值来初始化对象。它包括以下属性的初始化：
- task_dict: 一个字典，用于存储任务的唯一标识符和对应的Task对象。
- task_lock: 一个线程锁，用于保证对task_dict的操作的线程安全。
- now_id: 一个整数，表示当前任务的唯一标识符。
- query_id: 一个整数，表示查询任务的唯一标识符。
- sync_func: 一个函数，用于同步任务的执行。

**注意**: 
- TaskManager对象用于管理任务的执行和查询。
- task_dict属性用于存储任务的唯一标识符和对应的Task对象。
- task_lock属性用于保证对task_dict的操作的线程安全。
- now_id属性用于生成任务的唯一标识符。
- query_id属性用于生成查询任务的唯一标识符。
- sync_func属性用于同步任务的执行。
### _class_function all_success(self)
**all_success**: all_success函数的作用是判断任务字典是否为空。
**参数**: 该函数没有参数。
**代码描述**: all_success函数通过比较任务字典的长度是否为0来判断任务字典是否为空。如果任务字典为空，则返回True；否则返回False。
**注意**: 使用该代码时需要注意任务字典的数据类型，确保任务字典是一个有效的字典对象。
**输出示例**: 假设任务字典为空，函数将返回True。
### _class_function add_task(self, dependency_task_id, extra)
**add_task**: add_task函数的功能是将一个任务添加到任务管理器中。
**参数**: 
- dependency_task_id: 依赖的任务ID列表，类型为List[int]。
- extra: 任务的额外信息，类型为任意类型，默认为None。
**代码描述**: add_task函数首先通过依赖的任务ID列表获取对应的任务对象，然后将这些任务对象以及额外信息作为参数创建一个新的任务对象，并将其添加到任务管理器的任务字典中。接着，将当前任务ID加1，并返回当前任务ID减1作为新添加任务的ID。
**注意**: 
- add_task函数用于将一个任务添加到任务管理器中。
- 任务的依赖关系通过dependency_task_id参数指定。
- 任务的额外信息可以通过extra参数指定。
**输出示例**: 返回新添加任务的ID。
### _class_function get_next_task(self, process_id)
**get_next_task**: get_next_task函数的作用是获取下一个任务。
**参数**: 这个函数的参数是process_id，表示进程的ID。
**代码描述**: 这个函数首先使用self.task_lock进行线程锁定，然后递增self.query_id。接着，它遍历self.task_dict中的所有任务ID。对于每个任务ID，它判断任务的依赖是否为空且任务的状态是否为0，如果满足条件，则将任务的状态设置为1，并输出日志信息。如果self.query_id能被10整除，则调用self.sync_func()函数。最后，返回任务和任务ID。如果没有满足条件的任务，则返回None和-1。
**注意**: 使用这段代码时需要注意以下几点：
- 需要确保在调用get_next_task函数之前已经获取了self.task_lock的锁定。
- 需要确保在调用get_next_task函数之后释放了self.task_lock的锁定。
**输出示例**: 假设self.task_dict中有满足条件的任务，返回的结果可能是(task, task_id)。如果没有满足条件的任务，则返回的结果是(None, -1)。
### _class_function mark_completed(self, task_id)
**mark_completed**: mark_completed函数的功能是将指定任务标记为已完成。
**parameters**: mark_completed函数的参数为task_id，表示要标记为已完成的任务的ID。
**Code Description**: mark_completed函数的代码逻辑如下：
1. 使用self.task_lock对任务字典进行加锁，确保在操作任务字典时不会发生并发问题。
2. 根据task_id从任务字典中获取目标任务target_task。
3. 遍历任务字典中的所有任务，对于每个任务task：
   - 如果target_task在task的依赖列表中，就将target_task从依赖列表中移除。
4. 使用task_id从任务字典中删除已完成的任务target_task。
**Note**: 
- 在调用mark_completed函数之前，需要确保任务字典self.task_dict中存在指定的task_id。
- mark_completed函数会修改任务字典self.task_dict的内容，因此在调用该函数时需要注意并发访问的问题。
## _function worker(task_manager, process_id, handler)
**worker**: worker函数的作用是处理任务的工作函数。
**参数**: worker函数接受三个参数：
- task_manager: 任务管理器，用于获取下一个任务并标记任务完成。
- process_id: 进程ID，用于区分不同的工作进程。
- handler: 任务处理函数，用于处理任务的额外信息。

**代码描述**: worker函数是一个无限循环的函数，它会不断地从任务管理器中获取下一个任务并进行处理，直到所有任务都完成。具体的处理过程如下：
1. 首先判断任务管理器中的所有任务是否都已经完成，如果是，则直接返回。
2. 调用任务管理器的get_next_task方法获取下一个任务和任务ID。
3. 如果获取到的任务为空，则等待0.5秒后继续下一次循环。
4. 调用任务处理函数handler，传入任务的额外信息进行处理。
5. 调用任务管理器的mark_completed方法标记任务完成。

**注意**: 
- worker函数是一个无限循环的函数，只有当任务管理器中的所有任务都完成时才会退出循环。
- worker函数的执行需要依赖任务管理器和任务处理函数的正确实现。
- 在处理任务的过程中，可以根据实际需求对任务进行额外的处理或操作。

**输出示例**:
假设任务管理器中有3个任务，任务的额外信息分别为"info1"、"info2"和"info3"，任务处理函数为打印任务的额外信息。则worker函数的执行过程如下：
```
将执行任务: 1
info1
将执行任务: 2
info2
将执行任务: 3
info3
```
## _function some_function
**some_function**: some_function的功能是随机睡一会
**参数**: 这个函数没有参数
**代码描述**: 这个函数使用了time模块的sleep方法来实现睡眠功能。sleep方法接受一个参数，表示睡眠的时间，这里使用了random模块的random方法生成一个0到1之间的随机数，并乘以3作为睡眠时间。这样就实现了随机睡眠的功能。
**注意**: 使用这个函数时需要导入time和random模块。调用这个函数后，程序会暂停执行一段随机时间，时间的范围在0到3之间。
