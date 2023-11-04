# Command:
sudo docker run --gpus 0 -v /home/octo/hf_text_gen:/data -e HUGGING_FACE_HUB_TOKEN=YOUR_HF_TOKEN --network host ghcr.io/huggingface/text-generation-inference:0.8 --model-id bigcode/starcoder --max-concurrent-requests 400 --max-input-length 4000 --max-total-tokens 4512 -p 8080
 
# Explain
-gpus                                               Designate the GPU ID to use
-v /home/octo/hf_text_gen:/data                     Mount a persistant location for Text Gen output
-e HUGGING_FACE_HUB_TOKEN=YOUR_HF_TOKEN             Replace with your own HF Token
--network host                                      Container uses the host network mode: https://spacelift.io/blog/docker-networking
ghcr.io/huggingface/text-generation-inference:0.8   HF TGI image
--model-id bigcode/starcoder                        model id, we can replace it with the local cache (e.g., /home/octo/hf_text_gen/models--bigcode--starcoder/snapshots/xxxxxxxxx) after the initial download
--max-concurrent-requests 400
--max-input-length 4000                             maximum input token length the server can handle 
--max-total-tokens 4512                             the total tokens the model will generate
-p 8080                                             the port the server will listen to.

# Then you will see the following output
2023-11-03T15:22:41.113441Z  INFO text_generation_launcher: Successfully downloaded weights.
2023-11-03T15:22:41.113670Z  INFO text_generation_launcher: Starting shard 0
2023-11-03T15:22:51.124885Z  INFO text_generation_launcher: Waiting for shard 0 to be ready...
...
2023-11-03T15:24:00.771957Z  INFO shard-manager: text_generation_launcher: Server started at unix:///tmp/text-generation-server-0
 rank=0
2023-11-03T15:24:00.803275Z  INFO text_generation_launcher: Shard 0 ready in 79.689004555s
2023-11-03T15:24:00.878569Z  INFO text_generation_launcher: Starting Webserver
2023-11-03T15:24:00.946252Z  WARN text_generation_router: router/src/main.rs:158: no pipeline tag found for model /data/models--bigcode--starcoder/snapshots/<some hash>/
2023-11-03T15:24:00.949517Z  INFO text_generation_router: router/src/main.rs:178: Connected

# Verify the service on your laptop using http requests of `def hello()`

$ curl --location 'http://172.29.214.125:8080/generate' --header 'Content-Type: application/json' --data '{"inputs":"\n  def hello()","parameters":{"max_new_tokens":256}}'
 
# You would get the following similar response
{"generated_text":" -> str:\n    return 'Hello, world!'\n\n  @app.route('/hello/<name>')\n  def hello_name(name: str) -> str:\n    return f'Hello, {name}!'\n\n  @app.route('/hello/<name>/<int:age>')\n  def hello_name_age(name: str, age: int) -> str:\n    return f'Hello, {name}! You are {age} years old.'\n\n  @app.route('/hello/<name>/<int:age>/<float:height>')\n  def hello_name_age_height(name: str, age: int, height: float) -> str:\n    return f'Hello, {name}! You are {age} years old and {height} meters tall.'\n\n  @app.route('/hello/<name>/<int:age>/<float:height>/<float:weight>')\n  def hello_name_age_height_weight(name: str, age: int, height: float, weight: float) -> str:\n    return f'Hello, {name}! You are {age} years old and {height} meters tall and weigh {weight} kilograms.'\n\n  @app.route('/hello/<name"}