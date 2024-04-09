# VMware-generative-ai-reference-architecture

## Overview

This repository contains a series of Python scripts and configuration files that serve as a complement to the
white paper [Deploying Enterprise-Ready Generative AI on VMware Cloud Foundation](https://core.vmware.com/resource/deploying-enterprise-ready-generative-ai-vmware-cloud-foundation)

## Disclaimer
The scripts provided in this repository are intended to be used for educational purposes but not for production applications. Be aware that LLMs pose inherent vulnerabilities and risks, as illustrated by the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/). We strongly encourage customers to pay attention to OWASP guidance and the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) to build safe and robust AI systems.

## Directory Structure<br>
The repository is organized by the following structure:<br>
- The [vSphere-and-TKG-config-files](https://github.com/vmware-ai-labs/VMware-generative-ai-reference-architecture/tree/main/vSphere-and-TKG-config-files) directory provides configuration files to set the Tanzu Kubernetes Cluster, NVIDIA GPUs, and Network Kubernetes Operators
  that provide hardware acceleration services to VMware Tanzu Kubernetes clusters.
- The [Examples/LLM-fine-tuning-example](https://github.com/vmware-ai-labs/VMware-generative-ai-reference-architecture/tree/main/Examples/LLM-fine-tuning-example) 
directory provides __the steps to configure a Python virtual environment suitable for LLM fine-tuning tasks__ based on a series of 
[Hugging Face](https://huggingface.co/) libraries. It also includes a Python notebook that illustrates all the steps required to fine-tune
the [Falcon LLMs](https://falconllm.tii.ae/) on a custom dataset to teach the model to follow instructions.
- The [Examples/LLM-serving-wt-vLLM-and-RayServe-example](https://github.com/vmware-ai-labs/VMware-generative-ai-reference-architecture/tree/main/Examples/LLM-serving-wt-vLLM-and-RayServe-example) directory provides the configuration steps, the configuration files, and the Python
scripts to set a Ray cluster that serves the Falcon LLMs via [vLLM](https://github.com/vllm-project/vllm) running as a 
[Ray Serve](https://docs.ray.io/en/latest/serve/index.html) application. The Ray cluster gets deployed on Tanzu Kubernetes using
[Kuberay](https://github.com/ray-project/kuberay).
- We also include __Starter Packs__ which provide code examples about the implementation of the following use cases:
  - __Intro to RAG (retrieval augmented generation with LangChain and Gradio)__
  - __AI coding assistance via StarCoder (Code_Assistant)__
  - __Improved RAG (via LlamaIndex + PGVector + DeepEval)__
  


## Contributing

The VMware-generative-ai-reference-architecture project team welcomes contributions from the community. Before you start working with VMware-generative-ai-reference-architecture, please
read our [Contributor License Agreement](https://cla.vmware.com/cla/1/preview). All contributions to this repository must be
signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on
as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md](CONTRIBUTING_CLA.md).

## License
The project is [licensed](https://github.com/vmware-ai-labs/VMware-generative-ai-reference-architecture/blob/main/LICENSE) under the terms of the Apache 2.0 license.
