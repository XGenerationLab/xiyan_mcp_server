[![smithery badge](https://smithery.ai/badge/@XGenerationLab/xiyan_mcp_server)](https://smithery.ai/server/@XGenerationLab/xiyan_mcp_server)

# XiYan MCP Server

A Model Context Protocol (MCP) server that enables natural language queries to MySQL databases, power by XiYanSQL(https://github.com/XGenerationLab/XiYan-SQL) as text-to-sql technique.


## Features
- Fetch data by natural language throught XiYanSQL (https://github.com/XGenerationLab/XiYan-SQL)
- List available MySQL tables as resources
- Read table contents

## Installation

Python 3.11+ is required. 
you can install the server by a pre-release verion

```bash
pip install xiyan_mcp_server-0.1.0-py3-none-any.whl
```

After that you can directly run the server by:
```bash
python -m xiyan_mcp_server
```
But it does not provide any functions until you complete following config.
You will get a yml file. After that you can run the server by:
```yaml
env YML=path/to/yml python -m xiyan_mcp_server
```


## Configuration

You need a yml config file to configure the server.
a default config file is provided in config_demo.yml which looks like this:

```yaml
model:
  name: "pre-xiyan_multi_dialect_v3"
  key: ""
  url: "https://poc-dashscope.aliyuncs.com/compatible-mode/v1"

database:
  host: "localhost"
  port: 3306
  user: "root"
  password: ""
  database: ""
```

### About LLM
Name is the name of the model to use, key is the API key of the model, url is the API url of the model. 
#### Using general LLMs
if you want to use the general LLMs, e.g. gpt3.5, you can directly config like this:
```yaml
model:
  name: "gpt-3.5-turbo"
  key: "YOUR KEY "
  url: "https://api.openai.com/v1/chat/completions"
database:
```

if you want to use Qwen from alibaba, e.g. Qwen-max,
```yaml
model:
  name: "qwen-max"
  key: "YOUR KEY "
  url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
database:
```
#### Using Text-to-SQL SOTA model
Last, we recommend the XiYanSQL-qwencoder-32B (https://github.com/XGenerationLab/XiYanSQL-QwenCoder), which is the SOTA model in text-to-sql.
We deployed the model on DashScope, so you need to set the following environment variables:
Contact us to get the key.
```yaml
model:
  name: "pre-xiyan_multi_dialect_v3"
  key: "KEY"
  url: "https://poc-dashscope.aliyuncs.com/compatible-mode/v1"
database:
```

#### Local LLMs
To support in the future.

### About the database
host, port, user, password, database are the connection information of the MySQL database.

You can use local or any remote databases. Currently we support MySQL (more dialects soon)
```yaml
database:
  host: "localhost"
  port: 3306
  user: "root"
  password: ""
  database: ""
```

## Citation
If you find our work helpful, feel free to give us a cite.
```bib
@article{xiyansql,
      title={A Preview of XiYan-SQL: A Multi-Generator Ensemble Framework for Text-to-SQL}, 
      author={Yingqi Gao and Yifu Liu and Xiaoxia Li and Xiaorong Shi and Yin Zhu and Yiming Wang and Shiqi Li and Wei Li and Yuntao Hong and Zhiling Luo and Jinyang Gao and Liyu Mou and Yu Li},
      year={2024},
      journal={arXiv preprint arXiv:2411.08599},
      url={https://arxiv.org/abs/2411.08599},
      primaryClass={cs.AI}
}
```


