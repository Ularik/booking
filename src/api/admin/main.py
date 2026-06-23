from fastapi import APIRouter
from src.api.admin.booking import router as booking_router

router = APIRouter()

router.include_router(booking_router, prefix='/booking')