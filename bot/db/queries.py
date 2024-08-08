from sqlalchemy import select

from bot.db.core import session_factory
from bot.db.models import AIModel, User


async def add_user(tg_id: int) -> User | None:
    async with session_factory() as session:
        find_user_query = select(User).filter_by(tg_id=tg_id)
        existing_user = await session.scalar(find_user_query)
        if existing_user:
            return None

        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()

        return new_user


async def get_user(tg_id: int) -> User | None:
    async with session_factory() as session:
        query = select(User).filter_by(tg_id=tg_id)
        return await session.scalar(query)


async def get_ai_models() -> list[AIModel]:
    async with session_factory() as session:
        query = select(AIModel)
        result = await session.execute(query)
        return result.scalars().all()


async def get_ai_model(name: str) -> AIModel | None:
    async with session_factory() as session:
        query = select(AIModel).filter_by(name=name)
        return await session.scalar(query)
