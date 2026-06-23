from src.models.bookings import Status
from src.api.dependencies import DBDep, AuthUserDep, PaginationDep
from fastapi import APIRouter, Body, Request
from src.schemas.bookings import BookingAddRequestSchema, BookingUpdateRequestSchema, BookingOutSchema
from src.services.bookings import BookingServices
from src.tasks.tasks import task_generate_pdf, get_todays_bookings
from celery import chain
from celery.result import AsyncResult
from src.tasks.celery_app import celery_instance
import os

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    paging: PaginationDep,
) -> list[BookingOutSchema]:
    return await BookingServices(db).get_my_bookings(user_id, limit=paging.limit, offset=paging.offset)


@router.get("/")
async def get_all_bookings(db: DBDep, paging: PaginationDep):
    return BookingServices(db).get_all_bookings(limit=paging.limit, offset=paging.offset)


@router.post("/")
async def post_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    data: BookingAddRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "",
                "description": "",
                "value": {
                    "room_id": 17,
                    "from_date": "2026-03-18",
                    "to_date": "2026-03-20",
                },
            }
        }
    ),
) -> BookingOutSchema:
    new_booking = await BookingServices(db).add_booking(user_id, data)
    return new_booking


@router.delete("/{booking_id}")
async def delete_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    booking_id: int,
) -> dict:
    await BookingServices(db).delete_booking(booking_id=booking_id)
    return {"message": "delete success"}

@router.patch("/{booking_id}")
async def patch_booking(
    user_id: AuthUserDep,
    db: DBDep,
    booking_id: int,
    data: BookingUpdateRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "",
                "description": "",
                "value": {
                    "room_id": 25,
                    "from_date": "2026-06-22",
                    "to_date": "2026-06-28",
                },
            }
        })
) -> BookingOutSchema:
    """
    :param data: status: SUCCESS, PENDING, CANCELED
    :return:
    """
    result = await BookingServices(db).update_booking(user_id=user_id, booking_id=booking_id, data=data)
    return result


@router.post("/reports/generate/")
async def start_report_generation():
    report_workflow = chain(
        get_todays_bookings.s() | task_generate_pdf.s()
    )
    result_group = report_workflow.delay()
    return {"task_id": result_group.id, "status": "processing"}


@router.get("/reports/")
async def get_report(task_id: str, request: Request):
    result = AsyncResult(task_id, app=celery_instance)

    if result.state == "SUCCESS":
        relative_path = result.result

        file_name = os.path.basename(relative_path)

        full_url = request.url_for("media", path=f"reports/{file_name}")
        return {
            "status": "COMPLETED",
            "result": str(full_url)
        }

    elif result.state == "PENDING":
        return {
            "status": "PENDING",
            "message": "Задача всё еще выполняется или находится в очереди"
        }

    elif result.state == "FAILURE":
        return {
            "status": "FAILED",
            "error": str(result.info)
        }

    return {"status": result.state}
