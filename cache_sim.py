from simulator import run_sim
import sys

if __name__ == '__main__':
    local_memory_size = float(sys.argv[1]) * 1024
    high_limit_ratio = float(sys.argv[2])
    low_limit_ratio = float(sys.argv[3])
    if sys.argv[5] == 'all':
        cachelist = ['MEDO', 'V6d', 'Linux', 'LinuxParallel', 'MGLRU']
    else:
        cachelist = sys.argv[5].split(',')
        for cache in cachelist:
            if cache not in ['MEDO', 'V6d', 'Linux', 'LinuxParallel', 'MGLRU']:
                print("Invalid cache name: ", cache)
                sys.exit(1)
    dataset = sys.argv[4]
    run_sim(local_memory_size, high_limit_ratio, low_limit_ratio, dataset, cachelist)

