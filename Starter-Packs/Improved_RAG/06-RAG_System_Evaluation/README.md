# RAG Systems Evaluation

Evaluating RAG systems is essential to the LLM-driven application lifecycle. After trying multiple tools
it looked to us that [__DeepEval__](https://github.com/confident-ai/deepeval) is one the tools that gathers
the most comprehensive set of research-backed
[__evaluation metrics__](https://github.com/confident-ai/deepeval?tab=readme-ov-file#-metrics-and-features). 

In addition, __DeepEval__ showed a __very consistent behaviour between runs__ and its classes return a comprehensive amount of
metadata as a companion to the metrics scores given by its __`eval`__ method.

Finally, unlike other evaluations tools that rely mainly on closed-source LLMs such as GPT-4 or GPT-4o as evaluator
("judge"), DeepEval provides a mechanism to communicate the JSON schema it expects the LLM to follow when
grading the RAG pipeline's response to a test query according to a specific metric. This way, it is possible to use
powerful open-source LLMs such as `Meta-Llama-3-70b-Instruct` to power automatic evaluations of RAG pipelines
according to the [__metrics implemented by DeepEval.__](https://docs.confident-ai.com/docs/metrics-introduction)

### The evaluation metrics used in this notebook are:
- [Answer Relevancy](https://docs.confident-ai.com/docs/metrics-answer-relevancy).
The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating
how relevant the actual output of your LLM application is compared to the provided input. Deepeval's answer
relevancy metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.


- [Faithfulness](https://docs.confident-ai.com/docs/metrics-faithfulness). The faithfulness metric measures the quality of your RAG pipeline's generator by evaluating whether the actual output factually aligns with the contents of your retrieval context.
Deepeval's faithfulness metric is a self-explaining LLM-Eval, which outputs a reason for its metric score. 


- [Contextual Recall](https://docs.confident-ai.com/docs/metrics-contextual-recall). The contextual recall metric
measures the quality of your RAG pipeline's retriever by evaluating the extent to which the retrieval_context
aligns with the expected_output. Deepeval's contextual recall metric is a self-explaining LLM-Eval, which
outputs a reason for its metric score.


- [Contextual Precision](https://docs.confident-ai.com/docs/metrics-contextual-precision). The contextual precision
metric measures your RAG pipeline's retriever by evaluating whether nodes in your retrieval_context 
relevant to the given input are ranked higher than irrelevant ones. Deepeval's contextual precision metric
is a self-explaining LLM-Eval, which outputs a reason for its metric score.


- [Hallucination](https://docs.confident-ai.com/docs/metrics-hallucination). This metric determines whether your LLM generates
factually correct information by comparing the actual output to the provided context.
This is a fundamental metric, as one of the main goals of RAG pipelines is to 
help LLMs generate accurate, up-to-date, and factual responses to user queries.



Things to consider before running the `DeepEval_for_RAG_Llama-3-70b-Instruct.ipynb` Jupyter Notebook:
- Ensure the `07-Starter_Pack_config/improved_rag_config.yaml` configuration file properly points to the right
  hostname/IP addresses in section `Judge (evaluator) LLM service configuration`.
- That same section sets the values for multiple evaluation parameters such as `num_eval_samples`, `decision_threshold`,
etc. Please adjust them as it better suits your needs.
- Every time you run the Jupyter Notebook, the generated evaluation set gets saved in the `./eval_runs` directory.
  If there is a file already there, it gets renamed by appending the current date/time as suffix. 

