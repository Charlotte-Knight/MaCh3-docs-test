# Containers

MaCh3 containers are stored in https://github.com/mach3-software/MaCh3/pkgs/container/mach3

## Setting up
If you are on cluster then due to security reasons most likely you will have singularity or apptainer, in VERY rare cases docker. If you want to setup on your private machine then use the following.

### Linux Users
Install docker or podman via your distribution package manager, instructions below: YOU ONLY NEED ONE OF THE THREE
docker: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

OR docker-desktop: [https://docs.docker.com/desktop/install/linux-install/](https://docs.docker.com/desktop/install/linux-install/)

OR podman: [https://podman.io/docs/installation](https://podman.io/docs/installation)

 docker-desktop might be slightly easier to use for those not as comfortable sysadmining linux.

### Mac Users:
 Install orbstack or docker-desktop. I highly recommend orbstack over docker-desktop:  [https://orbstack.dev/download](https://orbstack.dev/download)

Select the right version for your mac architecture
### Windows Users:
Install docker-desktop: [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)


## How to use

### Docker
To pull: `docker pull ghcr.io/mach3-software/mach3:alma9latest`<br>
now that you have pulled it use: `docker run -it --name mach3-container ghcr.io/mach3-software/mach3:alma9latest`<br>
Congratulations you just entered MaCh3 container<br>

If encountering any access issues please use:
```
export CR_PAT=<TOKEN>
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

#### GPU Support (Docker)

If your system has an NVIDIA GPU, MaCh3 containers can use it for CUDA-accelerated workloads.

Copy‑paste quick start:
```
docker run -it --gpus=all ghcr.io/mach3-software/mach3:rocky9cudav2.4.2
```
You must have:

NVIDIA GPU drivers installed on the host
Docker Desktop (Windows/Mac) or Docker Engine (Linux)
NVIDIA Container Toolkit installed

Install NVIDIA Container Toolkit:
```
##### Ubuntu / Debian
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
Verify GPU support with:
```
docker run --rm --gpus=all nvidia/cuda:12.3.2-base-ubuntu22.04 nvidia-smi
```
If successful, your GPU information will be displayed.

Run MaCh3 container with GPU enabled
```
docker run -it --gpus=all \
  --name mach3-container \
  ghcr.io/mach3-software/mach3:rocky9cudav2.4.2
```
Run with GUI + shared folders + GPU (Windows/WSL example)
```
docker run -it --gpus=all \
  -e DISPLAY=host.docker.internal:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /c/Users/<your-username>/Desktop:/hosthome \
  ghcr.io/mach3-software/mach3:rocky9cudav2.4.2
```
Verify GPU inside container

Once inside the container, run:
```
nvidia-smi
```
If configured correctly, your NVIDIA GPU will be listed.

### Singularity
To pull: `singularity pull docker://ghcr.io/mach3-software/mach3:alma9latest`<br>
now that you pulled it use: `singularity shell mach3_alma9latest.sif`<br>
Congratulations you just entered MaCh3 container<br>
now
```
cd ${MACH3_INSTALL_DIR}
source bin/setup.MaCh3.sh
```
Your MaCh3 is setup and ready.

If encountering any access issues please use:
```
export SINGULARITY_DOCKER_USERNAME=<USERNAME>
export SINGULARITY_DOCKER_PASSWORD=<TOKEN>
```

Alternatively, you can treat the container as a black box and execute exe inside the container like this.
```
singularity exec <my_container.sif> do_something.exe /path/to/input <arguments>
```


### Words of caution
They are ephemeral: When you exit the main container process, everything is thrown away.
Don't expect changes you make to the container image to persist in different containers from the same image.


### Build experiment specific MaCh3 using Core as base
Docker allow

#Use MaCh3 container as a base
```
FROM ghcr.io/mach3-software/mach3:alma9latest AS mach3t2k_build
// Clone Your MaCh3
RUN git XXXXXXX.YourMaCh3.git
// cmake
RUN cmake ../
// compile
RUN make && make install
```

### Acknowledgments
Highly inspired by lessons from Luke Pickering
