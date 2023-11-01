# Introduction

This folder contains three examples Jupyter notebooks that gradually introduce the elements required to build a **Retrieval-Augmented 
Generation (RAG)** system, starting from creating a conversation application that evolves into a complete RAG generation chain.

We use the following open-source technologies to implement the examples:
- [LLama 2 13b Chat](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf). Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. This is the repository for the 13B fine-tuned model, optimized for dialogue use cases and converted for the Hugging Face Transformers format.
- [vLLM](https://vllm.readthedocs.io/en/latest/) is a fast and easy-to-use library for LLM inference and serving. vLLM is a quick and user-friendly library designed for LLM inference and deployment. In this instance, we utilize the VLLMOpenAI class from LangChain to interact with the vLLM service that is compatible with OpenAI's API.
- [Gradio](https://www.gradio.app/) provides a swift means to showcase machine learning models through an accessible web interface.
- [Langchain](https://python.langchain.com/) is a framework for the fast prototyping of applications powered by language models. Langchain links and coordinates actions between LLMs, data retrievers, and memory systems to expand the knowledge domain of LLMs beyond the datasets used to pre-train and fine-tune them.

# Folder structure
### Under the `chatbot` directory:

**e1) Implementing a chatbot with Llama-2-13b-chat served by vLLM, through the Gradio UI**

The `e1-Llama2-chatbot-on-vLLM-with-Gradio.ipynb` notebook implements a chatbot using LLama 2 Chat (13B) LLM served by vLLM. The Gradio UI handles the user interactions with the chatbot from a web browser. In this notebook, we discuss how to format prompts for Llama 2 properly. We also discuss leveraging Gradio's memory mechanisms to keep track of a conversation between the LLM (chatbot) and the user. Finally, we put together the Gradio elements required to implement a web UI that users can use to control the LLM generation parameters and submit prompts for completion.

**e2) Implementing a chatbot using Llama-2-13b-chat, vLLM, LangChain, and the Gradio UI**

The `e2-Llama2-chatbot-vLLM-Langchain-Gradio.ipynb` notebook introduces the fundamental LangChain constructs required to implement a conversation chain (LLMChain) with memory (via the ConversationBufferMemory class) and the different prompt template types that get combined to prompt LLama 2 in proper and diverse ways.

### Under the `chatbot-with-RAG` directory:

**e3) Implementing a chatbot with Retrieval-Augmented Generation (RAG) using Llama-2-13b-chat, vLLM, LangChain, and the Gradio UI**

The `e3-RAG-Llama2-chatbot-vLLM-Langchain-Gradio.ipynb` introduces the components required to build a RAG system; these are:

- `Document loaders`. In this case, we load three PDF documents containing NY Times articles about the Otis hurricane, which battered the Pacific coast of Mexico in late Oct 2023. This data is several months more recent than the datasets used to pre-train Llama 2 (released in July 2023). We use this info to expand the LLM's knowledge to answer questions on fresh data.
- `Embeddings encoders`. These encode the loaded documents into numeric vectors for semantic similarity search purposes.
- `Splitters` divide documents into multiple chunks that get loaded into a vector database.
- `Retrievers` are vector databases containing the embeddings resulting from the document encoding process. When a user enters a query, the retriever will pull all the document chunks that are semantically related to the question.
- The `LLM service` will use the context provided by the retriever to answer users' questions.
- The `RetrievalQA` chain is a `LangChain` class that brings all the previous components together into a single entity (object) capable of accepting users' queries and feeding the LLM with the data required to generate the answer.