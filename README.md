<h1 align="center">XiYan MCP Server</h1>
<p align="center">
  <a href="https://github.com/XGenerationLab/XiYan-SQL"><img alt="MCP Playwright" src="https://raw.githubusercontent.com/XGenerationLab/XiYan-SQL/main/xiyanGBI.png" height="60"/></a>
</p>
<p align="center">
  <b>A Model Context Protocol (MCP) server that enables natural language queries to databases</b><br/>
  <sub>powered by <a href="https://github.com/XGenerationLab/XiYan-SQL" >XiYan-SQL</a>, SOTA of text-to-sql on open benchmarks</sub>
</p>

<p align="center">
💻 <a href="https://github.com/XGenerationLab/xiyan_mcp_server" >XiYan-mcp-server</a> | 
🌐 <a href="https://github.com/XGenerationLab/XiYan-SQL" >XiYan-SQL</a> |
📖 <a href="https://arxiv.org/abs/2411.08599"> Arxiv</a> | 
📄 <a href="https://paperswithcode.com/paper/xiyan-sql-a-multi-generator-ensemble" >PapersWithCode</a>
💻 <a href="https://huggingface.co/collections/XGenerationLab/xiyansql-models-67c9844307b49f87436808fc">HuggingFace</a> |
🤖 <a href="https://modelscope.cn/collections/XiYanSQL-Models-4483337b614241" >ModelScope</a> |
🌕 <a href="https://bailian.console.aliyun.com/xiyan">析言GBI</a> 
<br />
<img src="https://badge.mcpx.dev/?type=server%20%27MCP%20Server%27" alt="MCP Server" />
<a href="https://arxiv.org/abs/2411.08599"><img src="imgs/Paper-Arxiv-orange.svg" ></a>
<a href="https://opensource.org/licenses/Apache-2.0">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0" />
</a>
<a href="https://pepy.tech/projects/xiyan-mcp-server"><img src="https://static.pepy.tech/badge/xiyan-mcp-server" alt="PyPI Downloads"></a>
  <a href="https://smithery.ai/server/@XGenerationLab/xiyan_mcp_server"><img alt="Smithery Installs" src="https://smithery.ai/badge/@XGenerationLab/xiyan_mcp_server" height="20"/></a>
<a href="https://github.com/XGenerationLab/xiyan_mcp_server" target="_blank">
    <img src="https://img.shields.io/github/stars/XGenerationLab/xiyan_mcp_server?style=social" alt="GitHub stars" />
</a>
<br />
<a href="https://github.com/XGenerationLab/xiyan_mcp_server" >English</a> | <a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/README_zh.md"> 中文 </a><br />
<a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/imgs/dinggroup_out.png">Ding Group钉钉群</a>｜ 
<a href="https://weibo.com/u/2540915670" target="_blank">Follow me on Weibo</a>
</p>


## Table of Contents

