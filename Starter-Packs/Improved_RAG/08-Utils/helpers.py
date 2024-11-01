from llama_index.core.schema import TransformComponent
import re
import os
from typing import List
import pandas as pd
from dotmap import DotMap
from datetime import datetime
from collections import namedtuple
from tqdm.notebook import tqdm
import json

from deepeval.models import DeepEvalBaseLLM
from deepeval.models import DeepEvalBaseEmbeddingModel
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import ChatMessage

from deepeval.test_case import LLMTestCase
from deepeval.evaluate import evaluate
from pydantic import BaseModel

class TextCleaner(TransformComponent):
    def __call__(self, nodes, **kwargs):
        for node in nodes:
            node.text = re.sub(r"\xad\n", "", node.text)
            node.text = re.sub(r"\n", " ", node.text)
            node.text = re.sub(r"\xa0", " ", node.text)
        return nodes


def get_indices_with_nulls(elements):
    """
    Scans the .text attribute across a list of Documents | Nodes to
    identify the presence of the 'x\00' character which is not supported
    by the 01-PGVector store.
    :param elements: A list of LlamaIndex Documents or Nodes
    :return: A list of indices of Documents | Nodes containing 'x\00'
    """
    bad_elements = []
    for idx, elem in enumerate(elements):
        if elem.text.find('\x00') != -1:
            bad_elements.append(idx)
    return bad_elements


def get_short_docs(documents, min_length):
    """
    From a list of LlamaIndex Documents, return the indices of those
    documents containing a number of words < min_length
    :param documents: A list of LlamaIndex Document objects
    :param min_length: The minimum length a document must have
    :return: The indices of documents whose length < min_length
    """
    short_docs = []
    for idx, doc in enumerate(documents):
        doc_length = len(doc.text.split())
        if doc_length < min_length:
            short_docs.append(idx)
    return short_docs


def remove_elements(elements, to_remove):
    """
    Removes the entries from 'elements' indexed by 'to_remove'
    :param elements: A list of Documents | Nodes
    :param to_remove: The indices to remove from the list
    :return: A subset of 'elements'
    """
    return [i for j, i in enumerate(elements)
            if j not in to_remove]


def remove_recs_without_query(records_list):
    """
    Removes records not containing a real query (question) in
    the `query` field.
    :param records_list: A list containing dictionary-type records.
    :return: The list of records containing the '?' character at the value
            pointed by the 'query' key.
    """
    bad_elements = []
    for idx, elem in enumerate(records_list):
        if elem['query'].find('?') == -1:
            bad_elements.append(idx)
    return [i for j, i in enumerate(records_list)
            if j not in bad_elements]


def remove_duplicated_queries(records_list):
    """
    Removes duplicated queries from the list
    :param records_list: A list containing dictionary-type records
    :return: The list of records without duplicated queries
    """
    seen = set()
    non_dups = []

    for elem in records_list:
        key = (elem['query'],)
        if key in seen:
            continue
        non_dups.append(elem)
        seen.add(key)

    return non_dups


def generate_responses_dict(query_engine, test_set_df):
    """
    Returns a dictionary containing the responses generated by 'query_engine'
    to the queries provided by the test_set_df dataframe. The dictionary also
    includes the expected response (ground truth) and the context text corresponding
    to the nodes retrieved by the query engine to generate each response.
    :param query_engine: A LlamaIndex query engine
    :param test_set_df: A Pandas dataframe with a test set
    :return: A dictionary containing the responses and the context required by
             evaluation frameworks like DeepEval
    """
    responses = [query_engine.query(q)
                 for q in tqdm(test_set_df['query'].to_list())]
    answers = []
    contexts = []

    for r in responses:
        answers.append(r.response.strip())
        contexts.append([c.node.get_content() for c in r.source_nodes])

    responses_dict = {
            "query": test_set_df['query'].to_list(),
            "answer": answers,
            "contexts": contexts,
            "ground_truth": test_set_df['reference_answer'].to_list()
    }
    return responses_dict


def goldens_to_pandas(goldens, include_context=False):
    test_set = {
            'query': [],
            'reference_answer': []
    }

    if include_context:
        test_set['reference_contexts']: []

    for golden in goldens:
        test_set['query'].append(golden.input)
        test_set['reference_answer'].append(golden.expected_output)
        if include_context:
            test_set['reference_contexts'].append(golden.context)

    return pd.DataFrame(test_set)


