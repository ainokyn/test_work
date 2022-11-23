from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Operation, User


class CRUDBase:
    """
    Базовый класс CRUD операций.
    """
    def __init__(self, model):
        self.model = model


async def invested(session: AsyncSession, db_obj):
    """
    Механизм транзакции.
    """
    user_id = db_obj.user_from
    user_to_name = db_obj.name
    user_to_surname = db_obj.surname
    user_to_patronymic = db_obj.patronymic
    user_from = await session.execute(select(User).where(User.id == user_id))
    user_from = user_from.scalars().first()
    user_to = await session.execute(select(User).where(
        User.name == user_to_name,
        User.surname == user_to_surname,
        User.patronymic == user_to_patronymic))
    user_to = user_to.scalars().first()
    if user_to:
        if user_from.balance >= db_obj.amount:
            new_balance_user_from = user_from.balance-db_obj.amount
            new_balance_user_to = user_to.balance+db_obj.amount
            dict_optional = {
                'commit': True,
                'close_date': datetime.now()
            }
            for field in dict_optional:
                setattr(db_obj, field, dict_optional[field])
            setattr(user_from, 'balance', new_balance_user_from)
            setattr(user_to, 'balance', new_balance_user_to)
            session.add(user_from)
            session.add(user_to)
            session.add(db_obj)
            await session.commit()
            await session.refresh(user_from)
            await session.refresh(user_to)
            await session.refresh(db_obj)
            return db_obj
    session.rollback()
    raise HTTPException(status_code=400, detail="что-то пошло не так")


class CRUDDTransaction(CRUDBase):

    async def create_tranzaction(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        """
        Создает объект транзакции.
        """
        obj_in_data = obj_in.dict()
        obj_in_data['user_from'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await invested(session, db_obj)
        return db_obj


transaction_crud = CRUDDTransaction(Operation)