- [Features](#features)
- [Preview](#preview)
  - [Architecture](#architecture)
  - [Best Practice](#best-practice)
  - [Tools Preview](#tools-preview)
- [Installation](#installation)
  - [Installing from pip](#installing-from-pip)
  - [Installing from Smithery.ai](#installing-from-smitheryai)
- [Configuration](#configuration)
  - [LLM Configuration](#llm-configuration)
    - [General LLMs](#general-llms)
    - [Text-to-SQL SOTA model](#text-to-sql-sota-model)
    - [Local Model](#local-model)
  - [Database Configuration](#database-configuration)
    - [MySQL](#mysql)
    - [PostgreSQL](#postgresql)
- [Launch](#launch)
  - [Claude Desktop](#claude-desktop)
  - [Cline](#cline)
  - [Goose](#goose)
  - [Cursor](#cursor)
- [It Does Not Work](#it-does-not-work)
- [Citation](#citation)


## Features
- 🌐 Fetch data by natural language through [XiYanSQL](https://github.com/XGenerationLab/XiYan-SQL)
- 🤖 Support general LLMs (GPT,qwenmax), Text-to-SQL SOTA model
- 💻 Support pure local mode (high security!)
- 📝 Support MySQL and PostgreSQL. 
- 🖱️ List available tables as resources
- 🔧 Read table contents

## Preview
### Architecture
There are two ways to integrate this server in your project, as shown below:
The left is remote mode, which is the default mode. It requires an API key to access the xiyanSQL-qwencoder-32B model from service provider (see [Configuration](#Configuration)).
Another mode is local mode, which is more secure. It does not require the API key.

![architecture.png](imgs/architecture.png)
### Best practice and reports

["Build a local data assistant using MCP + Modelscope API-Inference without writing a single line of code"](https://mp.weixin.qq.com/s/tzDelu0W4w6t9C0_yYRbHA)

["Xiyan MCP on Modelscope"](https://modelscope.cn/headlines/article/1142)

### Evaluation on MCPBench
The following figure illustrates the performance of the XiYan MCP server as measured by the MCPBench benchmark. The XiYan MCP server demonstrates superior performance compared to both the MySQL MCP server and the PostgreSQL MCP server, achieving a lead of 2-22 percentage points. The detailed experiment results can be found at [MCPBench](https://github.com/modelscope/MCPBench) and the report ["Evaluation Report on MCP Servers"](https://arxiv.org/abs/2504.11094).

![exp_mcpbench.png](imgs/exp_mcpbench.png)

### Tools Preview
 - The tool ``get_data`` provides a natural language interface for retrieving data from a database. This server will convert the input natural language into SQL using a built-in model and call the database to return the query results.

 - The ``{dialect}://{table_name}`` resource allows obtaining a portion of sample data from the database for model reference when a specific table_name is specified. 
- The ``{dialect}://`` resource will list the names of the current databases

## Installation
### Installing from pip

Python 3.11+ is required. 
You can install the server through pip, and it will install the latest version:

```bash
pip install xiyan-mcp-server
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

### Installing from Smithery.ai
See [@XGenerationLab/xiyan_mcp_server](https://smithery.ai/server/@XGenerationLab/xiyan_mcp_server)

Not fully tested.

## Configuration

You need a YAML config file to configure the server.
A default config file is provided in config_demo.yml which looks like this:

```yaml
model:
  name: "XGenerationLab/XiYanSQL-QwenCoder-32B-2412"
  key: ""
  url: "https://api-inference.modelscope.cn/v1/"

database:
  host: "localhost"
  port: 3306
  user: "root"
  password: ""
  database: ""
```

### LLM Configuration
``Name`` is the name of the model to use, ``key`` is the API key of the model, ``url`` is the API url of the model. We support following models.

| versions | general LLMs(GPT,qwenmax)                                             | SOTA model by Modelscope                   | SOTA model by Dashscope                                   | Local LLMs            |
|----------|-------------------------------|--------------------------------------------|-----------------------------------------------------------|-----------------------|
| description| basic, easy to use | best performance, stable, recommand        | best performance, for trial                               | slow, high-security   |
| name     | the official model name (e.g. gpt-3.5-turbo,qwen-max)                 | XGenerationLab/XiYanSQL-QwenCoder-32B-2412 | xiyansql-qwencoder-32b                                    | xiyansql-qwencoder-3b |
| key      | the API key of the service provider (e.g. OpenAI, Alibaba Cloud)      | the API key of modelscope                  | the API key via email                                     | ""                    |
| url      | the endpoint of the service provider (e.g."https://api.openai.com/v1") | https://api-inference.modelscope.cn/v1/    | https://xiyan-stream.biz.aliyun.com/service/api/xiyan-sql | http://localhost:5090 |

#### General LLMs
If you want to use the general LLMs, e.g. gpt3.5, you can directly config like this:
```yaml
model:
  name: "gpt-3.5-turbo"
  key: "YOUR KEY "
  url: "https://api.openai.com/v1"
database:
```

If you want to use Qwen from Alibaba, e.g. Qwen-max, you can use following config:
```yaml
model:
  name: "qwen-max"
  key: "YOUR KEY "
  url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
database:
```
#### Text-to-SQL SOTA model
We recommend the XiYanSQL-qwencoder-32B (https://github.com/XGenerationLab/XiYanSQL-QwenCoder), which is the SOTA model in text-to-sql, see [Bird benchmark](https://bird-bench.github.io/).
There are two ways to use the model. You can use either of them.
(1) [Modelscope](https://www.modelscope.cn/models/XGenerationLab/XiYanSQL-QwenCoder-32B-2412),  (2) Alibaba Cloud DashScope.


##### (1) Modelscope version
You need to apply a ``key`` of API-inference from Modelscope, https://www.modelscope.cn/docs/model-service/API-Inference/intro
Then you can use the following config:
```yaml
model:
  name: "XGenerationLab/XiYanSQL-QwenCoder-32B-2412"
  key: ""
  url: "https://api-inference.modelscope.cn/v1/"
```

Read our [model description](https://www.modelscope.cn/models/XGenerationLab/XiYanSQL-QwenCoder-32B-2412) for more details. 

##### (2) Dashscope version

We deployed the model on Alibaba Cloud DashScope, so you need to set the following environment variables:
Send me your email to get the ``key``. ( godot.lzl@alibaba-inc.com )
In the email, please attach the following information:
```yaml
name: "YOUR NAME",
email: "YOUR EMAIL",
organization: "your college or Company or Organization"
```
We will send you a ``key`` according to your email. And you can fill the ``key`` in the yml file.
The ``key`` will be expired by  1 month or 200 queries or other legal restrictions.


```yaml
model:
  name: "xiyansql-qwencoder-32b"
  key: "KEY"
  url: "https://xiyan-stream.biz.aliyun.com/service/api/xiyan-sql"
database:
```

Note: this model service is just for trial, if you need to use it in production, please contact us.

Alternatively, you can also deploy the model [XiYanSQL-qwencoder-32B](https://github.com/XGenerationLab/XiYanSQL-QwenCoder) on your own server.

#### Local Model
Note: the local model is slow (about 12 seconds per query on my macbook).
If you need a stable and fast service, we still recommend to use the modelscope version.

To run xiyan_mcp_server in local mode, you need 
1) a PC/Mac with at least 16GB RAM
2) 6GB disk space

Step 1: Install additional Python packages
```bash
pip install flask modelscope torch==2.2.2 accelerate>=0.26.0 numpy=2.2.3
```

Step 2: (optional) manually download the model
We recommend [xiyansql-qwencoder-3b](https://www.modelscope.cn/models/XGenerationLab/XiYanSQL-QwenCoder-3B-2502/).
You can manually download the model by
```bash
modelscope download --model XGenerationLab/XiYanSQL-QwenCoder-3B-2502
```
It will take you 6GB disk space.

Step 3: download the script and run server. src/xiyan_mcp_server/local_xiyan_server.py



```bash
python local_xiyan_server.py
```
The server will be running on http://localhost:5090/

Step 4: prepare config and run xiyan_mcp_server
the config.yml should be like:
```yml
model:
  name: "xiyansql-qwencoder-3b"
  key: "KEY"
  url: "http://127.0.0.1:5090"
```

Till now the local mode is ready.

### Database Configuration
``host``, ``port``, ``user``, ``password``, ``database`` are the connection information of the database.

You can use local or any remote databases. Now we support MySQL and PostgreSQL(more dialects soon).

#### MySQL

```yaml
database:
  host: "localhost"
  port: 3306
  user: "root"
  password: ""
  database: ""
```
#### PostgreSQL
Step 1: Install Python packages
```bash
pip install psycopg2
```
Step 2: prepare the config.yml like this:
```yaml
database:
  dialect: "postgresql"
  host: "localhost"
  port: 5432
  user: ""
  password: ""
  database: ""
```

Note that ``dialect`` should be ``postgresql`` for postgresql.
## Launch
### Claude Desktop
Add this in your Claude Desktop config file, ref <a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/imgs/claude_desktop.jpg">Claude Desktop config example</a>
```json
{
    "mcpServers": {
        "xiyan-mcp-server": {
            "command": "python",
            "args": [
                "-m",
                "xiyan_mcp_server"
            ],
            "env": {
                "YML": "PATH/TO/YML"
            }
        }
    }
}
```
### Cline
Prepare the config like [Claude Desktop](#claude-desktop)

### Goose
Add following command in the config, ref <a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/imgs/goose.jpg">Goose config example</a>

```yaml
env YML=path/to/yml python -m xiyan_mcp_server
```
### Cursor
Use the same command like [Goose](#goose).


### Witsy
Add following in command:
```yaml
python -m xiyan_mcp_server
```
Add an env: key is YML and value is the path to your yml file.
Ref <a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/imgs/witsy.jpg">Witsy config example</a>
## It Does Not Work!
Contact us:
<a href="https://github.com/XGenerationLab/xiyan_mcp_server/blob/main/imgs/dinggroup_out.png">Ding Group钉钉群</a>｜ 
<a href="https://weibo.com/u/2540915670" target="_blank">Follow me on Weibo</a>


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
