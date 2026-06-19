from src.tasks.celery_app import celery_instance
from time import sleep
from src.api.dependencies import DbManager
from src.models.bookings import Status
from src.database import AsyncSessionNullPool
from src.schemas.bookings import BookingUpdateSchema
from PIL import Image
import os
import asyncio


async def delete_booking(booking_id: int):
    async with DbManager(session_factory=AsyncSessionNullPool) as db:
        bookings = await db.bookingsModel.get_one(id=booking_id)
        if bookings.status == Status.PENDING:
            updated_schema = BookingUpdateSchema(room_id=bookings.room_id, status=Status.CANCELED)
            booking = await db.bookingsModel.edit(data=updated_schema, id=booking_id)
            await db.save()
            print(f'Статус обновлен на {booking.status}')


@celery_instance.task
def check_is_paid(booking_id: int):
    asyncio.run(delete_booking(booking_id))


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

    output_dir = "src/static/images"

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
