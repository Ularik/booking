from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from src.logging_conf.logging_conf import setup_logging
from src.exception_handlers.exception_handlers import register_exception_handlers
from fastapi_cache.backends.redis import RedisBackend

from src.api.dependencies import get_current_user_id
from src.init import redis_manager
from src.api.admin.main import router as admin_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.users import router as users_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount("/media", StaticFiles(directory="src/media"), name="media")

app.include_router(admin_router,
                   prefix="/admin",
                   tags=["admin"],
                   dependencies=[Depends(get_current_user_id)],
                   responses={403: {"description": "Forbidden"}},
                   )

app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(images_router)
