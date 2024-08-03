from openai import AsyncOpenAI
from openai.types import ChatModel

from bot.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_text(query: str, model: ChatModel = "gpt-3.5-turbo") -> str:
    completion = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": query}])
    return completion.choices[0].message.content