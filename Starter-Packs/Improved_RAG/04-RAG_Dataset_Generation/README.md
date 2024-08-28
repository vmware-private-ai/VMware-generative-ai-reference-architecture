# RAG Evaluation Dataset Generation

This notebook presents the use of the [__DeepEval's Synthesizer__](https://docs.confident-ai.com/docs/evaluation-datasets-synthetic-data)
to generate a question/answer dataset that can be used by
evaluation frameworks such as [__DeepEval__](https://github.com/confident-ai/deepeval) to evaluate the quality of RAG pipelines and determine how changes
in key components of a RAG pipeline such as LLMs, embedding models, re-ranking models, vector stores and retrieval
algorithms affect the quality of the generation process using different
[__evaluation metrics__](https://github.com/confident-ai/deepeval?tab=readme-ov-file#-metrics-and-features).

In our example, we used
[__Meta-Llama-3-70B-Instruct__](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct), one of the most 
capable open-source models available by mid-2024. As this
evaluation set is meant to evaluate a RAG pipeline, it is advised to use the most powerful model you have at hand.

The __Improved RAG Starter Pack comes with a pre-generated Q/A evaluation dataset__
(saved at the `./current` directory), so you __don't need to run this notebook__
to evaluate the improved RAG pipelines. However, we suggest you read through the notebook to understand the
dataset generation process and experiment with different configurations to create evaluation datasets appropriate
for your document corpus and RAG use cases.

Things to consider before running the `Testset_Generation_DeepEval_open-source-LLM.ipynb`
Jupyter Notebook:
- Ensure the `07-Starter_Pack_config/improved_rag_config.yaml` configuration file properly points to the right 
hostname/IP addresses in section `Dataset generation settings` (`Synthesizer LLM Settings (vLLM)` and 
`Synthesizer Embedder Settings (NIM)`)
- That same configuration file has a section labelled as `Dataset generation settings` which sets the values for
multiple evaluation set generation parameters such as `number of evolutions`, `chunk size`, etc. Please adjust them
as it better suits your needs.
- Every time you run the Jupyter Notebook, the generated evaluation set gets saved in the `./current` directory. 
If there is a file already there, it gets renamed by appending the current date/time as suffix and moved to
the `./archive` directory. 
