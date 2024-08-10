from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from bot.db.core import session_factory
from bot.db.models import AIModel, AIType, User
from bot.errors import AIModelNotFoundError, UserAlreadyExistsError, UserNotFoundError


async def add_user(tg_id: int) -> User:
    async with session_factory() as session:
        try:
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()
        except IntegrityError as err:
            raise UserAlreadyExistsError(f"user with tg_id={tg_id} already exists") from err
        else:
            return new_user


async def get_user(tg_id: int) -> User | None:
    async with session_factory() as session:
        query = select(User).filter_by(tg_id=tg_id)
        return await session.scalar(query)


async def get_ai_models(type_name: str | None = None) -> list[AIModel]:
    async with session_factory() as session:
        query = select(AIModel).join(AIType, AIModel.type_id == AIType.id)
        if type_name:
            query = query.filter(AIType.name == type_name)
        result = await session.execute(query)
        return result.scalars().all()


async def get_ai_model(name: str) -> AIModel | None:
    async with session_factory() as session:
        query = select(AIModel).filter_by(name=name)
        return await session.scalar(query)


async def pay_for_generation(tg_id: int, model_name: str, usage: int) -> Decimal:
    async with session_factory() as session:
        user_query = select(User).filter_by(tg_id=tg_id)
        user = await session.scalar(user_query)
        if not user:
            raise UserNotFoundError(f"user with tg_id={tg_id} not found")

        ai_model_query = select(AIModel).filter_by(name=model_name)
        ai_model = await session.scalar(ai_model_query)
        if not ai_model:
            raise AIModelNotFoundError(f"ai_model with name={model_name} not found")

        cost = ai_model.price * Decimal(usage)
        user.balance -= cost
        await session.commit()
        return cost
