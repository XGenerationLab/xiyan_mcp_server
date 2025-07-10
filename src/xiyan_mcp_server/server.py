import argparse
import logging
import os
import signal
import sys

import yaml  # 添加yaml库导入
from mcp.server import FastMCP
from mcp.types import TextContent

from .database_env import DataBaseEnv
from .utils.db_config import DBConfig
from .utils.db_source import HITLSQLDatabase
from .utils.db_util import init_db_conn
from .utils.file_util import extract_sql_from_qwen
from .utils.llm_util import call_openai_sdk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("xiyan_mcp_server")


# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def get_yml_config():
    config_path = os.getenv(
        "YML", os.path.join(os.path.dirname(__file__), "config_demo.yml")
    )
    logger.info(f"Loading configuration from {config_path}")
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_path} not found.")
        raise
    except yaml.YAMLError as exc:
        logger.error(f"Error parsing configuration file {config_path}: {exc}")
        raise


def get_xiyan_config(db_config):
    dialect = db_config.get("dialect", "mysql")

    if dialect.lower() == "sqlite":
        xiyan_db_config = DBConfig(
            dialect=dialect,
            db_path=db_config.get("db_path"),
        )
    else:
        xiyan_db_config = DBConfig(
            dialect=dialect,
            db_name=db_config["database"],
            user_name=db_config["user"],
            db_pwd=db_config["password"],
            db_host=db_config["host"],
            port=db_config["port"],
        )
    return xiyan_db_config


global_config = get_yml_config()
mcp_config = global_config.get("mcp", {})
model_config = global_config["model"]
global_db_config = global_config.get("database")
global_xiyan_db_config = get_xiyan_config(global_db_config)
dialect = global_db_config.get("dialect", "mysql")


mcp = FastMCP("xiyan", **mcp_config)


@mcp.resource(
    dialect
    + "://"
    + (
        global_db_config.get("db_path", "")
        if dialect.lower() == "sqlite"
        else "/" + global_db_config.get("database", "")
    )
)
async def read_resource() -> str:
    db_engine = init_db_conn(global_xiyan_db_config)
    db_source = HITLSQLDatabase(db_engine)
    return db_source.mschema.to_mschema()


@mcp.resource(dialect + "://{table_name}")
async def read_resource(table_name) -> str:
    """Read table contents."""
    try:
        db_engine = init_db_conn(global_xiyan_db_config)
        db_source = HITLSQLDatabase(db_engine)
        records, columns = db_source.fetch_with_column_name(
            f"SELECT * FROM {table_name}"
        )
        result = [",".join(map(str, row)) for row in records]
        return "\n".join([",".join(columns)] + result)
    except Exception as e:
        raise RuntimeError(f"Database error: {str(e)}")


def sql_gen_and_execute(db_env: DataBaseEnv, query: str):
    """
    Transfers the input natural language question to sql query (known as Text-to-sql) and executes it on the database.
     Args:
        query: natural language to query the database. e.g. 查询在2024年每个月，卡宴的各经销商销量分别是多少
    """

    # db_env = context_variables.get('db_env', None)
    prompt = f"""你现在是一名{db_env.dialect}数据分析专家，你的任务是根据参考的数据库schema和用户的问题，编写正确的SQL来回答用户的问题，生成的SQL用``sql 和```包围起来。
【数据库schema】
{db_env.mschema_str}

【问题】
{query}
"""
    # logger.info(f"SQL generation prompt: {prompt}")

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"用户的问题是: {query}"},
    ]
    param = {
        "model": model_config["name"],
        "messages": messages,
        "key": model_config["key"],
        "url": model_config["url"],
        "api_version": model_config.get("api_version"),
    }

    try:
        response = call_openai_sdk(**param)
        content = response.choices[0].message.content
        sql_query = extract_sql_from_qwen(content)
        status, res = db_env.database.fetch(sql_query)
        if not status:
            for idx in range(3):
                sql_query = sql_fix(
                    db_env.dialect, db_env.mschema_str, query, sql_query, res
                )
                status, res = db_env.database.fetch(sql_query)
                if status:
                    break

        sql_res = db_env.database.fetch_truncated(sql_query, max_rows=100)
        markdown_res = db_env.database.trunc_result_to_markdown(sql_res)
        logger.info(f"SQL query: {sql_query}\nSQL result: {sql_res}")
        return markdown_res.strip()

    except Exception as e:
        return str(e)


def sql_fix(
    dialect: str, mschema: str, query: str, sql_query: str, error_info: str
):
    system_prompt = """现在你是一个{dialect}数据分析专家，需要阅读一个客户的问题，参考的数据库schema，该问题对应的待检查SQL，以及执行该SQL时数据库返回的语法错误，请你仅针对其中的语法错误进行修复，输出修复后的SQL。
注意：
1、仅修复语法错误，不允许改变SQL的逻辑。
2、生成的SQL用```sql 和```包围起来。

【数据库schema】
{schema}
""".format(dialect=dialect, schema=mschema)
    user_prompt = """【问题】
{question}

【待检查SQL】
{sql}

【错误信息】
{sql_res}""".format(question=query, sql=sql_query, sql_res=error_info)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    param = {
        "model": model_config["name"],
        "messages": messages,
        "key": model_config["key"],
        "url": model_config["url"],
    }

    response = call_openai_sdk(**param)
    content = response.choices[0].message.content
    sql_query = extract_sql_from_qwen(content)

    return sql_query


def call_xiyan(query: str) -> str:
    """Fetch the data from database through a natural language query

    Args:
        query: The query in natual language
    """

    logger.info(f"Calling tool with arguments: {query}")
    try:
        db_engine = init_db_conn(global_xiyan_db_config)
        db_source = HITLSQLDatabase(db_engine)
    except Exception as e:
        return "数据库连接失败" + str(e)
    logger.info("Calling xiyan")
    env = DataBaseEnv(db_source)
    res = sql_gen_and_execute(env, query)

    return str(res)


@mcp.tool()
def get_data(query: str) -> list[TextContent]:
    """Fetch the data from database through a natural language query

    Args:
        query: The query in natural language
    """

    res = call_xiyan(query)
    return [TextContent(type="text", text=res)]


def main():
    parser = argparse.ArgumentParser(description="Run MCP server.")
    parser.add_argument(
        "transport",
        nargs="?",
        default="stdio",
        choices=["stdio", "streamable-http", "sse"],
        help="Transport type (stdio, streamable-http or sse)",
    )
    parser.add_argument(
        "host", default="localhost", help="host for the http transport"
    )

    parser.add_argument(
        "port", default="8000", help="port for the http transport"
    )
    args = parser.parse_args()

    if args.transport == "streamable-http":
        mcp.settings.port = args.port
        mcp.settings.host = args.host
        logger.info(f"MCP server running at {args.host}/{args.port}")
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
