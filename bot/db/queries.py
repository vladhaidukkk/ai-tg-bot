from decimal import Decimal
from functools import wraps
from typing import Callable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import session_factory
from bot.db.models import AIModel, AIType, User
from bot.errors import AIModelNotFoundError, UserAlreadyExistsError, UserNotFoundError


def inject_session(fn: Callable) -> Callable:
    @wraps(fn)
    async def wrapper(*args: any, **kwargs: any) -> any:
        async with session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper


@inject_session
async def add_user(session: AsyncSession, tg_id: int) -> User:
    try:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except IntegrityError as err:
        raise UserAlreadyExistsError(f"user with tg_id={tg_id} already exists") from err
    else:
        return new_user


@inject_session
async def get_user(session: AsyncSession, tg_id: int) -> User | None:
    query = select(User).filter_by(tg_id=tg_id)
    return await session.scalar(query)


@inject_session
async def get_ai_models(session: AsyncSession, type_name: str | None = None) -> list[AIModel]:
    query = select(AIModel).join(AIType, AIModel.type_id == AIType.id)
    if type_name:
        query = query.filter(AIType.name == type_name)
    result = await session.execute(query)
    return list(result.scalars().all())


@inject_session
async def get_ai_model(session: AsyncSession, name: str) -> AIModel | None:
    query = select(AIModel).filter_by(name=name)
    return await session.scalar(query)


@inject_session
async def pay_for_generation(session: AsyncSession, tg_id: int, model_name: str, usage: int) -> Decimal:
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
