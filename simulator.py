from Cachelib.LinuxCache import LinuxCache, LinuxCacheParallel
from Cachelib.MedoCache import MedoCache
from Cachelib.V6dCache import V6dCache
from Cachelib.MGLRU import MGLRU_Cache

def realcachesim(cache):
    import numpy as np
    datalines = np.loadtxt(open("data/traces/FRDTrace.csv","rb"),delimiter=",",skiprows=1).astype(int)
    for data in datalines:
        if data[3] == 0:
            cache.put_object(data[0], data[1]*1024, data[2])
        if data[3] == 1:
            cache.get_object(data[0], data[1]*1024)
    print("finish ", cache.name, " FRD trace simulation!")
    return cache

def singleserversim(cache):
    import numpy as np
    datalines = np.loadtxt(open("data/traces/test.csv","rb"),delimiter=",",skiprows=1).astype(int)
    for data in datalines:
        if data[3] == 0:
            cache.put_object(data[0], data[1]*1024, data[2])
        if data[3] == 1:
            cache.get_object(data[0], data[1]*1024)
    print("finish ", cache.name, " single server trace simulation!")
    return cache

def randomcachesim(cache):
    import numpy as np
    datalines = np.loadtxt(open("data/traces/RandomTrace.csv","rb"),delimiter=",",skiprows=1).astype(int)
    for data in datalines:
        if data[3] == 0:
            cache.put_object(data[0], data[1]*1024, data[2])
        if data[3] == 1:
            cache.get_object(data[0], data[1]*1024)
    print("finish", cache.name, " random data sim!")
    return cache

def save_data(name, CacheList):
    data = list(zip(*[cache.hit_rate_list for cache in CacheList]))
    import csv
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cache.name for cache in CacheList])
        for row in data:
            writer.writerow(row)
            
def draw_hit_ratio(CacheList, SavePath="HitRaio"):
    import matplotlib.pyplot as plt
    for cache in CacheList:
        plt.plot([i * 100 for i in cache.hit_rate_list], label = cache.name)

    plt.ylabel('hit rate/%',fontsize=15)
    plt.xlabel('time/s',fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc=4)
    plt.savefig(SavePath)
    plt.show()

def run_real_sim(LocalMemorySize, MemoryHighLimit, MemoryLowLimit, CacheList):
    memory_high = LocalMemorySize*MemoryHighLimit
    memory_low = LocalMemorySize*MemoryLowLimit
    
    ResultList = []
    if 'MEDO' in CacheList:
        medocache = MedoCache(memory_high, memory_low)
        ResultList.append(realcachesim(medocache))
    if 'V6d' in CacheList:
        v6dCache = V6dCache(memory_high, memory_low)
        ResultList.append(realcachesim(v6dCache))
    if 'Linux' in CacheList:
        linuxcache = LinuxCache(memory_high, memory_low)
        ResultList.append(realcachesim(linuxcache))
    if 'LinuxParallel' in CacheList:
        linuxparallel = LinuxCacheParallel(memory_high, memory_low)
        ResultList.append(realcachesim(linuxparallel))
    if 'MGLRU' in CacheList:
        mglrucache = MGLRU_Cache(memory_size=LocalMemorySize)
        ResultList.append(realcachesim(mglrucache))
    
    save_data("data/results/real_data_sim.csv", ResultList)
    draw_hit_ratio(ResultList, "data/fig/FRDHitRatio")
    
def run_random_sim(LocalMemorySize, MemoryHighLimit, MemoryLowLimit, CacheList):
    memory_high = LocalMemorySize*MemoryHighLimit
    memory_low = LocalMemorySize*MemoryLowLimit
    
    ResultList = []
    if 'MEDO' in CacheList:
        medocache = MedoCache(memory_high, memory_low)
        ResultList.append(randomcachesim(medocache))
    if 'V6d' in CacheList:
        v6dCache = V6dCache(memory_high, memory_low)
        ResultList.append(randomcachesim(v6dCache))
    if 'Linux' in CacheList:
        linuxcache = LinuxCache(memory_high, memory_low)
        ResultList.append(randomcachesim(linuxcache))
    if 'LinuxParallel' in CacheList:
        linuxparallel = LinuxCacheParallel(memory_high, memory_low)
        ResultList.append(randomcachesim(linuxparallel))
    if 'MGLRU' in CacheList:
        mglrucache = MGLRU_Cache(memory_size=LocalMemorySize)
        ResultList.append(randomcachesim(mglrucache))
    
    save_data("data/results/random_data_sim.csv", ResultList)
    draw_hit_ratio(ResultList, "data/fig/RandomHitRatio")
