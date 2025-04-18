from collections import deque
class LRU:
    def __init__(self):
        self.lru_queue = deque()
    
    def put(self, key):
        if key in self.lru_queue:
            self.lru_queue.remove(key)
        self.lru_queue.appendleft(key)
        
    def get(self, key):
        if key not in self.lru_queue:
            raise KeyError("Key not in LRU")
        self.lru_queue.remove(key)
        self.lru_queue.appendleft(key)
        return key
    def remove(self, key):
        if key in self.lru_queue:
            self.lru_queue.remove(key)
        else:
            raise KeyError("Key not in LRU")
    
    def clear(self):
        self.lru_queue.clear()
    
    def pop(self):
        return self.lru_queue.pop()
    
    def __len__(self):
        return self.lru_queue.__len__()
    
class MGLRU:
    def __init__(self, num_LRU = 4, clock_interval = 10, degree_threshold = 10):
        self.clock = 0
        self.clock_interval = clock_interval
        self.degree_threshold = degree_threshold
        self.num_LRU = num_LRU
        self.LRU_list = [LRU() for i in range(num_LRU)]
        self.key_lru = {}
        self.access_cnt = {}
    
    def put(self, key):
        self.clock = self.clock + 1
        if self.clock % self.clock_interval == 0:
            self.degree_adjust()
        if key in self.key_lru:
            self.LRU_list[self.key_lru[key]].remove(key)
        self.LRU_list[0].put(key)
        self.key_lru[key] = 0
        self.access_cnt[key] = 1
    
    def get(self, key):
        self.clock = self.clock + 1
        if self.clock % self.clock_interval == 0:
            self.degree_adjust()
        if key not in self.key_lru:
            raise KeyError("Key not in MGLRU")
        self.LRU_list[self.key_lru[key]].remove(key)
        self.LRU_list[self.key_lru[key]].put(key)
        self.access_cnt[key] = self.access_cnt[key] + 1
        return key
    
    def degree_adjust(self):
        for key in self.access_cnt:
            if self.access_cnt[key] > self.degree_threshold:
                self.upgrade(key)
                self.access_cnt[key] = 0
            elif self.access_cnt[key] == 0:
                self.downgrade(key)
                self.access_cnt[key] = 0
            else:
                self.access_cnt[key] = self.access_cnt[key] - 1
            
    def upgrade(self, key):
        if key not in self.key_lru:
            raise KeyError("Key not in MGLRU")
        if self.key_lru[key] == 0:
            return
        self.LRU_list[self.key_lru[key]].remove(key)
        self.key_lru[key] = self.key_lru[key] - 1
        self.LRU_list[self.key_lru[key]].put(key)
    
    def downgrade(self, key):
        if key not in self.key_lru:
            raise KeyError("Key not in MGLRU")
        if self.key_lru[key] == self.num_LRU - 1:
            return
        self.LRU_list[self.key_lru[key]].remove(key)
        self.key_lru[key] = self.key_lru[key] + 1
        self.LRU_list[self.key_lru[key]].put(key)
    
    def spill(self):
        spill_list = []
        for i in range(self.LRU_list[self.num_LRU-1].__len__()):
            key = self.LRU_list[self.num_LRU-1].pop()
            spill_list.append(key)
        if spill_list.__len__() == 0:
            while self.clock % self.clock_interval != 0:
                self.clock = self.clock + 1
            self.degree_adjust()
            # self.print_size()
            spill_list = self.spill()
        self.LRU_list[self.num_LRU-1].clear()
        for key in spill_list:
            del self.key_lru[key]
            del self.access_cnt[key]
        return spill_list

    def print_size(self):
        for i in range(self.num_LRU):
            print("LRU", i, "size:", self.LRU_list[i].__len__())
        
           
class MGLRU_Cache:
    def __init__(self, num_LRU = 4, clock_interval = 10, degree_threshold = 10, memory_size = 1000000000):
        self.name = 'MGLRU-' + str(num_LRU)
        self.mglru = MGLRU(num_LRU = num_LRU, clock_interval = clock_interval, degree_threshold = degree_threshold)
        self.memory = {}
        self.disk = {}
        self.memory_size = memory_size
        self.miss_cnt = 0
        self.total_cnt = 0
        self.hit_rate_list = []
        self.current_size = 0
        self.load_size = 0
        self.store_size = 0
        
    def spill(self):
        spill_list = []
        while spill_list.__len__() == 0:
            spill_list = self.mglru.spill()
        for key in spill_list:
            self.disk[key] = self.memory[key]
            self.current_size = self.current_size - self.memory[key]
            del self.memory[key]
        return
    
    def put_block(self, key, value, type):
        self.miss_cnt = self.miss_cnt + 1
        self.total_cnt = self.total_cnt + 1
        self.mglru.put(key)
        self.memory[key] = value
        self.current_size = self.current_size + value
        if self.current_size > self.memory_size:
            self.spill()
    
    def get_block(self, key):
        self.total_cnt = self.total_cnt + 1
        if key in self.memory:
            self.mglru.get(key)
            return 1
        
        self.miss_cnt = self.miss_cnt + 1
        if key in self.disk:
            self.memory[key] = self.disk[key]
            self.current_size = self.current_size + self.disk[key]
            self.mglru.put(key)
            del self.disk[key]
            return self.get_block(key)
        else:
            raise KeyError("Key not in disk or cache")
        
    def put_object(self, key, value, type):
        blockcnt = int(value/4)
        self.store_size = self.store_size + value
        for i in range(blockcnt):
            self.put_block(str(key)+'_'+str(i), 4 , type)
        self.hit_rate_list.append(1-self.miss_cnt/self.total_cnt)
        
    def get_object(self, key, value):
        blockcnt = int(value/4)
        self.load_size = self.load_size + value
        for i in range(blockcnt):
            self.get_block(str(key)+'_'+str(i))
        self.hit_rate_list.append(1-self.miss_cnt/self.total_cnt)