from Cachelib.LRU import LRU
class V6dCache:

    def __init__(self, memory_high_limit, memory_low_limit):
        self.name = 'V6d'
        self.lru = LRU()
        self.memory_size = 0
        self.misscnt = 0
        self.totalcnt = 0
        self.hit_rate_list = []
        self.memory_high_limit = memory_high_limit
        self.memory_low_limit = memory_low_limit
        self.load_size = 0
        self.store_size = 0
    def spill(self, spill_size):
        self.lru.remove_lru(spill_size)

    def put_block(self, key, value):
        self.misscnt += 1
        self.totalcnt += 1
        self.lru.put(key, value)
        self.memory_size = self.lru.memory_size()
        if self.memory_size > self.memory_high_limit:
            spill_size = self.memory_size - self.memory_low_limit
            # print("spill size: ", spill_size)
            self.spill(spill_size)
        self.memory_size = self.lru.memory_size()

    def get_block(self, key):
        self.totalcnt += 1
        if self.lru.get(key) != -1:
            return 1
        self.misscnt += 1
        if self.lru.reload(key) == -1:
            print("error: key ", key, " not in disk!")
        self.put_block(key, self.lru.cache[key])
        return self.get_block(key)
    
    def put_object(self, key, value, type):
        res = self.put_block(key, value)
        self.store_size = self.store_size + value
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)
        return res
            
    def get_object(self, key, value):
        res = self.get_block(key)
        self.load_size = self.load_size + value
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)
        return res