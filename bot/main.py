import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

from bot.config import settings
from bot.db.models import User
from bot.db.queries import add_user
from bot.generators import generate_text
from bot.keyboards import MainKbMessage, main_kb
from bot.middlewares import UserMiddleware
from bot.surveys import ChatSurvey

root_router = Router(name=__name__)


@root_router.message(CommandStart())
async def start_command_handler(message: Message, user: User | None) -> None:
    if not user:
        await add_user(tg_id=message.from_user.id)
    text = markdown.text("👋", markdown.hbold(message.from_user.full_name))
    await message.answer(text=text, reply_markup=main_kb)


@root_router.message(F.text == MainKbMessage.CHAT)
async def chat_button_handler(message: Message, user: User, state: FSMContext) -> None:
    if user.balance > 0:
        await state.set_state(ChatSurvey.query)
        await message.answer(text="🔍 What's your query?")
    else:
        await message.answer(text="💸 To use the chat, top up your balance")


@root_router.message(ChatSurvey.query)
async def chat_query_state_handler(message: Message, state: FSMContext) -> None:
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await state.set_state(ChatSurvey.wait)
        result = await generate_text(query=message.text)
        await message.answer(text=result)
        await state.clear()


@root_router.message(ChatSurvey.wait)
async def chat_wait_state_handler(message: Message) -> None:
    await message.answer(text="⏳ Processing previous query. Please wait...")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)


async def main() -> None:
    dp = Dispatcher()
    dp.message.outer_middleware(UserMiddleware())
    dp.include_router(root_router)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
