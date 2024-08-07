from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db.queries import get_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        data["user"] = await get_user(tg_id=event.from_user.id)
        return await handler(event, data)
