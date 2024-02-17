## _class Task
**Task**: Task的功能是创建一个任务对象，用于表示一个任务的相关信息和状态。

**属性**：
- task_id: 任务的唯一标识，类型为int。
- dependencies: 任务的依赖列表，类型为List[Task]。
- extra_info: 任务的额外信息，类型为Any，默认值为None。
- status: 任务的状态，类型为int，取值范围为0、1、2、3，分别表示未开始、正在进行、已经完成和出错了。

**代码描述**：
Task类是一个用于表示任务的类。在初始化时，需要传入任务的唯一标识task_id、任务的依赖列表dependencies和任务的额外信息extra_info。初始化完成后，会将这些参数赋值给对应的属性。同时，任务的状态status被初始化为0，表示任务未开始。

Task类的作用是用于管理任务的相关信息和状态。通过创建Task对象，可以方便地获取任务的标识、依赖关系、额外信息和状态等属性。这些属性可以帮助开发者了解任务的相关信息，从而进行任务的调度和执行。

在项目中，Task类被其他对象调用，用于创建任务对象并添加到任务字典中。通过调用Task类的add_task方法，可以创建一个新的任务对象，并将其添加到任务字典中。在创建任务对象时，需要指定任务的依赖列表和额外信息。任务对象创建完成后，会生成一个唯一的任务标识，并将任务对象添加到任务字典中。

此外，Task类还被其他对象调用，用于打印任务列表。通过调用Task类的print_task_list方法，可以将任务字典中的任务信息打印出来。打印的任务列表包括任务标识、文档生成原因、路径和依赖关系等信息，以表格的形式展示。

**注意**：
- Task类的任务标识task_id必须是唯一的，用于区分不同的任务。
- 任务的依赖列表dependencies中的任务对象必须在任务字典中存在，否则会引发异常。
- 任务的状态status表示任务的执行状态，可以根据需要进行更新和查询。
- Task类的add_task方法用于创建任务对象并添加到任务字典中，返回任务的唯一标识。
- Task类的print_task_list方法用于打印任务列表，以便查看任务的相关信息。
### _function __init__(self, task_id, dependencies, extra_info)
**__init__**: __init__函数的功能是初始化一个Task对象。

**参数**：这个函数的参数。
· task_id: 任务的ID，类型为int。
· dependencies: 任务的依赖列表，类型为List[Task]。
· extra_info: 额外的信息，类型为Any，默认值为None。

**代码说明**：这个函数用于初始化一个Task对象。在函数内部，将传入的参数赋值给对象的属性。task_id表示任务的ID，extra_info表示额外的信息，dependencies表示任务的依赖列表。status属性表示任务的状态，0表示任务未开始，1表示任务正在进行，2表示任务已经完成，3表示任务出错了。

**注意**：在使用这个函数时，需要传入task_id和dependencies参数，extra_info参数是可选的。
## _class TaskManager
**TaskManager**: TaskManager的功能是管理任务的类。

**属性**：
- task_dict: 一个字典，用于存储任务的信息，键为任务ID，值为Task对象。
- task_lock: 一个线程锁，用于保证多线程环境下的任务操作的安全性。
- now_id: 一个整数，表示当前任务的ID。
- query_id: 一个整数，表示查询任务的ID。
- sync_func: 一个函数，用于同步任务。

**代码描述**：
TaskManager类是一个用于管理任务的类。它包含了添加任务、获取下一个任务、标记任务完成等功能。

在初始化时，TaskManager类会初始化task_dict为空字典，task_lock为一个线程锁，now_id为0，query_id为0，sync_func为None。

add_task方法用于添加任务。它接受dependency_task_id和extra两个参数，其中dependency_task_id是一个任务ID的列表，extra是额外的信息。在方法内部，使用task_lock进行线程安全的操作，根据传入的参数创建一个Task对象，并将其添加到task_dict中，然后更新now_id的值，并返回新添加任务的ID。

get_next_task方法用于获取下一个任务。它接受process_id作为参数，表示进程ID。在方法内部，使用task_lock进行线程安全的操作，遍历task_dict中的任务，找到满足条件的任务，即依赖任务为空且状态为0的任务。如果找到了满足条件的任务，将其状态设置为1，并返回该任务和任务ID。如果没有找到满足条件的任务，返回None和-1。

mark_completed方法用于标记任务完成。它接受task_id作为参数，表示任务ID。在方法内部，使用task_lock进行线程安全的操作，找到对应的任务，并将其从task_dict中移除。同时，遍历task_dict中的任务，如果某个任务的依赖中包含了目标任务，将其从依赖中移除。

**注意**：在多线程环境下使用TaskManager时，需要注意对任务的操作需要使用task_lock进行线程安全的操作。

**输出示例**：
```python
task_manager = TaskManager()
task_id = task_manager.add_task([1, 2], extra="additional info")
next_task, task_id = task_manager.get_next_task(1)
task_manager.mark_completed(task_id)
```
### _function __init__(self)
**__init__**: __init__函数的功能是初始化TaskManager对象。

