from sqlalchemy import select

from bot.db.core import session_factory
from bot.db.models import UserModel


async def add_user(tg_id: int) -> UserModel | None:
    async with session_factory() as session:
        find_user_query = select(UserModel).filter_by(tg_id=tg_id)
        existing_user = await session.scalar(find_user_query)
        if existing_user:
            return None

        new_user = UserModel(tg_id=tg_id)
        session.add(new_user)
        await session.commit()

        return new_user
