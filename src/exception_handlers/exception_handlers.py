from fastapi import Request
from fastapi.responses import JSONResponse
from src.exception_handlers import exceptions


def register_exception_handlers(app):

    @app.exception_handler(exceptions.RoomNotFoundException)
    async def bad_room_handler(request: Request, exc: exceptions.RoomNotFoundException):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.exception_handler(exceptions.FacilityIsExistException)
    async def facility_conflict_handler(request: Request, exc: exceptions.FacilityIsExistException):
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(exceptions.FacilityNotFoundException)
    async def facility_delete_handler(request: Request, exc: exceptions.FacilityNotFoundException):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.exception_handler(exceptions.NotValidTimedeltaException)
    async def bad_request_handler(request: Request, exc: exceptions.NotValidTimedeltaException):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.exception_handler(exceptions.NotEmptyRoomsException)
    async def not_empty_room_handler(request: Request, exc: exceptions.NotEmptyRoomsException):
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(exceptions.NoResultException)
    async def not_found_handler(request: Request, exc: exceptions.NoResultException):
        return JSONResponse(status_code=404, content={"detail": exc.detail})
