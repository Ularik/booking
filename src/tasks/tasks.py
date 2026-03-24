from src.tasks.celery_app import celery_instance
from time import sleep
from src.repositories.bookings import BookingsRepository
from src.api.dependencies import DbManager
from src.database import AsyncSessionNullPool
import asyncio
from PIL import Image
import os

@celery_instance.task
def task_test():
    sleep(5)
    print("I am groot")


async def get_todays_bookings_util():
    async with DbManager(session_factory=AsyncSessionNullPool) as db:
        bookings = await db.bookingsModel.get_todays_bookings()
        print(f"Bookings={bookings}")


@celery_instance.task(name="booking_todays_chekins")
def get_todays_bookings():
    asyncio.run(get_todays_bookings_util())

@celery_instance.task
def save_resized_images(input_path: str):
    sizes = [1000, 500, 200]

    output_dir = 'src/static/images'

    with Image.open(input_path) as img:
        original_width, original_height = img.size

        for width in sizes:
            # вычисляем новую высоту с сохранением пропорций
            ratio = width / original_width
            height = int(original_height * ratio)

            resized = img.resize((width, height), Image.LANCZOS)

            base_name = os.path.basename(input_path)
            name, ext = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{name}_{width}px{ext}")

            resized.save(output_path)

            print(f"Saved: {output_path} ({width}x{height})")