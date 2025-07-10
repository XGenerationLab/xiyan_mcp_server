## Local Model Configuration
Note: the local model is slow (about 12 seconds per query on my macbook).
If you need a stable and fast service, we still recommend to use the modelscope version.

To run xiyan_mcp_server in local mode, you need
1) a PC/Mac/Machine with at least 16GB RAM
2) 6GB disk space

The above setting is for model of size 3B. You can adjust the settings to run a 32B model on a server.

### Step 1: Install additional Python packages
```bash
pip install flask modelscope torch==2.2.2 accelerate>=0.26.0 numpy=2.2.3
```

### Step 2: (optional) manually download the model
We recommend [xiyansql-qwencoder-3b](https://www.modelscope.cn/models/XGenerationLab/XiYanSQL-QwenCoder-3B-2502/).
You can manually download the model by
```bash
modelscope download --model XGenerationLab/XiYanSQL-QwenCoder-3B-2502
```
It will take you 6GB disk space.

### Step 3: download the script and run server.

Script is located at `src/xiyan_mcp_server/local_model/local_xiyan_server.py`

```bash
python local_xiyan_server.py
```
The server will be running on http://localhost:5090/

### Step 4: prepare config and run xiyan_mcp_server
the config.yml should be like:
```yml
model:
  name: "xiyansql-qwencoder-3b"
  key: "KEY"
  url: "http://127.0.0.1:5090"
```

Till now the local model is ready.

## LLama Cpp configuration

### Model Source:

Download the model from [mradermacher/XiYanSQL-QwenCoder-3B-2504-GGUF](https://huggingface.co/mradermacher/XiYanSQL-QwenCoder-3B-2504-GGUF). In this case, Q8_0 (size 3.4GB) was used.

### Running the server

1. Install required packages
```
#for Mac; Check llama-cpp-python documentation for other CMAKE_ARGS
CMAKE_ARGS="-DGGML_METAL=on" uv pip install llama-cpp-python
uv pip install Flask
```

2. Specify the path of the downloaded model in `MODEL_PATH` variable in `src/xiyan_mcp_server/local_model/llama_cpp_server.py`.

3. Run the script: `uv run  src/xiyan_mcp_server/local_model/llama_cpp_server.py`

### Configuration:

```yml
model:
  name: "xiyan-llama-cpp" #any name will work
  key: ""
  url: "http://127.0.0.1:5090"
```

Now, run the xiyan mcp server and verify with mcp inspector.

For Mac Pro M3, RAM: 24 GB:

```
llama_perf_context_print:        load time =    3652.49 ms
llama_perf_context_print: prompt eval time =    3472.98 ms /  1502 tokens (    2.31 ms per token,   432.48 tokens per second)
llama_perf_context_print:        eval time =    3711.96 ms /    85 runs   (   43.67 ms per token,    22.90 tokens per second)
llama_perf_context_print:       total time =    7202.74 ms /  1587 tokens
```
