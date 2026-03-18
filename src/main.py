from fastapi import FastAPI
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.users import router as users_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router


app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["Пользователи"])
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
