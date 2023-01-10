from typing import Callable


class TasksQueue:
    """
    Special class for managing tasks queue.\n
    Useful for creating tasks that run some routine, wait for something and only then
    return result WITHOUT stopping all other proccesses.\n
    Example:\n
    Let's say you have to call some functions that send request to a server and wait for response.
    The best way running them all would be using TasksQueue: you don't need to think about every routine,
    have they finished yet or not, etc.
    """

    def __init__(self):
        self.tasks = []

    def push(self, task: Callable[..., bool], *args, **kwargs):
        """
        Push task to the queue.\n
        task - function, that returns tuple (args, kwargs) for next call if task is not finished and None otherwise
        *args, **kwargs - function arguments
        """
        self.tasks.append((task, args, kwargs))

    def run(self):
        while self.tasks:
            task, args, kwargs = self.tasks.pop(0)

            result = task(*args, **kwargs)

            if result is not None:
                self.tasks.append((task, result[0], result[1]))


queue = TasksQueue()


def count_to(to: int, current_index: int = 0):
    print(current_index)

    if to == current_index:
        return None
    else:
        return ((to, current_index + 1), {})


queue.push(count_to, 6)


while queue.tasks:
    queue.run()
