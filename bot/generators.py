import asyncio

import httpx
from openai import AsyncOpenAI
from openai.types import ChatModel

from bot.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key, http_client=httpx.AsyncClient(proxy=settings.openai_proxy))


async def generate_text(query: str, model: ChatModel = "gpt-3.5-turbo") -> str:
    if settings.openai_stub_responses:
        await asyncio.sleep(2)
        return "Stub text"

    completion = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": query}])
    return completion.choices[0].message.content
