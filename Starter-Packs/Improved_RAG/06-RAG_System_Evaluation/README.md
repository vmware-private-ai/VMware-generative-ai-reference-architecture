# RAG Systems Evaluation

Evaluating RAG systems is essential to the LLMOps and LLM-powered app lifecycle. After trying multiple tools
it looked to us that [__DeepEval__](https://github.com/confident-ai/deepeval) is one the tools that gathers
the most comprehensive set of research-backed
[__evaluation metrics__](https://github.com/confident-ai/deepeval?tab=readme-ov-file#-metrics-and-features). 

In addition, __DeepEval__ showed a __very consistent behaviour between runs__ and its classes return a comprehensive amount of
metadata as a companion to the metrics scores given by the __`eval`__ method.

It is important to highlight that for DeepEval evaluation tasks, you need to use the __largest proprietary LLMs, such
as GPT3.5__ that produce __consistent evaluation (judging) results in proper JSON format__, just like DeepEval (and other
tools) require. 

### The evaluation metrics used in this notebook are:
- [Answer Relevancy](https://docs.confident-ai.com/docs/metrics-answer-relevancy).
The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating
how relevant the actual output of your LLM application is compared to the provided input. Deepeval's answer
relevancy metric is a self-explaining LLM-Eval, meaning it outputs a reason for its metric score.


- [Faithfulness] (https://docs.confident-ai.com/docs/metrics-faithfulness). The faithfulness metric measures the quality of your RAG pipeline's generator by evaluating whether the actual output factually aligns with the contents of your retrieval context.
Deepeval's faithfulness metric is a self-explaining LLM-Eval, which outputs a reason for its metric score. 


- [Contextual Recall](https://docs.confident-ai.com/docs/metrics-contextual-recall). The contextual recall metric
measures the quality of your RAG pipeline's retriever by evaluating the extent to which the retrieval_context
aligns with the expected_output. Deepeval's contextual recall metric is a self-explaining LLM-Eval, which
outputs a reason for its metric score.


- [Contextual Precision](https://docs.confident-ai.com/docs/metrics-contextual-precision). The contextual precision
metric measures your RAG pipeline's retriever by evaluating whether nodes in your retrieval_context 
relevant to the given input are ranked higher than irrelevant ones. Deepeval's contextual precision metric
is a self-explaining LLM-Eval, which outputs a reason for its metric score.



