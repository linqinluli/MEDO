# MEDO [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15253482.svg)](https://zenodo.org/records/15253482)

This is the simulation code for MEDO and other swap algorithms. We inplement algorithms including MEDO, V6d, Linux, LinuxParallel, MGLRU.

**MEDO**: The algorithm proposed by us. It is the subsystem of cloud memory pool. MEDO manges the data offloading of the memory node in the memory pool.

**V6d** ([Vineyard](https://v6d.io/)): Vienyard. An in-memory data sharing system. We implement V6d's data spill algorithm. It is a single-LRU object-based algorithm.

**Linux** ([Linux swap](https://docs.kernel.org/mm/swap.html)): The old Linux swap mechanism. It is a single-LRU page-based algorithm.

**LinuxParallel**: The parallel version of Linux swap mechanism. We implement the Linux swap with parallel data swap in and out for comparison. It is a single-LRU page-based algorithm.

**MGLRU** ([Linux MGLRU](https://docs.kernel.org/admin-guide/mm/multigen_lru.html)): The newest Linux swap mechanism. It is a multi-LRU page-based algorithm.

## Directory Structure
```
├── Cachelib
|   └──  The implementation of cache algorithms
├── data
|   ├── fig: the output figures
|   ├── results: the hit ratio data and cluster simluation data
|   └── traces: the trace data
├── cache_sim.py: the cache simulator
├── cluster_sim.py: the cluster simulator
├── requirements.txt: the required packages
├── simulator.py: the simulator for two traces
```

## Requirements
```
pip install -r requirements.txt
```
## Datasets
We provide two datasets: FRD and random.

**FRD**: The dataset used in the paper. It is the data access trace of a fraud risk detection system task.

**Random**: A random dataset generated whose features are aligned with the features described in the paper.

You can generate your own dataset. It should follow the format described below:
1. The head of the dataset should be: `key,value,type,operation`
2. Key is unique for each data object.
3. Value is the size of the data object in GB.
4. Type is the type of the data object. -1 means MED, 0 means LED, 1 means IED (MED, LED, IED are described in the paper).
5. Operation is the operation performed on the data object. 0 means put, 1 means get.
6. Objects cannot be got before they are put.

## Running the code
To run the code, simply run the following command in the terminal:

**Cache simulator:**
```
python cache_sim.py $local_memory_size $high_limit_ratio $low_limit_ratio $dataset $algorithms
```
-- local_memory_size: the size of local memory in GB. e.g. 128

-- high_limit_ratio: the ratio of highest memory to trigger data offloading. less than 1.0. e.g. 0.8

-- low_limit_ratio: the ratio of lowest memory in local memory affter data offloading. less than 1.0. e.g. 0.2

-- dataset: the dataset to use. supported datasets: random, FRD. Input the csv file path of your dataset if you want to use your own dataset. e.g. data/traces/test.csv

-- algorithms: the algorithms to use. supported algorithms: MEDO, V6d, Linux, LinuxParallel, MGLRU. all means simulate all algorithms. e.g. MEDO,V6d,Linux,LinuxParallel,MGLRU

The hit ratio data will be saved in `data/results/`.

The output figure will be saved in `data/fig/`

Example:

Simulate MEDO V6d MGLRU on FRD dataset with local memory size 128 and high-low priority ratio 0.8-0.2:
```
python cache_sim.py 128 0.8 0.2 FRD MEDO,V6d,MGLRU

```
Simulate all algorithms on random dataset with local memory size 256 and high-low priority ratio 0.7-0.3:
```
python cache_sim.py 256 0.7 0.3 random all
```

Simulate all algorithms on provided dataset with local memory size 256 and high-low priority ratio 0.7-0.3:
```
python cache_sim.py 256 0.7 0.3 data/traces/test.csv all
```

**Cluster simulator:**
```
python cluster_sim.py $memory_begin $itnumm $itstep
```
-- memory_begin: the beginning memory size in GB. e.g. 256

-- itnumm: the number of iterations for memory size. e.g. 5

-- itstep: the step size for memory size. e.g. 128

The detail data will be saved in `data/results/SingleServerSimResult.csv`.

Example:

Simulate the performance of a server with memory from 256GB to 256+5*128 GB:
```
python cluster_sim.py 256 5 128
```
