import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings

root_router = Router(name=__name__)


@root_router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = markdown.text("👋", markdown.hbold(message.from_user.full_name))
    await message.answer(text=text)


async def main() -> None:
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(root_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
