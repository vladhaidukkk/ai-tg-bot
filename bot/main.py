import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings
from bot.generators import generate_text

root_router = Router(name=__name__)


@root_router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = markdown.text("👋", markdown.hbold(message.from_user.full_name))
    await message.answer(text=text)


@root_router.message(Command("ai", magic=F.args))
async def ai_command_handler(message: Message, command: CommandObject) -> None:
    result = await generate_text(query=command.args)
    await message.answer(text=result)


@root_router.message(Command("ai"))
async def ai_command_fallback_handler(message: Message) -> None:
    await message.answer(text="Pass a query to the /ai command")


async def main() -> None:
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(root_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
