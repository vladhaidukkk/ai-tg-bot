from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings
from bot.db.queries import get_users
from bot.filters import AdminFilter
from bot.surveys import NotifySurvey

router = Router(name=__name__)


@router.message(AdminFilter(), Command("notify"))
async def notify_command_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(NotifySurvey.message)
    text = markdown.text("🔔", markdown.hbold("Enter the notification message"))
    await message.answer(text=text)


@router.message(NotifySurvey.message)
async def notify_message_state_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("⏳ Start sending notification")

    users = await get_users()
    for user in users:
        if user.tg_id in settings.bot.admins:
            continue
        try:
            await message.copy_to(chat_id=user.tg_id)
        except TelegramBadRequest:
            # User can delete the chat or even block the bot.
            pass

    await message.answer("✅ Notification has been sent")
