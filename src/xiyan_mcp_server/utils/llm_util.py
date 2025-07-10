import logging

from openai import AzureOpenAI, OpenAI


def call_openai_sdk(**args):
    key = args["key"]
    base_url = args["url"]

    if "azure" in base_url:
        api_version = args.get("api_version", "2025-01-01-preview")
        client = AzureOpenAI(
            api_version=api_version,
            api_key=key,
            azure_endpoint=base_url,
            azure_deployment=args.get("model", "gpt-35-turbo"),
        )
        logging.info("Configured AzureOpenAI")
    else:
        client = OpenAI(
            api_key=key,
            base_url=base_url,
        )
    del args["key"]
    del args["url"]
    del args["api_version"]
    completion = client.chat.completions.create(**args)
    return completion
