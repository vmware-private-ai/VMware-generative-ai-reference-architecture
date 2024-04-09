# Improved RAG Approaches

As mentioned in the Improved Stater Pack's top README.md file, we explore three RAG pipeline
implementation variants powered by __[LlamaIndex](https://docs.llamaindex.ai/en/stable/).__  

- **Standard RAG Pipeline + re-ranker**: Implements a standard RAG pipeline using LlamaIndex, incorporating a
final re-ranking step. Different from embedding model, a re-ranker uses question and document as input and directly
output similarity instead of embedding. You can get a relevance score by inputting query and passage to the reranker. 
The reranker is optimized based cross-entropy loss, so the relevance score is not bounded to a specific range. All the
RAG pipelines implemented in this notebook use 
__[BAAI/bge-reranker-base](https://github.com/FlagOpen/FlagEmbedding/tree/master/FlagEmbedding/reranker)__


- **Sentence Windows (node) Parsing**: Improves the standard RAG pipeline by introducing LlamaIndex's implementation of
__[Sentence Windows Node Parsing](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_window/)__. A 
sentence window node parser splits a document into Nodes, with each node being a sentence. Each node contains a
window from the surrounding sentences in the metadata.


- **Auto Merging Retrieval**: In this improved RAG variant, the 
__[AutoMergingRetriever](https://docs.llamaindex.ai/en/stable/api_reference/retrievers/auto_merging/?h=autome#llama_index.core.retrievers.AutoMergingRetriever)__
will try to merge context into parent context. The retriever first retrieves chunks from a document store. Then, it will try to merge the chunks into a single context.
