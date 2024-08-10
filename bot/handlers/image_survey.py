from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

from bot.balance import predict_image_generation_cost
from bot.db.models import User
from bot.db.queries import get_ai_model, get_ai_models, pay_for_generation
from bot.generators import generate_image
from bot.keyboards import MainKbMessage, build_ai_models_kb, main_kb
from bot.middlewares import RequireUserMiddleware
from bot.surveys import ImageSurvey

router = Router(name=__name__)
router.message.outer_middleware(RequireUserMiddleware())


@router.message(F.text == MainKbMessage.IMAGE)
async def image_button_handler(message: Message, user: User, state: FSMContext) -> None:
    if user.balance > 0:
        await state.set_state(ImageSurvey.model)
        ai_models = await get_ai_models(type_name="image")
        await message.answer(
            text=markdown.text(
                "🌄", markdown.hbold("Image generation session started!"), "Type /cancel to stop at any time"
            )
        )
        await message.answer(
            text="🤖 What model to use?",
            reply_markup=build_ai_models_kb(ai_models=ai_models),
        )
    else:
        await message.answer(text="💸 To generate images, top up your balance")


@router.message(ImageSurvey.model)
async def image_model_state_handler(message: Message, state: FSMContext) -> None:
    ai_models = await get_ai_models(type_name="image")
    ai_model_names = [ai_model.name for ai_model in ai_models]

    if message.text not in ai_model_names:
        await message.answer(
            text="🚨 Invalid model input. Please click on a button",
            reply_markup=build_ai_models_kb(ai_models=ai_models),
        )
        return

    await state.update_data({"model": message.text})
    await state.set_state(ImageSurvey.query)
    await message.answer(text="🔍 What's your query?", reply_markup=ReplyKeyboardRemove())


@router.message(ImageSurvey.query)
async def image_query_state_handler(message: Message, user: User, state: FSMContext) -> None:
    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        data = await state.get_data()
        model_name = data["model"]

        ai_model = await get_ai_model(name=model_name)
        estimated_cost = predict_image_generation_cost(ai_model=ai_model)

        if estimated_cost > user.balance:
            await message.answer(text="💸 Top up your balance to generate this image", reply_markup=main_kb)
        else:
            await state.set_state(ImageSurvey.wait)
            image_url, images_number = await generate_image(query=message.text, model=model_name)
            await pay_for_generation(tg_id=user.tg_id, model_name=ai_model.name, usage=images_number)
            await message.answer_photo(photo=image_url, reply_markup=main_kb)

        await state.clear()


@router.message(ImageSurvey.wait)
async def image_wait_state_handler(message: Message) -> None:
    await message.answer(text="⏳ Generating image. Please wait...")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
