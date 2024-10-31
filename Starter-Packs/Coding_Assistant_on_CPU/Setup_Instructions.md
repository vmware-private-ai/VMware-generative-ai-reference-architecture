
# Running an AI Coding Assistant on VCF 5.2.1 VMs Powered by AMD EPYC CPUs.

# Introduction

This technical document provides the configuration details of an Ubuntu 24.04 (desktop) developer VM hosted by VCF 5.2.1. The developer VM aims to use the StarChat2-15b-v0.1 large language model (LLM) as a coding assistant, running exclusively on AMD EPYC™ 9654 CPUs.

# Main Components

- AMD EPYC™ 9654 (96-core socket) CPUs, 2 per physical host.  
- 24 x RDIMM 64 GB per physical.  
- AMD optimized `gcc` compiler and libraries (AOCC and AOCL) 5.0.0  
- vSphere 8.0 U3 virtual infrastructure  
- Ubuntu 24.04 desktop OS  
- StarChat2-15b-v0.1 LLM  
- Llama.cpp (b3943) compiled from source with AMD AOCC and AOCL  
- MS VS Code 1.94.2  
- Collama VS Code extension.

# VM Setup

## Ubuntu 24.04 Developer VM

To reproduce the developer VM configuration described in this technical document, you must deploy Ubuntu 24.04 on a VM running on vSphere 8 (we used vSphere 8.0 u3). To install operating systems on vSphere VMs, refer to the [*Install a* *Guest Operating System documentation*](https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-vm-administration/GUID-90E7F734-D699-4603-B222-AF4DE84459C7.html).

We set up a developer VM with Ubuntu 24.04 to facilitate access to more up-to-date development tools such as `Python 12` and `gcc 13`. Ubuntu's "desktop" version provides a GENOME IDE that allows users to run VS Code and other GUI-based development tools.

## **vCPU Configuration**

1. Set the number of virtual CPUs to match one socket of the AMD EPYC 9654:  
   * The EPYC 9654 has 96 cores per socket  
   * Configure the VM with 96 vCPUs.  
2. Use virtual sockets instead of cores per socket:  
   * Set "Number of Virtual Sockets" to 96  
   * Set "Number of cores per socket" to 1\.  
3. Configure CPU reservation:  
   * Set the CPU reservation to 100% of the allocated vCPUs.  
   * This guarantees that all 96 cores are exclusively reserved for this VM.  
4. Enable manual NUMA configuration:  
   * This allows you to control how the VM's resources are aligned with the physical NUMA nodes.  
   * Set the VM to use resources from a single NUMA node corresponding to one physical CPU socket.  
5. Set the ESXi host power policy to "High Performance" to ensure maximum CPU performance.

## VM Memory Reservations

1. In our case, we gave the VM 128 GB of memory to give the CPU cores access to multiple physical memory modules.  
   - Note: If you use smaller memory modules, you could reduce the memory assigned to the developer VM to 64 or 32 GB, sufficient to run the StarChat2 LLM.  
2. In the VM memory reservation settings, tick the "Reserve all guest memory" box.

# Llama.cpp setup

## About llama.cpp and the AMD optimization libraries and compiler.

`llama.cpp` is a powerful open-source C++ library for efficient large language model (LLM) inference, particularly on CPU-based systems. Developed by Georgi Gerganov, it optimizes LLM performance through advanced quantization techniques, reducing model size and computational requirements. This enables faster inference and broader applicability across various platforms, including those with limited resources.

Compiling `llama.cpp` from source using AMD AOCL and AOCC can significantly enhance LLM inference performance on AMD EPYC CPUs. This approach leverages the EPYC architecture's high core counts and large cache sizes, which are well-suited for LLM workloads. Users can achieve substantial performance improvements without specialized GPU hardware by utilizing AOCL's optimized BLAS implementations and AOCC's advanced code generation.

This CPU-only solution offers cost savings and increased deployment flexibility for organizations using AMD EPYC-based infrastructure.

## Compiler infrastructure setup

To install the AMD-optimized gcc compiler and libraries, run the commands from a shell terminal in the Ubuntu 24.04 desktop VM.

### Install `cmake`.

```
# Install  cmake
sudo apt-get update
sudo apt-get install cmake
```

