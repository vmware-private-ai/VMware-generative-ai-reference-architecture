# VMware-generative-ai-reference-architecture

## Overview

This repository contains a series of configuration files and Python scripts that serve as a complement to the
white paper<br>[Deploying Enterprise-Ready Generative AI on VMware Cloud Foundation]( https://core.vmware.com/resource/deploying-enterprise-ready-generative-ai-vmware-cloud-foundation) .

This repository intends to provide readers with examples so they can more easily reproduce the VMware infrastructure configuration. The repository also includes a series of Python scripts and notebooks that provide working examples about the Large Language Model (LLM) fine-tuning and inference tasks.

## Directory Structure<br>
The repository is organized by the following structure:<br>
- The `vSphere-and-TKG-config-files` directory provides configuration files to setup the Tanzu Kubernetes Cluster, NVIDIA GPUs and Network Kubernetes Operators
  that provide hardware acceleration services to VMware Tanzu Kubernetes clusters.
- The `LLM-fine-tuning-example` provides the steps to configure a Python virtual environment suitable for LLM fine-tuning tasks based on a series of 
[Hugging Face](https://huggingface.co/) libraries. It also includes a Python notebook that illustrates all the steps required to fine-tune
the [Falcon LLMs](https://falconllm.tii.ae/) on a custom dataset to teach the model to follow instructions.
- The `LLM-serving-wt-vLLM-and-RayServe-example`directory provides the configuration steps, the configuration files, and the Python
scripts to setup a Ray cluster that serves the Falcon LLMs via [vLLM](https://github.com/vllm-project/vllm) running as a 
[Ray Serve](https://docs.ray.io/en/latest/serve/index.html) application. The Ray cluster gets deployed on Tanzu Kubernetes using
[Kuberay](https://github.com/ray-project/kuberay).

## Contributing

The VMware-generative-ai-reference-architecture project team welcomes contributions from the community. Before you start working with VMware-generative-ai-reference-architecture, please
read our [Developer Certificate of Origin](https://cla.vmware.com/dco). All contributions to this repository must be
signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on
as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License
