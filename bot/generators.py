import asyncio

import httpx
from openai import AsyncOpenAI
from openai.types import ChatModel, ImageModel

from bot.config import settings

client = AsyncOpenAI(api_key=settings.openai.api_key, http_client=httpx.AsyncClient(proxy=settings.openai.proxy))


async def generate_text(query: str, model: ChatModel) -> tuple[str, int]:
    if settings.openai.stub_responses:
        await asyncio.sleep(2)
        content = "Stub text"
        return content, len(query) + len(content)

    completion = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": query}])
    return completion.choices[0].message.content, completion.usage.total_tokens


async def generate_image(query: str, model: ImageModel) -> tuple[str, int]:
    number = 1

    if settings.openai.stub_responses:
        await asyncio.sleep(2)
        return "https://picsum.photos/1024", number

    response = await client.images.generate(
        model=model,
        prompt=query,
        size="1024x1024",
        quality="standard",
        n=number,
    )
    return response.data[0].url, number
