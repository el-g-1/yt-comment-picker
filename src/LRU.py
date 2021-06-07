from collections import deque

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.queue_next = 0
        self.queue_curr = 0
        self.dict = {}

    def get(self, key):
        if key in self.dict:
            self.update_queue(key)
            return self.dict[key][0]
        return None

    def put(self, key, value):
        if key in self.dict:
            self.update_queue(key)
            self.dict[key] = (value, self.queue_next - 1)
        else:
            if self.capacity == 0:
                removed = self.queue[self.queue_curr]
                while removed == None:
                    removed = self.queue[self.queue_curr]
                    self.queue_curr += 1
                val, queue_idx = self.dict[removed]
                self.queue[queue_idx] = None
                del self.dict[removed]
                self.capacity += 1
            self.queue.append(key)
            self.dict[key] = (value, self.queue_next)
            self.queue_next += 1
            self.capacity -= 1

    def update_queue(self, key):
        val, queue_idx = self.dict[key]
        self.queue[queue_idx] = None
        self.queue.append(key)
        self.dict[key] = (val, self.queue_next)
        self.queue_next += 1