**参数**：
- self: 表示类实例对象本身。

**代码描述**：
__init__函数是TaskManager类的构造函数，用于初始化TaskManager对象。在初始化过程中，会为TaskManager对象的属性赋予初始值。具体属性的初始化如下：
- task_dict: 一个字典，用于存储任务的唯一标识和对应的任务对象。初始值为空字典。
- task_lock: 一个线程锁，用于保证多线程环境下对任务字典的操作的安全性。初始值为一个新的线程锁对象。
- now_id: 一个整数，表示当前任务的唯一标识。初始值为0。
- query_id: 一个整数，表示查询任务的唯一标识。初始值为0。
- sync_func: 一个函数对象，用于同步任务的执行。初始值为None。

TaskManager类的作用是用于管理任务的调度和执行。通过创建TaskManager对象，可以方便地添加、删除和查询任务。TaskManager对象内部维护了一个任务字典，用于存储任务的唯一标识和对应的任务对象。通过调用TaskManager对象的方法，可以对任务字典进行操作，实现任务的调度和执行。

在项目中，TaskManager类被其他对象调用，用于管理任务的调度和执行。通过创建TaskManager对象，可以方便地添加、删除和查询任务。在创建TaskManager对象时，会自动初始化TaskManager对象的属性，并为其赋予初始值。这些属性包括任务字典、线程锁、当前任务标识、查询任务标识和同步函数等。通过这些属性，可以方便地对任务进行管理和操作。

**注意**：
- TaskManager类的属性task_dict用于存储任务的唯一标识和对应的任务对象。任务的唯一标识必须是整数类型，任务对象必须是Task类的实例对象。
- TaskManager类的属性task_lock用于保证多线程环境下对任务字典的操作的安全性。在对任务字典进行操作时，需要先获取线程锁，以确保操作的原子性和一致性。
- TaskManager类的属性now_id用于生成任务的唯一标识。每次创建新的任务时，会自动递增now_id的值，并将其作为任务的唯一标识。
- TaskManager类的属性query_id用于生成查询任务的唯一标识。每次查询任务时，会自动递增query_id的值，并将其作为查询任务的唯一标识。
- TaskManager类的属性sync_func用于同步任务的执行。通过设置sync_func属性，可以指定任务的执行方式，如同步执行或异步执行等。
### _function all_success(self)
**all_success**: all_success函数的功能是检查任务字典是否为空。
**参数**: 该函数没有参数。
**代码描述**: 这个函数通过检查任务字典的长度是否为0来判断任务字典是否为空。如果任务字典为空，函数返回True；否则，返回False。
**注意**: 在调用这个函数之前，需要确保任务字典已经被初始化并且包含了需要执行的任务。
**输出示例**: 返回值为True或False，取决于任务字典是否为空。

这个函数的作用是检查任务字典是否为空。任务字典是一个存储任务的数据结构，它将任务的唯一标识符与任务对象进行关联。在调用这个函数之前，我们需要确保任务字典已经被初始化并且包含了需要执行的任务。

函数内部的实现非常简单。它通过比较任务字典的长度是否为0来判断任务字典是否为空。如果任务字典的长度为0，说明任务字典为空，函数返回True；否则，返回False。

这个函数的返回值可以用于判断任务字典是否为空，从而决定是否继续执行其他操作。例如，我们可以在执行多任务调度的过程中使用这个函数来判断是否所有的任务都已经完成，如果任务字典为空，说明所有的任务都已经完成，我们可以继续执行下一步操作；如果任务字典不为空，说明还有任务正在执行，我们可以等待一段时间后再次检查任务字典的状态。

需要注意的是，在调用这个函数之前，我们需要确保任务字典已经被正确地初始化，并且在执行任务的过程中，需要及时更新任务字典的状态。否则，这个函数的返回值可能会不准确。

下面是一个可能的返回值示例：
```
True
```
### _function add_task(self, dependency_task_id, extra)
**add_task**: add_task函数的功能是将任务添加到任务字典中。

**参数**：
- dependency_task_id: 依赖任务的唯一标识列表，类型为List[int]。
- extra: 任务的额外信息，类型为Any，默认值为None。

**代码描述**：
add_task函数首先使用self.task_lock对任务字典进行加锁，以确保在多线程环境下的安全操作。然后，根据依赖任务的唯一标识列表dependency_task_id，通过遍历任务字典获取对应的依赖任务对象，并将其存储在denp_tasks列表中。

接下来，add_task函数创建一个新的任务对象Task，传入参数包括任务的唯一标识self.now_id、依赖任务列表denp_tasks和额外信息extra。创建完成后，将任务对象添加到任务字典self.task_dict中，使用self.now_id作为键，任务对象作为值。

最后，add_task函数更新self.now_id的值，使其自增1，表示下一个任务的唯一标识。然后，返回新添加任务的唯一标识self.now_id减1，作为函数的返回值。

