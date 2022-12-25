from typing import Callable


class EventEmitter:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = dict()

    def on(self, event: str, callback: Callable):
        if event not in self.subscribers:
            self.subscribers[event] = list()

        self.subscribers[event].append(callback)

    def off(self, event: str, callback: Callable):
        if event in self.subscribers:
            self.subscribers[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        if event in self.subscribers:
            for callback in self.subscribers[event]:
                callback(*args, **kwargs)
