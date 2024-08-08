from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db.queries import get_user


class InjectUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        data["user"] = await get_user(tg_id=event.from_user.id)
        return await handler(event, data)


class RequireUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        if data.get("user"):
            return await handler(event, data)
        await event.answer("🤗 Enter /start to begin your journey")
