from tqdm.notebook import tqdm


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