### Install the `libcurses5` and `libstdc++-13-dev` libraries

```
wget http://archive.ubuntu.com/ubuntu/pool/universe/n/ncurses/libtinfo5_6.4-2_amd64.deb && sudo dpkg -i libtinfo5_6.4-2_amd64.deb && rm -f libtinfo5_6.4-2_amd64.deb

wget http://archive.ubuntu.com/ubuntu/pool/universe/n/ncurses/libncurses5_6.4-2_amd64.deb && sudo dpkg -i libncurses5_6.4-2_amd64.deb && rm -f libncurses5_6.4-2_amd64.deb

sudo apt install libncurses5 libncurses5-dev -y 

sudo apt install libstdc++-13-dev

```

### Download the AMD AOCC package.

Visit the [AMD AOCC download page](https://www.amd.com/en/developer/aocc.html) and download the latest `.deb` package for Ubuntu. In our setup, we utilized [aocc-compiler-5.0.0\_1\_amd64.deb](https://www.amd.com/en/developer/aocc/eula/aocc-5-0-eula.html?filename=aocc-compiler-5.0.0_1_amd64.deb). Once downloaded, execute the following commands to install it. 

### Install AOCC

```
sudo dpkg -i aocc-compiler-5.0.0_1_amd64.deb
```

Add the required environment variables to `.bashrc` and source it:

```
# Add the following env variables to your .bashrc file
export AOCC_ROOT=/opt/AMD/aocc-compiler-5.0.0
export PATH=$AOCC_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$AOCC_ROOT/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=$AOCC_ROOT/lib:$LIBRARY_PATH
export CPATH=$AOCC_ROOT/include:$CPATH

# Then source it
source ~/.bashrc

```

Verify the installation

```
clang --version

# AMD clang version 17.0.6 (CLANG: AOCC_5.0.0-Build#1377 2024_09_24)
# Target: x86_64-unknown-linux-gnu
# Thread model: posix
# InstalledDir: /opt/AMD/aocc-compiler-5.0.0/bin
```

### Install AMD AOCL

Download the AMD AOCL `.deb` file, which is available from [this link](https://www.amd.com/en/developer/aocl/eula/aocl-5-0-eula.html?filename=aocl-linux-aocc-5.0.0_1_amd64.deb).

Now install the AOCL package:

```
sudo dpkg -i aocl-linux-aocc-5.0.0_1_amd64.deb

```

Add the required environment variables to `.bashrc` and source it:

```
# Add the following env variables to your .bashrc file
export AOCL_ROOT=/opt/AMD/aocl/aocl-linux-aocc-5.0.0/aocc
export LD_LIBRARY_PATH=$AOCL_ROOT/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=$AOCL_ROOT/lib:$LIBRARY_PATH
export CPATH=$AOCL_ROOT/include:$CPATH

# Then source it
source ~/.bashrc
```

## Compiling `llama.cpp` from source

Download `llama.cpp` by "git-cloning" its GitHub repository:

- Note: If not installed yet, you can install `git` using the following command:  
    
  `sudo apt install git`

```
# Clone and enter the llama.cpp repository

cd && mkdir code && cd code
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

Create and enter the `build` compilation directory:

```
mkdir build && cd build
```

Save the following code in a file called `config_cmake.sh`

```
CC=/opt/AMD/aocc-compiler-5.0.0/bin/clang CXX=/opt/AMD/aocc-compiler-5.0.0/bin/clang++ cmake .. \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_C_FLAGS="-march=znver4 -mtune=znver4 -O3 -ffast-math -flto -fno-finite-math-only" \
-DCMAKE_CXX_FLAGS="-march=znver4 -mtune=znver4 -O3 -ffast-math -flto -fno-finite-math-only" \
-DLLAMA_BLAS=ON \
-DLLAMA_BLAS_VENDOR=OpenBLAS \
-DCMAKE_PREFIX_PATH=/opt/AMD/aocl/aocl-linux-aocc-5.0.0/aocc \
-DLLAMA_NATIVE=ON \
-DLLAMA_AVX=ON \
-DLLAMA_AVX2=ON \
-DLLAMA_FMA=ON \
-DLLAMA_F16C=ON
```

Source the `config_cmake.sh` file:

```
source config_cmake.sh
```

Compile llama.cpp binaries. This step will take between 2-3 minutes.

```
# The `j96` parameter matches the 96 vCPUs of our lab VM
# If you have less vGPUs in your VM, reduce the number accordingly. 

cmake --build . --config Release -j96
```

Once the compilation process is finished, you'll be ready to server LLMs using the AMD-optimized version of `llama.cpp`.

# Running and testing StarChat2 LLM llama.cpp

## About StarChat2

We decided to use `StarChat2` (15 billion parameters, 16k tokens of context size) LLM in this technical document because it is robust and provides high-quality query completions. Once you get to a working setup, you might try other coding assistant LLMs of a similar size.

## Model download

Download the `StarChat2` (quantized by HF user `Bartowski`) LLM from the HF model repository. Please refer to the [model card](https://huggingface.co/HuggingFaceH4/starchat2-15b-v0.1) document to understand the model's licensing, intended usage, and other relevant information.

```
cd && mkdir starchat2 && cd starchat2
wget https://huggingface.co/bartowski/starchat2-15b-v0.1-GGUF/resolve/main/starchat2-15b-v0.1-Q5_K_S.gguf
```

## Llama.cpp server setup

Return to the lama.cpp build directory and add the following code to a file named `run_server.sh` in the build directory. Notice we use a number of threads equal to `num_vCPUs - 2`.

```
# Return to the build directory
cd ~/code/llama.cpp/build

# Insert the following test into a file named run_server.sh 
./bin/llama-server -m ~/starchat2/starchat2-15b-v0.1-Q5_K_S.gguf \
  -c 0 \
  --host 0.0.0.0 \
  --port 8080 \
  --mlock \
  --numa isolate \
  -cb \
  -t 94
```

Run the server

```
chmod +x run_server.sh
./run_server.sh


```

Create a text script named `test_rest_inf.sh` in the build directory. If `curl` is not installed, you can install it with the command `sudo apt install curl`.

```
curl --request POST \
    --url http://localhost:8080/completion \
    --header "Content-Type: application/json" \
    --data '{"prompt": "Implement a quick sort function in Python.","n_predict": 512,"temperature":0}'

```

Run the test script:

```
chmod +x test_rest_inf.sh
./test_rest_inf.sh

```

You should see a return message like the following within 15-16 seconds:

````
{"content":"\n\nThe quick sort algorithm follows the divide-and-conquer approach. It works by selecting a pivot element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then recursively sorted.\n\nHere is the implementation of the quick sort function in Python:\n\n```python\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n```\n\nYou can test the function with an example:\n\n```python\narr = [3, 6, 8, 10, 1, 2, 1]\nsorted_arr = quick_sort(arr)\nprint(sorted_arr)\n```\n\nOutput:\n```\n[1, 1, 2, 3, 6, 8, 10]\n```\n\nThe time complexity of the quick sort algorithm is O(n log n) in the average case and O(n^2) in the worst case. The space complexity is O(log n) due to the recursive calls.\n\nNote: The implementation above uses list comprehensions to partition the array. You can also implement it using loops if you prefer.","id_slot":0,"stop":true,"model":"/home/vmuser/starchat2/starchat2-15b-v0.1-Q5_K_S.gguf","tokens_predicted":340,"tokens_evaluated":8,"generation_settings":{"n_ctx":2048,"n_predict":-1,"model":"/home/vmuser/starchat2/starchat2-15b-v0.1-Q5_K_S.gguf","seed":4294967295,"seed_cur":4294967295,"temperature":0.0,"dynatemp_range":0.0,"dynatemp_exponent":1.0,"top_k":40,"top_p":0.949999988079071,"min_p":0.05000000074505806,"xtc_probability":0.0,"xtc_threshold":0.10000000149011612,"tfs_z":1.0,"typical_p":1.0,"repeat_last_n":64,"repeat_penalty":1.0,"presence_penalty":0.0,"frequency_penalty":0.0,"mirostat":0,"mirostat_tau":5.0,"mirostat_eta":0.10000000149011612,"penalize_nl":false,"stop":[],"max_tokens":512,"n_keep":0,"n_discard":0,"ignore_eos":false,"stream":false,"n_probs":0,"min_keep":0,"grammar":"","samplers":["top_k","tfs_z","typ_p","top_p","min_p","xtc","temperature"]},"prompt":"Implement a quick sort function in Python.","has_new_line":true,"truncated":false,"stopped_eos":true,"stopped_word":false,"stopped_limit":false,"stopping_word":"","tokens_cached":347,

"timings":{"prompt_n":8,"prompt_ms":92.608,"prompt_per_token_ms":11.576,"prompt_per_second":86.38562543192812,"predicted_n":340,"predicted_ms":15497.658,"predicted_per_token_ms":45.581347058823525,"predicted_per_second":21.938798752688957},"index":0}
real    0m15.606s
user    0m0.005s
sys     0m0.011s
````

# Setup Python environment for VS Code

## Install pip3

```
sudo apt install python3-pip
```

## Install pipenv

```
sudo apt install pipenv
```

## Setup a `pipenv` virtual environment to test the AI assistant

Add `PIPENV_VENV_IN_PROJECT=1` to `~/.bashrc` and source it. Then run the following code block:

```
mkdir ~/code/test_assist && cd ~/code/test_assist
pipenv --python 3.12
pipenv shell
pipenv install pandas scikit-learn xgboost jupyter
```

Please install MS VS Code using the App Center application available in Ubuntu 24.04 Desktop. After installing VS Code, from the `~/code/test_assist` directory, run the command `code` to open VS Code.

With VS Code up and running, make sure you install the following extensions:

- `Python` by Microsoft  
    
- `Jupyter` by Microsoft  
    
- `collama` by rickyang (v0.16.9). This extension requires the following setup:  
    
  - At the `Server Endpoint,` enter `http://127.0.0.1:8080`  
  - At the `Autocomplete Max Tokens` value, enter `100`  
  - At the `Chat Max Tokens` value, enter `10240`  
  - Enable `Inline chat`


- From VS Code File Explorer, open the `code/test_assist` folder.  
    
- Confirm you trust the authors of `code` directory.  
    
- From the `File` menu, select `New File` and create a new `Jupyter Notebook.`  
    
- In the top right corner of VS Code, click on `select kernel`, then click on  `Python environments` nd select the one whose name starts with `test-assist...`  
    
- Now click the Cody (collama) icon (left edge) to open the assistant chat window. In the message box type the following prompt:

```
Write the Python code to train an XGBoost model for classifying the Iris dataset. Include data loading, preprocessing, model training, and a simple evaluation. Use scikit-learn to load the dataset and split it into training and testing sets. Return the code in a single cell and add comments where you consider appropriate.
```

As you can see, the prompt requires de LLM to generate the Python code to perform multiple data science tasks, such as:

- Download a dataset.  
- Preprocess the dataset, including splitting it into training and test sets.  
- Fit the required model which is `xgboost` in this case.  
- Run predictions on the test set and evaluate the model's accuracy.

After you submit the prompt to Cody (collama) you will see it incrementally generating (streaming) a code block similar to this:

```
# Import required libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# Load Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create XGBoost classifier
model = XGBClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy: %.2f%%' % (accuracy * 100.0))
```

Copy and paste the previous code into a single Jupyter Notebook code cell. Run the cell and wait for it to finish. You should see a model evaluation accuracy of 100%, which is a powerful demonstration of StarChat2 coding capabilities.

Now, from VS Code's `File` menu, select `New File,` and create a new Python file. At the `collama` chat box, insert the following prompt:

```
Create a unit test for the XGBoost model training code you just wrote. The test should verify that the model achieves aminimum accuracy threshold on the test set. Include necessary imports and use the unittest framework.
```

The assistant will incrementally generate (stream) the unitest Python code script.

Copy the code and paste it into the Python script. Save the script as `unitest.py,` which will be saved in the `~/code/test_assist` directory.

From a terminal, run the following command: `python unitest.py`

You should see something similar to the following output:

```
--------------------------------------------------------
Ran 1 test in 0.129s

OK
```

This result confirms that the code initially generated by the coding assistant for the Jupyter Notebook is correct.

This concludes the AI coding assistant demonstration. As you can see, effective AI coding assistants can be enabled by using open-source LLMs such as StarChat2 and running these LLMs on last-generation CPUs such as AMD EPYC.
