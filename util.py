import os
import httpx
import asyncio
import tiktoken
from datetime import datetime, timedelta
from typing import Union, Dict, List


def format_date() -> list[str]:
    # ['2023-04-01', '2023-04-30']
    today = datetime.now()
    year = today.year
    month = today.month
    last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day
    formatted_first_day = f"{year}-{str(month).zfill(2)}-01"
    formatted_last_day = f"{year}-{str(month).zfill(2)}-{str(last_day).zfill(2)}"
    return [formatted_first_day, formatted_last_day]


def get_proxies(package) -> Union[None | Dict[str, str]]:
    SOCKS_PROXY_HOST = os.getenv("SOCKS_PROXY_HOST")
    SOCKS_PROXY_PORT = os.getenv("SOCKS_PROXY_PORT")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY")
    proxy, proxies = "", None
    if SOCKS_PROXY_HOST and SOCKS_PROXY_PORT:
        SOCKS_PROXY_USERNAME = os.getenv("SOCKS_PROXY_USERNAME")
        SOCKS_PROXY_PASSWORD = os.getenv("SOCKS_PROXY_PASSWORD")
        if SOCKS_PROXY_USERNAME and SOCKS_PROXY_PASSWORD:
            proxy = f"socks5://{SOCKS_PROXY_USERNAME}:{SOCKS_PROXY_PASSWORD}@{SOCKS_PROXY_HOST}:{SOCKS_PROXY_PORT}"
        else:
            proxy = f"socks5://{SOCKS_PROXY_HOST}:{SOCKS_PROXY_PORT}"
    elif HTTPS_PROXY:
        proxy = HTTPS_PROXY
    if package == "httpx" and proxy:
        proxies = {
            "http://": proxy,
            "https://": proxy,
        }
    if package == "openai" and proxy:
        proxies = proxy
    return proxies


async def get_key_usage():
    OPENAI_API_BASE_URL = base_url if (base_url:=os.getenv('OPENAI_API_BASE_URL')) else "https://api.openai.com"
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    proxies = get_proxies(package="httpx")
    startDate, endDate = format_date()
    url_usage = f"{OPENAI_API_BASE_URL}/v1/dashboard/billing/usage?start_date={startDate}&end_date={endDate}"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(proxies=proxies) as client:
        resp = await client.get(url=url_usage, headers=headers)
        data = resp.json()
        usage = round(data.get("total_usage")) / 100
        return usage


async def num_tokens_from_messages(messages:List[dict], model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            return await num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
        elif model == "gpt-4":
            print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
            return await num_tokens_from_messages(messages, model="gpt-4-0314")
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
