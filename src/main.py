from fastapi import FastAPI
from src.api.hotels import router as hotels_router


app = FastAPI()

app.include_router(hotels_router)