**注意**：
- 在多线程环境下，使用self.task_lock对任务字典进行加锁，以确保操作的原子性和线程安全。
- 依赖任务的唯一标识列表dependency_task_id中的任务对象必须在任务字典self.task_dict中存在，否则会引发异常。
- add_task函数会创建一个新的任务对象Task，并将其添加到任务字典self.task_dict中。
- 新添加任务的唯一标识是self.now_id减1，作为函数的返回值。

**输出示例**：
假设当前任务字典self.task_dict为空，self.now_id的初始值为0。调用add_task函数，传入dependency_task_id=[1, 2]和extra="example"，则函数会将依赖任务1和2对应的任务对象添加到任务字典中，并返回新添加任务的唯一标识2。此时，任务字典self.task_dict的内容为{2: Task(task_id=2, dependencies=[Task(task_id=1, dependencies=[], extra_info=None), Task(task_id=2, dependencies=[], extra_info=None)], extra_info="example")}。
### _function get_next_task(self, process_id)
**get_next_task**: get_next_task函数的功能是获取下一个任务。

**parameters**:
- self: 当前对象的实例
- process_id: 进程ID，表示当前进程的标识符，为整数类型

**Code Description**:
get_next_task函数用于获取下一个可执行的任务。函数首先使用self.task_lock进行线程同步，然后递增self.query_id的值。接着，通过遍历self.task_dict中的任务ID，判断当前任务是否满足可执行条件。任务的可执行条件是：任务的依赖列表为空且任务的状态为0。如果任务满足可执行条件，则将任务的状态设置为1，并记录日志信息。如果self.query_id能被10整除，则调用self.sync_func()函数进行同步操作。最后，返回满足条件的任务和任务ID。如果没有满足条件的任务，则返回None和-1。

**Note**:
- 在调用get_next_task函数之前，需要确保已经获取了self.task_lock的锁。
- 该函数是一个实例方法，需要通过对象实例来调用。

**Output Example**:
假设self.task_dict中有两个任务，任务ID分别为1和2。其中，任务1的依赖列表为空，状态为0；任务2的依赖列表为[1]，状态为0。调用get_next_task函数时，如果process_id为1，则返回任务1和任务ID 1；如果process_id为2，则返回任务2和任务ID 2。如果self.task_dict中没有满足条件的任务，则返回None和-1。
### _function mark_completed(self, task_id)
**mark_completed**: mark_completed函数的功能是将指定任务标记为已完成。

**参数**：该函数的参数如下：
- task_id: int类型，表示要标记为已完成的任务的ID。

**代码说明**：mark_completed函数的作用是将指定任务标记为已完成。在函数内部，首先使用self.task_lock对任务字典进行加锁，以确保在多线程环境下的数据安全。然后，通过任务ID从任务字典中获取目标任务对象target_task。接下来，遍历任务字典中的所有任务，对于每个任务，如果目标任务target_task存在于其依赖列表中，则将其从依赖列表中移除。最后，使用任务ID从任务字典中删除目标任务。

**注意**：在使用mark_completed函数时，需要确保传入的任务ID存在于任务字典中，并且任务字典是线程安全的。此外，该函数会修改任务字典中的数据，因此在使用该函数时需要注意数据一致性的问题。
## _function worker(task_manager, process_id, handler)
**worker**: worker函数的作用是执行任务并标记任务为已完成。

**参数**：
- task_manager: 任务管理器对象，用于获取下一个任务和标记任务完成。
- process_id: 进程ID，用于区分不同的工作进程。
- handler: 任务处理函数，用于执行任务的具体操作。

**代码说明**：
worker函数是一个无限循环的函数，它会不断地从任务管理器中获取下一个任务，并执行任务的处理函数。如果任务管理器中的所有任务都已经完成，函数会立即返回。

在每次循环中，函数首先检查任务管理器的all_success属性，如果为True，则表示所有任务已完成，函数会立即返回。

接下来，函数调用task_manager的get_next_task方法获取下一个任务和任务ID。如果获取到的任务为None，表示当前没有可执行的任务，函数会暂停0.5秒后继续下一次循环。

如果获取到了任务，函数会调用handler函数执行任务的具体操作，传入任务的额外信息作为参数。

最后，函数调用task_manager的mark_completed方法标记任务为已完成。

**注意**：
- worker函数是一个长时间运行的函数，需要在合适的时机终止循环。
- handler函数需要根据任务的额外信息来执行具体的任务操作。
- 在循环中使用time.sleep方法可以避免CPU占用过高。

**输出示例**：
无返回值。
## _function some_function
**some_function**: some_function函数的功能是随机睡眠一段时间。

**参数**：这个函数的参数。
· 无参数

**代码描述**：这个函数使用了time模块的sleep函数来实现睡眠功能。sleep函数的参数是一个浮点数，表示睡眠的秒数。在这个函数中，使用了random模块的random函数来生成一个0到1之间的随机数，然后乘以3，得到一个0到3之间的随机秒数。最后，调用sleep函数来实现随机睡眠。

**注意**：在使用这个函数时，需要导入time和random模块。另外，需要注意的是，这个函数是一个阻塞函数，即在调用这个函数时，程序会暂停执行一段时间，直到睡眠时间结束才会继续执行后面的代码。
