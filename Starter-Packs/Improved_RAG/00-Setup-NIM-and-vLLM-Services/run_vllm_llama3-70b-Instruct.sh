# Serve the Llama3-70b-instruct model on port 8020
# and on the first two GPUs in OpenAI-like mode.

docker run --runtime nvidia --rm --gpus '"device=0,1"' \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=<YOUR_HF_ACCESS_TOKEN>" \
    -p 8020:8000 \
    --ipc=host \
    --name="vllm_llama3-70b-Instruct" \
    vllm/vllm-openai:v0.5.5 \
    --model meta-llama/Meta-Llama-3-70B-Instruct \
    --enforce-eager \
    --tensor-parallel-size 2