from aiogram import Router

from .chat_survey import router as chat_survey_router
from .commands import router as commands_router
from .image_survey import router as image_survey_router

router = Router(name=__name__)
router.include_routers(
    commands_router,
    chat_survey_router,
    image_survey_router,
)
