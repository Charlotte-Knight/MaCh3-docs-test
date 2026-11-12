# Clusters
> **Last updated:** 20 Feb 2026

## Centrum Informatyczne Świerk (CIS), Warsaw Cluster
<img src="../_static/images/clusters-01.png" width="30%"/>

```
source /mnt/opt/spack/0.20/share/spack/setup-env.sh
spack load gcc@8.5.0%gcc@=8.5.0
spack load cmake@3.26.3%gcc@=8.5.0
spack load python@3.8.12%gcc@=8.5.0
spack load binutils@2.30%gcc@=8.5.0
spack load vdt@0.4.3
spack load git@2.40.0%gcc@=8.5.0
spack load imake
spack load makedepend
spack load xz@5.4.1%gcc@=8.5.0 #This holds LZMA
spack load libxpm@3.5.12%gcc@=8.5.0
spack load ncurses@6.4%gcc@8.5.0
spack load davix@0.8.1%gcc@8.5.0
spack load openssl@1.1.1t%gcc@=8.5.0
source /mnt/home/share/t2k/kskwarczynski/CERN_ROOT/root-6.24.08/build_root/bin/thisroot.sh
export LD_LIBRARY_PATH=/mnt/opt/spack/0.20/opt/spack/linux-centos7-ivybridge/gcc-8.5.0/vdt-0.4.3-s6mhw6a6pl7zdfbnaekxl5ad3x7jayvn/lib:$LD_LIBRARY_PATH
```


```
System: CentOS Linux 7
```

## LXPLUS, CERN Cluster
<img src="../_static/images/clusters-02.png" width="60%"/>

Works with default configuration:
```
System: Red Hat Enterprise Linux 9.3
GCC:    11.4.1
CMake:  3.20.2
ROOT:   6.30/04
```

## Fir/Rorqual/Narval, Digital Research Alliance of Canada
<img src="../_static/images/clusters-03.png" width="60%"/>

```
module load root
```
Then configuration looks like:
```
System: Red Hat Enterprise Linux 9.3
GCC:    12.3.1
CMake:  3.27.7
ROOT:   6.28/06
```
To use GPUs you can additionally use
```
module load cuda
```
For information about using CC GPUs see: https://docs.alliancecan.ca/wiki/Using_GPUs_with_Slurm

### NOTE
Using VSCode via SSH connection is now banned on Fir's login nodes! Please see the advice from sys admins: https://docs.alliancecan.ca/wiki/Visual_Studio_Code


## Your Cluster?
