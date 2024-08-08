import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

from bot.balance import predict_generation_cost
from bot.config import settings
from bot.db.models import User
from bot.db.queries import add_user, get_ai_model, get_ai_models
from bot.generators import generate_text
from bot.keyboards import MainKbMessage, build_ai_models_kb, main_kb
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
        await state.set_state(ChatSurvey.model)
        ai_models = await get_ai_models()
        await message.answer(
            text="🤖 What model to use?",
            reply_markup=build_ai_models_kb(ai_models=ai_models),
        )
    else:
        await message.answer(text="💸 To use the chat, top up your balance")


@root_router.message(ChatSurvey.model)
async def chat_model_state_handler(message: Message, state: FSMContext) -> None:
    ai_models = await get_ai_models()
    ai_model_names = [ai_model.name for ai_model in ai_models]

    if message.text not in ai_model_names:
        await message.answer(
            text="🚨 Invalid model input. Please click on a button",
            reply_markup=build_ai_models_kb(ai_models=ai_models),
        )
        return

    await state.update_data({"model": message.text})
    await state.set_state(ChatSurvey.query)
    await message.answer(text="🔍 What's your query?", reply_markup=ReplyKeyboardRemove())


@root_router.message(ChatSurvey.query)
async def chat_query_state_handler(message: Message, user: User, state: FSMContext) -> None:
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        data = await state.get_data()
        model_name = data["model"]

        ai_model = await get_ai_model(name=model_name)
        estimated_cost = predict_generation_cost(ai_model=ai_model, input_tokens=len(message.text))

        if estimated_cost > user.balance:
            await message.answer(text="💸 Top up your balance to send this query", reply_markup=main_kb)
        else:
            await state.set_state(ChatSurvey.wait)
            result, total_tokens = await generate_text(query=message.text, model=model_name)
            await message.answer(text=result, reply_markup=main_kb)

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
