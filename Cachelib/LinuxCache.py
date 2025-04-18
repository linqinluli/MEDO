from Cachelib.LRU import LRU
class LinuxCache:
    def __init__(self, memory_high_limit, memory_low_limit):
        self.name = 'Linux'
        self.size = -1
        self.memory_high_limit = memory_high_limit
        self.memory_low_limit = memory_low_limit
        self.lru = LRU()
        self.memory_size = 0
        self.misscnt = 0
        self.totalcnt = 0
        self.hit_rate_list = []
        self.load_size = 0
        self.store_size = 0
    def spill(self, spill_size):
        self.lru.remove_lru(spill_size)

    def put_block(self, key, value, type):
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
        self.lru.reload(key)
        self.put_block(key, self.lru.cache[key], 1)
        return self.get_block(key)
    
    def put_object(self, key, value, type):
        blockcnt = int(value/4)
        self.store_size = self.store_size + value
        for i in range(blockcnt):
            self.put_block(str(key)+'_'+str(i), 4 , type)
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)
    def get_object(self, key, value):
        blockcnt = int(value/4)
        self.load_size = self.load_size + value
        for i in range(blockcnt):
            self.get_block(str(key)+'_'+str(i))
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)

class LinuxCacheParallel:

    def __init__(self, memory_high_limit, memory_low_limit):
        self.name = 'LinuxParallel'
        self.size = -1
        self.memory_high_limit = memory_high_limit
        self.memory_low_limit = memory_low_limit
        self.lru = LRU()
        self.memory_size = 0
        self.misscnt = 0
        self.totalcnt = 0
        self.hit_rate_list = []
        self.load_size = 0
        self.store_size = 0
    def spill(self, spill_size):
        self.lru.remove_lru(spill_size)

    def put_block(self, key, value, type):
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
        key_pair = key.split('_')
        self.lru.reload(key)
        self.lru.reload(key_pair[0]+'_'+str(int(key_pair[1])+1))
        self.lru.reload(key_pair[0]+'_'+str(int(key_pair[1])+2))
        self.lru.reload(key_pair[0]+'_'+str(int(key_pair[1])+3))
        self.put_block(key, self.lru.cache[key], 1)
        self.put_block(key_pair[0]+'_'+str(int(key_pair[1])+1), self.lru.cache[key_pair[0]+'_'+str(int(key_pair[1])+1)], 1)
        self.put_block(key_pair[0]+'_'+str(int(key_pair[1])+2), self.lru.cache[key_pair[0]+'_'+str(int(key_pair[1])+1)], 1)
        self.put_block(key_pair[0]+'_'+str(int(key_pair[1])+3), self.lru.cache[key_pair[0]+'_'+str(int(key_pair[1])+1)], 1)
        return self.get_block(key)
    
    def put_object(self, key, value, type):
        blockcnt = int(value/4)
        self.store_size = self.store_size + value
        for i in range(blockcnt):
            self.put_block(str(key)+'_'+str(i), 4 , type)
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)
    def get_object(self, key, value):
        blockcnt = int(value/4)
        self.load_size = self.load_size + value
        for i in range(blockcnt):
            self.get_block(str(key)+'_'+str(i))
        self.hit_rate_list.append(1-self.misscnt/self.totalcnt)