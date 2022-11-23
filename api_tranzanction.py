from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import transaction_crud
from models import User, get_async_session
from shemas import OperationCreate, OperationDB
from users import current_user

router = APIRouter()


@router.post('/',
             response_model=OperationDB,
             )
async def create_transaction(
        transactions: OperationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """ Создание транзакции.Только для зарегистрированных пользователей."""
    transaction = await transaction_crud.create_tranzaction(transactions,
                                                            session,
                                                            user)
    return transaction
