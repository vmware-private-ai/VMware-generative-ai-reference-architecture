# RAG Evaluation Dataset Generation

This notebook presents the use of LlamaIndex's
[__RAGDatasetGenerator__](https://docs.llamaindex.ai/en/stable/examples/llama_dataset/labelled-rag-datasets/?h=ragdatasetgenerator) to generate a question/answer dataset that can be used by
evaluation frameworks such as [__DeepEval__](https://github.com/confident-ai/deepeval) to evaluate the quality of RAG pipelines and determine how changes
in kay components of a RAG pipeline such as LLMs, embedding models, re-ranking models, vector stores and retrieval
algorithms affect the quality of the generation process using different
[__evaluation metrics__](https://github.com/confident-ai/deepeval?tab=readme-ov-file#-metrics-and-features).

In our example, we used
[__mistralai/Mixtral-8x7B-Instruct-v0.1__](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1), one of the most 
capable [open-source](https://huggingface.co/models?license=license%3Aapache-2.0) models available by Q2-2024. As this
test set is meant to evaluate a RAG pipeline, it is adviced to use the most powerful model you have at hand.

The __Improved RAG Starter Pack comes with a pre-generated Q/A evaluation dataset__, so you __don't need to run this notebook__
to evaluate the improved RAG pipelines. However, we suggest you to go through the notebook to understand the
dataset generation process and experiment with different configurations to create evaluation datasets appropriate
for your document corpus and RAG use cases.
