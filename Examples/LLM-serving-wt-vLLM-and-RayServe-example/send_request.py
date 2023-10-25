import requests
import json

prompt = """
Human: At a store, shoes cost shoe_cost pair and socks cost sock_cost per pair.
If a customer buys shoe_p pais of shoes and  sock_p pairs of socks, what is the total cost of the purchase?

Write a Python function that returns the answer.

Assistant:
def store_cost(shoe_cost, shoe_p, sock_cost, sock_p):
    return (shoe_cost * shoe_p) + (sock_cost * sock_p)  
>
Human: At the cinema, tickets for adults cost adult_fee and tickets for children cost child_fee
If a family with num_adult adults and num_child children go to the movies, what's the total cost for that family?

Write a Python function that returns the answer.
"""

sample_input = {"prompt": prompt,
                "stream": False,
                "max_tokens": 200,
                "temperature": 0,
                "use_beam_search": True,
                }
# Replace the hostname with Ray head's hostname or IP address
ray_url = "http://172.29.214.18:8000/"
output = requests.post(ray_url, json=sample_input)
for line in output.iter_lines():
    print(json.loads(line.decode("utf-8"))['text'][0])