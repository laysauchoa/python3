from collections import deque
def search(iterable, predicate):
    for item in iterable:
        if predicate(item):
            return item
    raise ValueError("Not found")


def async_search(iterable, predicate):
    for item in iterable:
        if predicate(item):
            return item
        yield
    raise ValueError("Not found")

class Task:
    next_id = 0

    def __init__(self, routine):
        self.id = Task.next_id
        Task.next_id = Task.next_id + 1
        self.routine = routine

class Scheduler:
    def __init__(self):
        self.runnable_tasks = deque()
        self.completed_task_results = {}
        self.failed_task_errors = {}

    def add(self, routine): #wraps routine and add the task to the queue
        task = Task(routine)
        self.runnable_tasks.append(task)
        return task.id

    def run_to_completion(self):
        while len(self.runnable_tasks) != 0:
            task = self.runnable_tasks.popleft()
            print("Running task ... {}".format(task.id), end='')
            try:
                yielded = next(task.routine)
            except StopIteration as stopped:
                print("complete with the result: {!r}", format(stopped.value))
                self.completed_task_results[task.id] = stopped.value
            except Exception as e:
                print("failed with exception: {}".format(e))
                self.failed_task_errors[task.id] = e
            else:
                assert yielded is None
                print("now yielded")
                self.runnable_tasks.append(task)

