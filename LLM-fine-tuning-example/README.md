# Example use case: Fine-tune a large language model (LLM) on a single VM.

## 1. Introduction to fine-tuning task.

The open-source community keeps releasing new LLMs, such as [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b) and [Falcon-7B](https://huggingface.co/tiiuae/falcon-7b), which at the time of this writing rank at the top of the [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard?_hsenc=p2ANqtz-865CMxeXG2eIMWb7rFgGbKVMVqV6u6UWP8TInA4WfSYvPjc6yOsNPeTNfS_m_et5Atfjyw). This working example will guide how to finetune these models on a specific dataset and use tuned model for prompt completion by using one or two mid-range GPUs.

As a complementary resource we have published a GitHub repo that provides the Python code required to finetune Falcon-7B using a single A100 (40G) GPU and Falcon-40B on two of those GPUs by using HugginFace's implementation of [LoRA](https://huggingface.co/docs/peft/conceptual_guides/lora) (part of the [PEFT](https://huggingface.co/docs/peft/index) package) and the [bits and bytes](https://github.com/TimDettmers/bitsandbytes) library (by [Tim Dettmers](https://github.com/TimDettmers)) to load the models using 8-bit or 4-bit quantization numeric precision.

## 2. Requirements

We will assume that you already have an [Ubuntu 22.04 LTS Desktop](https://ubuntu.com/desktop) ready with the following minimum requirements:

- 1 or 2 NVIDIA A100 (40GB) GPUs attached either as vGPU or DirectPath I/O devices. You can use other NVIDIA GPUs will less memory but that might limit the size of the model you'll be able to load.
- 64GB or RAM
- 16 vCPU
- 500GB of disk storage. Notice that the more model checkpoints you decide to keep, the more storage space you will need.
- Internet connectivity to download software packages, LLM models and datasets.

For more details about the configuration steps on vSphere to use NVIDA GPUs, please refer to [Configuring Virtual Graphics in vSphere](https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-resource-management/GUID-74A657D9-52F7-4F92-AB86-9039A90A028D.html)

## 3. Python environment setup

### Installing CUDA 11.8

First you need to install the NVIDIA driver for Ubuntu 22.04. 
- From the graphical interface, launch the `Software and Updtes` application. Select the
`Additional Drivers` tab and from the `NVIDIA Corporation` section pick the driver that is labeled as `(propietary, tested)`. When building this 
working example, we picked `driver 535`. After selecting the driver, the system will get reconfigured. Even if you're no asked to do so, it 
is convenient to reboot the OS with the command:
```azure
reboot
```

Next, you need to download the CUDA 11.8 toolkit and install it. Follow the next steps:

````
# Download the binaries for Ubuntu 22.04
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run

# Execute the run file
sudo sh cuda_11.8.0_520.61.05_linux.run
````
The CLI command will start a text-based dialog interface. You will get a warming like this:
````
┌──────────────────────────────────────────────────────────────────────────────┐
│ Existing package manager installation of the driver found. It is strongly    │
│ recommended that you remove this before continuing.                          │
│ Abort                                                                        │
│ Continue                                                                     │
│                                                                              │
````
Using the keyboard arrows, select `Continue` and hit `Enter`. Next, you need to accept the EULA to continue.
````
Do you accept the above EULA? (accept/decline/quit):                         │
  │ accept 
````
Then use the keyboard to move down the screen and using the space bar, deselect the `Driver`, the `CUDA Demo Suite` and the `CUDA documentation`. Then move to the `Install`
option and hit `Enter` as shown next.
````
┌──────────────────────────────────────────────────────────────────────────────┐
│ CUDA Installer                                                               │
│ - [ ] Driver                                                                 │
│      [ ] 520.61.05                                                           │
│ + [X] CUDA Toolkit 11.8                                                      │
│   [ ] CUDA Demo Suite 11.8                                                   │
│   [ ] CUDA Documentation 11.8                                                │
│ - [ ] Kernel Objects                                                         │
│      [ ] nvidia-fs                                                           │
│   Options                                                                    │
│   Install                                                                    │
│                                                                              │
│ Up/Down: Move | Left/Right: Expand | 'Enter': Select | 'A': Advanced options │
└──────────────────────────────────────────────────────────────────────────────┘
````
Once the installer finishes, add a new line to `/etc/ld.so.conf` with the `/usr/local/cuda-11.8/lib64` entry an run:
````azure
sudo ldconfig
````
CUDA will get installed under `/usr/local`
````azure
ls /usr/local
# cuda  cuda-11.8  etc  games  include  lib  man  sbin  share  src
````

### Miniconda installation steps.

We recommend the use of [Miniconda](https://docs.conda.io/en/latest/miniconda.html) as the Python package management system over the default 
distributions embedded in the OS. Here the shell commands you need to run to setup a Python environment.<br>

```shell
## Installing Miniconda

# Downloading the latest Miniconda installer for Linux.

wget -nc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Perform a Miniconda silent installation

bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda

# Add Conda activation, assuming you use bash as SHELL

eval "$($HOME/miniconda/bin/conda shell.bash hook)"

# With this activated shell, install conda's shell functions

conda init
```
#### Python virtual environment setup.

Let's clone the git repository for the Jupyter notebook that contains the LLM fine-tune code:

```shell
## Cloning the git repo

# Verify git is installed
git --version

# If git is not installed, pleade install it with these two commands
sudo apt update
sudo apt install git

# Clone the git repo containing the fine-tune Jupyter notebook
git clone https://github.com/vmware-ai-labs/VMware-generative-ai-reference-architecture.git

# Enter the fine-tune example directory
cd VMware-generative-ai-reference-architecture/LLM-fine-tuning-example/
```

Then run the following commands to create a conda virtual environment:

```shell
## Setting-up the virtual env for LLM tasks

# Create the conda virtual env

conda env create -f llm-env.yaml

# Create the virtual env using a conda dependency specification

# - The package versions in the YAML file have been tested by our experiments

conda activate llm-env

# OPTIONAL: login to wandb.ai using the CLI

# - The wandb.ai dashboard allows you to follow the training process online.
# - You'll need free account and an API key
# - See details at https://docs.wandb.ai/quickstart

wandb login

# Start Jupyter-lab session

jupyter-lab
```

Next, your web browser will show a JupyterLab session like the one shown next. Double click on the `Notebook-Falcon-finetune.ipynb` file to open the notebook and get ready to go over the Falcon LLM fine-tune process. Once the notebook is open you may follow the notebook annotations which explain the LLM fine-tune process and the role of each component of it.
