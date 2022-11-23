from fastapi import APIRouter

from api_tranzanction import router as tranzaction_router
from api_users import router as users_router

main_router = APIRouter()
main_router.include_router(users_router)
main_router.include_router(tranzaction_router, prefix='/tranzaction')
