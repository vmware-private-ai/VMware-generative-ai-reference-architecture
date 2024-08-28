# Improved RAG Starter Pack

The **Improved RAG Starter Pack** offers a comprehensive suite of Python scripts designed for enthusiasts and 
professionals in machine learning, specifically focusing on Retrieval-Augmented Generation (RAG) pipelines.
This repository provides step-by-step guidance on how to build a RAG system, starting from the document ingestion,
vector (text embeddings) index population, and standard RAG pipeline implementation, all the way to improvements over
the standard RAG retrieval processes. 

The technologies we used to implement this Starter Pack include the following:

- [The latest NVIDIA NIM microservices](https://docs.nvidia.com/nim/index.html) that provide production-grade runtimes for 
different types of ML models (embeddings, reranking, text generation, etc) that include on-going security updates.
- [PGVector extension on PostgreSQL (v12)](https://docs.vmware.com/en/VMware-Postgres/15.7/vmware-postgres/installing.html) which 
provides a robust and scalable vector database engine required to augment large language models (LLM) generation
capabilities. 
- [LlamaIndex (v0.11.x),](https://github.com/run-llama/llama_index) an orchestration and data processing framework
that facilitates the constructions of LLM-driven applications.
- [vLLM (v.0.5),](https://github.com/vllm-project/vllm) a powerful, fast and easy-to-use LLM inference server.
- [DeepEval (v1.1.x),](https://docs.confident-ai.com/docs/getting-started) an open-source evaluation framework for LLMs and 
LLM-driven applications such as RAG pipelines.
- [Meta Llama-3 models.](https://ai.meta.com/blog/meta-llama-3/) State-of-the-art open source LLMs. 

### Covered Topics:

The Improved RAG Starter Pack will guide you through the phases required to build robust RAG pipelines that allow
your LLM-driven applications improve the accuracy and relevancy of its outputs. We also dedicate a good deal of 
attention to the evaluation process of RAG pipelines via the use of metrics such as 
Answer Relevancy, Contextual Precision, and more.

### Repository Structure

- __NVIDIA NIMs and vLLM services setup (directory 00)__: Provide the steps necesary to launch the NVIDIA NIM and vLLM services 
required to power the different RAG architectures we implement in this repository,


- __Document Ingestion into PGVector DB (directories 01, 02 and 03)__: Exemplify how to ingest a collection of
documents that constitute a knowledge base (e-books on NASA's history in this case) into a vector (PGVector) database. 
Vector databases enrich LLMs' completions by providing a grounded foundation for LLMs to generate accurate and factual
answers to users' queries related to specific knowledge domains.


- __Evaluation Dataset Generation (directory 04)__: Provides instructions for automatically generating an evaluation
dataset tailored for assessing RAG pipelines. This component is crucial for developers looking to assess
and calibrate their RAG implementations against standardized metrics listed further down this document. 


- **The implementation of three different RAG architectures (directory 05)**:   
  - **Standard RAG Pipeline + re-ranker**: Implements a standard RAG pipeline using LlamaIndex, incorporating a
  final re-ranking step. The re-ranker enhances the accuracy of the document retrieval process to provide LLMs with
  a factual and relevant context to generate quality responses.

  - **Sentence Windows Parsing**: Improves the standard RAG pipeline by introducing LlamaIndex's implementation of 
  Sentence Windows Parsing. This method optimizes the parsing of retrieved documents, ensuring a more effective and 
  contextually relevant selection of text for LLMs.

  - **Auto Merging Retrieval**: Further refines the RAG pipeline through LlamaIndex's Auto Merging Retrieval feature. 
  This technique automatically merges relevant retrieved information, streamlining the input to LLMs and fostering 
  more coherent and accurate responses.


- **RAG Pipeline Evaluation (directory 06)**: Implements an automated evaluation method for RAG pipelines using 
[__DeepEval evaluations__](https://docs.confident-ai.com/docs/metrics-introduction) and a pre-generated evaluation 
dataset (directory 04). This approach allows for a detailed assessment of a pipeline's performance, offering insights 
into its efficiency based on the __Contextual Precision, Faithfulness, Contextual Recall, Hallucinations and 
Answer Relevancy__ metrics.


- __Starter Pack configuration (directory 07)__: Stores the `improved_rag_config.yaml` configuration file that is used by
the Jupyter Notebooks and Python scripts in the Starter Pack to retrieve their configuration. It also stores the 
`impv_rag.yaml` file that can be used by 
[__Conda__](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to install all the Python 
packages required to run the Jupyter Notebooks included in this Starter Pack.


- __Utils (directory 08)__: Stores the `helpers.py` script containing the definition of multiple classes and helper
functions utilized by the Jupyter Notebooks that constitute this Starter Pack.

### Starter Pack Directory Structure
To run all the examples in the Starter Pack, **please execute the tasks following the numeric order of the directory
structure**. Each directory contains a README.md file with instructions on how to use its content.
```
Improved RAG Starter Pack Directory Structure:

┌── 00-Setup-NIM-and-vLLM-Services (START HERE)
├── 01-PGVector  
├── 02-KB-Documents   
├── 03-Document_ingestion  
├── 04-RAG_Dataset_Generation  
├── 05-RAG_Variants  
│   ├── 01-Standard_RAG_with_Reranking  
│   ├── 02-Sentence_Window_Retrieval  
│   └── 03-Auto_Merging_Retrieval  
├── 06-RAG_System_Evaluation
├── 07-Starter_Pack_config
└── 08-Utils
```
