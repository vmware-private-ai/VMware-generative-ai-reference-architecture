# Choose a container name for bookkeeping
export NGC_API_KEY=<YOUR_KEY>
export NIM_MODEL_NAME=nvidia/nv-rerankqa-mistral-4b-v3
export CONTAINER_NAME=$(basename $NIM_MODEL_NAME)

# Choose a NIM Image from NGC
export IMG_NAME="nvcr.io/nim/$NIM_MODEL_NAME:1.0.0"

# Choose a path on your system to cache the downloaded models
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"

# Start the NIM Re-ranker service on port 8010 and on the 3rd GPU
docker run -it --rm --name=$CONTAINER_NAME \
  --runtime=nvidia \
  --gpus '"device=2"' \
  --shm-size=16GB \
  -e NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -u $(id -u) \
  -p 8010:8000 \
  $IMG_NAME