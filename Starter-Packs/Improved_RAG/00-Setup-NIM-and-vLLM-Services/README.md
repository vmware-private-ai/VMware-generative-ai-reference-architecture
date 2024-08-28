# Launching Nvidia NIM and vLLM Services

## Overview

This directory contains a set of Linux shell scripts that can be used to launch the Nvidia NIM services
required to implement retrieval augmented generation (RAG) pipelines. These services are: 
- __Text generation__ by large language models (LLMs), 
- __Embedding of text strings__ (queries, sentences, etc.), and 
- __Re-ranking of text passages__ according to their semantic similarity or relevance to a query. 

I addition to NIMs, you'll need vLLM to run the 
__[meta-llama/Meta-Llama-3-70B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct)__ 
LLM to leverage vLLM's __[guided JSON](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)__
feature that is required to use an LLM as a _"judge"_ for 
__[DeepEval](https://docs.confident-ai.com/docs/getting-started)__ to evaluate the different architectures of 
RAG pipelines that get covered in this Starter Pack.

Notice that you'll need multiple GPU resources to run the different NIMs as indicated below. In our 
tests __we used a VM with 8 x H100 (80GB) GPUs__ but you can use other Nvidia GPUs like A100, L40s, 
A10G and L4 as indicated in each NIM's support matrix.

Finally, we provide pointers to the ___Getting Started___ documentation for each NIM. Make sure you follow those
documents to understand how to authenticate at __Nvidia's NCG services__ so you can pull the NIM containers. Once you have 
authenticated and generated your `NGC_API_KEY`, __please plug it into `line 2` of the scripts launching NIMs__.

## Setting up NIM services for RAG pipelines


- __NVIDIA NIM for Text Embedding.__ This 
[NIM's documentation](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/index.html) includes a 
[Getting Started](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/getting-started.html) 
section that provides all the steps required to get access to the NIM containers and how to launch them. In this
directory we provide the __`embedder_launch.sh`__ script that contains the environment variable definitions
and the `docker run` command line required to launch the NIM container. There are a 
few things to consider:
  - When using the __`embedder_launch.sh`__ script, make sure you adjust the port number assigned to the
embedding service. In this script, the service becomes available at `port 8000` by default.
  - In this Starter Pack we use the `NV-EmbedQA-E5-v5` model which requires one of the GPUs indicated
in the [NV-EmbedQA-E5-v5's supported hardware](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/support-matrix.html#supported-hardware)
section.
  - The script runs the container on the 4th GPU device by default (` --gpus '"device=3"'`).
  - Notice the `NV-EmbedQA-E5-v5` model supports a __maximum token count of 512__.
  

- __NVIDIA Text Reranking NIM.__ This
  [NIM's documentation](https://docs.nvidia.com/nim/nemo-retriever/text-reranking/latest/index.html) also includes a
  [Getting Started](https://docs.nvidia.com/nim/nemo-retriever/text-reranking/latest/getting-started.html)
  section with all the steps required to pull and launch the NIM containers. In this
  directory we provide the __`reranker_launch.sh`__ script that contains the environment variable definitions
  and the `docker run` command line required to launch the NIM container. There are a
  few things to consider:
  - When using the __`reranker_launch.sh`__ script, the service becomes available at `port 8010` by default.
  - In this Starter Pack we use the `nv-rerankqa-mistral-4b-v3` model which requires one of the GPUs indicated
  in the [nv-rerankqa-mistral-4b-v3's supported hardware](https://docs.nvidia.com/nim/nemo-retriever/text-reranking/latest/support-matrix.html#supported-hardware)
   section.
   -  The script runs the container on the 3rd GPU device by default (` --gpus '"device=2"'`). 
   - Notice the `NV-EmbedQA-E5-v5` model supports a __maximum token count of 512__.


- __NVIDIA  NIM for Large Language Models.__ This
  [NIM's documentation](https://docs.nvidia.com/nim/large-language-models/latest/introduction.html) also includes a
  [Getting Started](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html)
  section with all the steps required to pull and launch the NIM containers. In this
  directory we provide the __`run_Llama3-8b-Instruct.sh`__ script that contains the environment variable definitions
  and the `docker run` command line required to launch the NIM container. There are a
  few things to consider:
  - The __`run_Llama3-8b-Instruct.sh`__ script launches the LLM service as an ___OpenAI like API service___ 
available at `port 8030` by default.
  - In this Starter Pack we use the `Meta-Llama3-8b-instruct` model to generate responses in the RAG pipeline. This model
requires one of the GPUs indicated in the [supported hardware](https://docs.nvidia.com/nim/large-language-models/latest/support-matrix.html#meta-llama-3-8b-instruct)
section.
  -  The script runs the container on the 5th device by default (` --gpus '"device=4"'`).
  - Notice the `Meta-Llama3-8b-instruct` model supports a __maximum context window of 8192 tokens.__


- __Running `Meta-Llama-3-70B-Instruct` on a vLLM container__. A crucial aspect of RAG pipelines development
is the evaluation stage. In this Starter Pack we use __[DeepEval](https://docs.confident-ai.com/docs/getting-started)__
which provides a wealth of features to automate the __[generation of synthetic evaluation sets](https://docs.confident-ai.com/docs/evaluation-datasets-synthetic-data)__
and evaluation processes via an __[extensive collection of evaluation metrics](https://docs.confident-ai.com/docs/metrics-introduction).__ DeepEval
requires a powerful LLM service to generate synthetic evaluation sets and to act as evaluator ("judge") responsible for
gauging every metric used to asses a RAG pipeline. One of the requirements for an LLM to act as a judge is the ability
to generate verdicts in the form of JSON objects. This is not an easy task as very few closed-source LLMs can do it
consistently (GPT-4 or GPT-4o for example). In the open-source LLM world, after testing lots of models, __only 
Llama-3-70b-Instruct__ running on vLLM in ___guided-JSON mode___ was capable of doing the job consistently. Please consider
the following when running the __`run_vllm_llama3-70b-Instruct.sh`__ script:
  - vLLM runs in a container exposing an ___OpenAI-like API service___ on `port 8020`.
  - You'll need a valid [HuggingFace access token](https://huggingface.co/docs/hub/en/security-tokens) and request access to
  [meta-llama/Meta-Llama-3-70B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct) gated model. Once you have
your access token, __please plug it into line 6 of the script.__
  - You will need at least __2 GPUs with 80GB of VRAM each__ to run this model.
  - The container uses the first two GPUs in the system by default (`--gpus '"device=0,1"'`).__
  - Notice the `Meta-Llama3-70b-instruct` model supports __a maximum context window of 8192 tokens.__

 <br>

When running the four containers (3 NIMs + 1 vLLM) simultaneously in the same VM, they look like this:
```
vmuser@h100-vm:~$ docker ps
CONTAINER ID   IMAGE                                                          COMMAND                  CREATED        STATUS        PORTS                                       NAMES
4e3de113d6e1   dockerhub.usw5.packages.broadcom.com/vllm/vllm-openai:latest   "python3 -m vllm.ent…"   15 hours ago   Up 15 hours   0.0.0.0:8020->8000/tcp, :::8020->8000/tcp   vllm_llama3-70b-Instruct
ef35617e3bf0   nvcr.io/nim/meta/llama3-8b-instruct:1.0.3                      "/opt/nvidia/nvidia_…"   33 hours ago   Up 33 hours   0.0.0.0:8030->8000/tcp, :::8030->8000/tcp   Llama3-8B-Instruct
b630d6e1851c   nvcr.io/nim/nvidia/nv-rerankqa-mistral-4b-v3:1.0.0             "/opt/nvidia/nvidia_…"   33 hours ago   Up 33 hours   0.0.0.0:8010->8000/tcp, :::8010->8000/tcp   nv-rerankqa-mistral-4b-v3
bfcd819fd514   nvcr.io/nim/nvidia/nv-embedqa-e5-v5:1.0.0                      "/opt/nvidia/nvidia_…"   33 hours ago   Up 33 hours   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   nv-embedqa-e5-v5
```


_