class CustomSynthesizerModel(DeepEvalBaseLLM):
    def __init__(self, llm_cfg):
        self.model = OpenAILike(
                model=llm_cfg.model,
                api_key=llm_cfg.api_key,
                api_base=llm_cfg.api_base,
                temperature=llm_cfg.temperature,
                max_tokens=llm_cfg.max_tokens,
                repetition_penalty=llm_cfg.repetition_penalty,
                #chat_template=llm_cfg.chat_template,
                is_chat_model=True,
        )
        self.model_name = llm_cfg.model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        messages = [
                ChatMessage(
                        role="system",
                        content="You are an accurate assistant that is not chatty, and always provides accurate and very succinct completions."
                                "Don't generate greetings or other type of unnecessary text."
                ),
                ChatMessage(role="user", content=prompt),
        ]
        output = chat_model.chat(
                messages=messages,
        ).message.content

        return output

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name


class CustomEmbeddingModel(DeepEvalBaseEmbeddingModel):
    def __init__(self, embedding_cfg):
        self.model_name = embedding_cfg.model
        self.embedder = NVIDIAEmbedding(
                base_url=embedding_cfg.api_base,
                model=embedding_cfg.model,
                embed_batch_size=embedding_cfg.batch_size,
                truncate="END",
        )

    def load_model(self):
        return self.embedder

    def embed_text(self, text: str) -> List[float]:
        embedding_model = self.load_model()
        return embedding_model.get_text_embedding(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embedding_model = self.load_model()
        return embedding_model.get_text_embedding_batch(texts, show_progress=True)

    async def a_embed_text(self, text: str) -> List[float]:
        embedding_model = self.load_model()
        return await embedding_model.aget_text_embedding(text)

    async def a_embed_texts(self, texts: List[str]) -> List[List[float]]:
        embedding_model = self.load_model()
        return await embedding_model.aget_text_embedding_batch(texts, show_progress=True)

    def get_model_name(self):
        return self.model_name

def save_results(
        responses_df: pd.DataFrame,
        rag_type: str,
        llm_model: str,
        emb_model: str,
        rank_model: str
) -> None:

    # Save current responses file
    file_list = os.listdir("responses/current")
    current_file = file_list[0] if len(file_list) > 0 else None
    if current_file is not None:
        os.rename(
                src=f"responses/current/{current_file}",
                dst=f"responses/archive/{current_file}",
        )

    # Serialize the inference results dataframe
    file_name = (f"responses/current/{rag_type}__{llm_model.split('/')[1]}"
                 f"__{emb_model.split('/')[1]}"
                 f"__{rank_model.split('/')[1]}.csv")

    responses_df.to_csv(
            path_or_buf=file_name,
            index=False,
    )
    print(f"{rag_type} pipeline responses successfully saved to file: {file_name}.")


def save_testset(
        test_set_df: pd.DataFrame,
        config: DotMap,
) -> None:

    # Save a copy of the current test set file
    file_list = os.listdir(config.deep_eval.current_files_dir)
    current_file = file_list[0] if len(file_list) > 0 else None
    if current_file is not None:
        file_suffix = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        os.rename(
                src=f"{config.deep_eval.current_files_dir}/{current_file}",
                dst=f"{config.deep_eval.archive_files_dir}/{current_file}_{file_suffix}",
        )

    # Save newly generated test set in the "current" directory
    file_name = (f"{config.deep_eval.current_files_dir}/NASA_history_QA__"
                 f"{config.deep_eval.synth_llm_cfg.model.split('/')[-1]}__generated.csv")
    test_set_df.sample(frac=1).to_csv(
            path_or_buf=file_name,
            index=False,
    )
    print(f"Evaluation set saved at location: {file_name}. ")

class CustomEvaluationModel(DeepEvalBaseLLM):
    def __init__(self, llm_cfg):
        self.model = OpenAILike(
                model=llm_cfg.model,
                api_key=llm_cfg.api_key,
                api_base=llm_cfg.api_base,
                temperature=llm_cfg.temperature,
                max_tokens=llm_cfg.max_tokens,
                repetition_penalty=llm_cfg.repetition_penalty,
                #chat_template=llm_cfg.chat_template,
                is_chat_model=True,
        )
        self.model_name = llm_cfg.model

    def load_model(self):
        return self.model

    def generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        chat_model = self.load_model()
        messages = [
                ChatMessage(
                        role="system",
                        content="You are an accurate assistant that is not chatty, and always provides accurate and very succinct responses."
                                "When asked to provide reasons or verdicts, you MUST use the very minimum amount of words and avoid full citations."
                ),
                ChatMessage(role="user", content=prompt),
        ]
        schema_str = json.dumps(schema.model_json_schema())
        output = chat_model.chat(
                messages=messages,
                extra_body=dict(guided_json=schema_str),
                #extra_body={"nvext":dict(guided_json=json.loads(schema_str))},
        ).message.content
        try:
            json_result = json.loads(output)
        except ValueError as error:
            print(error)
            print(f'Failed json:\n{output}\n')
        return schema(**json_result)

    async def a_generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_name


def run_evaluations(qa_set_df, metrics):
    """
    Run the measurement of contextual_precision, contextual_recall,
    answer_relevancy, and faithfulness metrics implemented by
    DeepEval.
    :param qa_set_df: A dataframe containing the Q/A pairs,
    ground truth and context required by DeepEval to run a
    test case.
    :param metrics: A list of metrics to execute on each test case.
    :return: The results from deepeval.evaluate.
    """

    test_cases =[]
    for _, row in qa_set_df.iterrows():
        test_case = LLMTestCase(
                input=row['query'],
                actual_output=row['answer'],
                expected_output=row['ground_truth'],
                retrieval_context=eval(row['contexts']),
                context=eval(row['contexts']),
        )
        test_cases.append(test_case)

    return evaluate(
            test_cases=test_cases,
            metrics=metrics,
            show_indicator=False,
            print_results=False,
            ignore_errors=True,
            run_async=False,
    )

def deepeval_on_test_sets(test_sets, metrics, nrows=5):
    """
    Runs DeepEval on each element of test_sets and returns a named tuple containing
    the name of the RAG pipeline and a Pandas dataframe containing the scores
    from each DeepEval metric.
    :param test_sets: The list of test sets containing the Q/A pairs, ground truth and
    context of a RAG pipeline.
    :param metrics: A list of metrics to execute on each test case.
    :param nrows: Number of rows of the test set to be used by DeepEval to evaluate a
    RAG pipeline.
    :return: A list named tuples containing the DeepEval scores for each test set.
    """

    # Try opening all test sets, if one does not exist, rise an exception
    for file in test_sets:
        f = open(file)
        f.close()

    ModelEval = namedtuple("ModelEval",
                           "modelmix results")
    model_evals = []

    for tset in tqdm(test_sets):
        model_mix = tset.split('/')[-1].split('.')[0]
        print(f"Evaluating {model_mix}")
        qa_set_df = pd.read_csv(
                filepath_or_buffer=tset,
                nrows=nrows,
        )
        results = run_evaluations(
                qa_set_df,
                metrics,
        )

        model_evals.append(
                ModelEval(
                        model_mix,
                        results
                )
        )

    return model_evals

def deepeval_to_dict(evals):
    """
    Converts a list of DeepEval results into a dictionary that can be used to
    create Pandas dataframes.
    :param evals: A list with DeepEval results from 'eval'
    :return: A dictionary with the dataset name as key and the DeepEval results as value
    """
    res_summary = {}
    for dset in evals:
        res_summary[dset.modelmix] = {}
        for results in dset.results:
            for field in results.metrics_data:
                mkey = f"{field.name} Score"
                if mkey in res_summary[dset.modelmix].keys():
                    res_summary[dset.modelmix][mkey].append(field.score)
                    res_summary[dset.modelmix] \
                        [f"{field.name} Reason"].append(field.reason)
                    res_summary[dset.modelmix] \
                        [f"{field.name} Error"].append(field.error)
                else:
                    res_summary[dset.modelmix][mkey] = [field.score]
                    res_summary[dset.modelmix][f"{field.name} Reason"] = [field.reason]
                    res_summary[dset.modelmix][f"{field.name} Error"] = [field.error]

    return res_summary