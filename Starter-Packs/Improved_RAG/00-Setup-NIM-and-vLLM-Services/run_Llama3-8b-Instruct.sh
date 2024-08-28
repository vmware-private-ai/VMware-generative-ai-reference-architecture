# Choose a container name for bookkeeping
export NGC_API_KEY=<YOUR_KEY>
export CONTAINER_NAME="Llama3-8B-Instruct"

# The container name from the previous ngc registgry image list command
Repository=nim/meta/llama3-8b-instruct
Latest_Tag="1.0.3"

# Choose a LLM NIM Image from NGC
export IMG_NAME="nvcr.io/${Repository}:${Latest_Tag}"

# Choose a path on your system to cache the downloaded models
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"

# Start the LLM NIM on port 8030 and the 5th GPU
docker run -it --rm --name=$CONTAINER_NAME \
  --runtime=nvidia \
  --gpus '"device=4"' \
  --shm-size=16GB \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -u $(id -u) \
  -p 8030:8000 \
  $IMG_NAME