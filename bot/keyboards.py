from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import AIModel


class MainKbMessage(StrEnum):
    CHAT = "💬 Chat"
    IMAGE = "🌄 Image"


main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=MainKbMessage.CHAT), KeyboardButton(text=MainKbMessage.IMAGE)]],
    resize_keyboard=True,
    input_field_placeholder="Select an action...",
)


def build_ai_models_kb(ai_models: list[AIModel]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for ai_model in ai_models:
        builder.button(text=ai_model.name)
    return builder.adjust(2).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Select a model...",
    )
