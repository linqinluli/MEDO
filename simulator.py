from Cachelib.LinuxCache import LinuxCache, LinuxCacheParallel
from Cachelib.MedoCache import MedoCache
from Cachelib.V6dCache import V6dCache
from Cachelib.MGLRU import MGLRU_Cache

def cachesim(Cache, DatasetPath):
    import numpy as np
    datalines = np.loadtxt(open(DatasetPath,"rb"),delimiter=",",skiprows=1).astype(int)
    for data in datalines:
        if data[3] == 0:
            Cache.put_object(data[0], data[1]*1024, data[2])
        if data[3] == 1:
            Cache.get_object(data[0], data[1]*1024)
    print("Finish ", Cache.name, " ", DatasetPath, " trace simulation!")
    return Cache

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

def run_sim(LocalMemorySize, MemoryHighLimit, MemoryLowLimit, dataset, CacheList):
    memory_high = LocalMemorySize*MemoryHighLimit
    memory_low = LocalMemorySize*MemoryLowLimit
    
    DatasetPath = dataset
    if dataset == "FRD":
        DatasetPath = "data/traces/FRDTrace.csv"
    elif dataset == "random":
        DatasetPath = "data/traces/RandomTrace.csv"
    ResultList = []
    if 'MEDO' in CacheList:
        medocache = MedoCache(memory_high, memory_low)
        ResultList.append(cachesim(medocache, DatasetPath))
    if 'V6d' in CacheList:
        v6dCache = V6dCache(memory_high, memory_low)
        ResultList.append(cachesim(v6dCache, DatasetPath))
    if 'Linux' in CacheList:
        linuxcache = LinuxCache(memory_high, memory_low)
        ResultList.append(cachesim(linuxcache, DatasetPath))
    if 'LinuxParallel' in CacheList:
        linuxparallel = LinuxCacheParallel(memory_high, memory_low)
        ResultList.append(cachesim(linuxparallel, DatasetPath))
    if 'MGLRU' in CacheList:
        mglrucache = MGLRU_Cache(memory_size=LocalMemorySize)
        ResultList.append(cachesim(mglrucache, DatasetPath))
    
    save_data("data/results/HitRatioData.csv", ResultList)
    draw_hit_ratio(ResultList, "data/fig/HitRatio")
    