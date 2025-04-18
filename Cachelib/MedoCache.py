from Cachelib.LRU import LRU
class MedoCache:

    def __init__(self, memory_high_limit, memory_low_limit):
        self.size = -1
        self.name = 'MEDO'
        self.memory_high_limit = memory_high_limit
        self.memory_low_limit = memory_low_limit
        self.hotlru = LRU()
        self.warmlru = LRU()
        self.coldlru = LRU()
        self.memory_size = 0
        self.warmcnt = 1
        self.coldcnt = 1
        self.misscnt = 0
        self.totalcnt = 0
        self.hit_rate_list = []
        self.load_size = 0
        self.store_size = 0
    def spill_warm(self, spill_size):
        self.warmlru.remove_lru(spill_size)
    def spill_cold(self, spill_size):
        self.coldlru.remove_lru(spill_size)
    def spill_hot(self, spill_size):
        self.hotlru.remove_lru(spill_size)

    def put_block(self, key, value, type):
        self.misscnt += 1
        self.totalcnt += 1
        if type == 1:
            self.hotlru.put(key, value)
        elif type == 0:
            self.warmcnt += 1
            self.warmlru.put(key, value)
        elif type == -1:
            self.coldcnt += 1
            self.coldlru.put(key, value)
        self.memory_size = self.hotlru.memory_size() + self.warmlru.memory_size() + self.coldlru.memory_size()
        if self.memory_size > self.memory_high_limit:
            spill_size = self.memory_size - self.memory_low_limit
            warm_spill_size = spill_size*(self.coldcnt/(self.coldcnt+self.warmcnt))
            if warm_spill_size <= self.warmlru.memory_size():
                cold_spill_size = spill_size - warm_spill_size
            else:
                warm_spill_size = self.warmlru.memory_size() 
                cold_spill_size = spill_size - warm_spill_size
            # print("spill warm: ", warm_spill_size, "cold: ", cold_spill_size)
            self.spill_warm(warm_spill_size)
            self.spill_cold(cold_spill_size)
            self.compute_size()
            if self.memory_size > self.memory_low_limit:
                spill_size = self.memory_size - self.memory_low_limit
                # print("spill hot: ", spill_size)
                self.spill_hot(spill_size)
        self.compute_size()
    def compute_size(self):
        self.memory_size = self.hotlru.memory_size() + self.warmlru.memory_size() + self.coldlru.memory_size()
        return
    def get_block(self, key):
        self.totalcnt += 1
        if self.hotlru.get(key) != -1:
            return 1
        if self.warmlru.get(key) != -1:
            self.warmcnt += 1
            return 1
        if self.coldlru.get(key) != -1:
            self.warmcnt += 1
            return 1
        self.misscnt += 1
        key_pair = key.split('_')
        if self.hotlru.reload(key) != -1:
            self.hotlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+1))
            self.hotlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+2))
            self.hotlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+3))
            self.compute_size()
            self.put_block(key, self.hotlru.get(key), 1)
            self.misscnt -= 1
            self.totalcnt -= 1
            return self.get_block(key)
        if self.warmlru.reload(key) != -1:
            self.warmlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+1))
            self.warmlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+2))
            self.warmlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+3))
            value = self.warmlru.get(key)
            self.warmlru.remove(key)
            self.put_block(key, value, 1)
            self.misscnt -= 1
            self.totalcnt -= 1
            self.compute_size()
            return self.get_block(key)
        if self.coldlru.reload(key) != -1:
            self.coldlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+1))
            self.coldlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+2))
            self.coldlru.reload(key_pair[0]+'_'+str(int(key_pair[1])+3))
            value = self.coldlru.get(key)
            self.coldlru.remove(key)
            self.put_block(key, value, 1)
            self.misscnt -= 1
            self.totalcnt -= 1
            self.compute_size()
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