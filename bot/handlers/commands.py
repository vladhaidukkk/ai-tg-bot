from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.models import User
from bot.db.queries import add_user
from bot.keyboards import main_kb

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message, user: User | None) -> None:
    if not user:
        await add_user(tg_id=message.from_user.id)
    text = markdown.text("👋", markdown.hbold(message.from_user.full_name))
    await message.answer(text=text, reply_markup=main_kb)


@router.message(Command("cancel"))
async def cancel_command_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text="🚫 Survey was cancelled", reply_markup=main_kb)
