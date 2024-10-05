import threading


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class OrderNumberService(metaclass=SingletonMeta):
    def __init__(self):
        self._current_number = 0
        self._lock = threading.Lock()

    def get_next_order_number(self) -> int:

        with self._lock:
            self._current_number += 1
            return self._current_number
