from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class MainKbMessage(StrEnum):
    CHAT = "💬 Chat"


main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=MainKbMessage.CHAT)]],
    resize_keyboard=True,
    input_field_placeholder="Select an action...",
)
