from Cachelib.LinuxCache import LinuxCache, LinuxCacheParallel
from Cachelib.MedoCache import MedoCache
from Cachelib.V6dCache import V6dCache
from simulator import singleserversim
import sys, csv

def run_single_server_sim(memory_size):
    local_memory_size = memory_size*1024
    high_limit_ratio = 0.7
    low_limit_ratio = 0.3
    memory_high = local_memory_size*high_limit_ratio
    memory_low = local_memory_size*low_limit_ratio
    medocache = MedoCache(memory_high, memory_low)
    medocache= singleserversim(medocache)
    v6dCache = V6dCache(memory_high, memory_low)
    v6dCache= singleserversim(v6dCache)
    linuxcache = LinuxCache(memory_high, memory_low)
    linuxparallel = LinuxCacheParallel(memory_high, memory_low)

    res = [medocache.store_size, medocache.load_size, v6dCache.store_size, v6dCache.load_size, linuxcache.store_size, linuxcache.load_size, linuxparallel.store_size, linuxparallel.load_size, medocache.hotlru.spill_size, medocache.coldlru.spill_size, medocache.warmlru.spill_size, v6dCache.lru.spill_size, linuxcache.lru.spill_size, linuxparallel.lru.spill_size, medocache.hotlru.reload_size, medocache.coldlru.reload_size, medocache.warmlru.reload_size, v6dCache.lru.reload_size, linuxcache.lru.reload_size, linuxparallel.lru.reload_size]
    res = [x / 1024 for x in res]
    return res

if __name__ == '__main__':
    memory_begin = float(sys.argv[1])
    itnumm = float(sys.argv[2])
    itstep = float(sys.argv[3])
    res_list = []
    for i in range(itnumm):
        memory = memory_begin + (i+1)*itstep
        print("begin local memory = ", memory, "G")
        res_list.append(run_single_server_sim(memory))
    SavePath = "data/results/SingleServerSimResult.csv"
    with open(SavePath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["MEDO_store_size", "MEDO_load_size", "V6d_store_size", "V6d_load_size", "Linux_store_size", "Linux_load_size", "LinuxParallel_store_size", "LinuxParallel_load_size", "MEDO_hot_spill_size", "MEDO_cold_spill_size", "MEDO_warm_spill_size", "V6d_spill_size", "Linux_spill_size", "LinuxParallel_spill_size", "MEDO_hot_reload_size", "MEDO_cold_reload_size", "MEDO_warm_reload_size", "V6d_reload_size", "Linux_reload_size", "LinuxParallel_reload_size"])
        for res in res_list:
            writer.writerow(res)
    print(res_list)

