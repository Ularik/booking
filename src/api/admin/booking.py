from fastapi import APIRouter

router = APIRouter()


@router.patch("/{booking_id}")
async def update_booking(booking_id: int):
    pass