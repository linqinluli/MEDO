from collections import deque
class LRU:

    def __init__(self):
        self.cache = dict()
        self.lru_queue = deque()
        self.tmpmemory = 0
        self.spill_size = 0
        self.reload_size = 0
        self.diskstore = dict()
        
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.lru_queue.remove(key)
        self.lru_queue.appendleft(key)
        return self.cache[key]
    
    def memory_size(self):
        return self.tmpmemory
    
    def remove(self, key):
        self.tmpmemory -=self.cache[key]
        self.lru_queue.remove(key)
        
        del self.cache[key]
    
    def remove_lru(self, remove_size):
        while(self.tmpmemory!=0 and remove_size > 0):
            old_key = self.lru_queue.pop()
            self.diskstore[old_key] = self.cache[old_key]
            self.tmpmemory -=self.cache[old_key]
            remove_size -= self.cache[old_key]
            self.spill_size = self.spill_size + self.cache[old_key]
            del self.cache[old_key]
            
    def reload(self, key):
        if key not in self.diskstore:
            return -1
        self.reload_size = self.reload_size + self.diskstore[key]
        self.put(key, self.diskstore[key])
        del self.diskstore[key]
        
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(key)
        self.cache[key] = value
        self.tmpmemory+=value
        self.lru_queue.appendleft(key)







