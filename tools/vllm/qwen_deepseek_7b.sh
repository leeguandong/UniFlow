export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

python3 -m vllm.entrypoints.api_server \
  --model /dev_share/models/DeepSeek-R1-Distill-Qwen-7B \
  --served-model-name DeepSeek-R1-Distill-Qwen-7B \
  --port 8000 \
  --gpu-memory-utilization 0.8 \
  --max-model-len 2048 \
  --max-num-batched-tokens 2048 \
  --dtype float16 \
  --tensor-parallel-size 1 \
  --trust-remote-code