class NoResultException(Exception):
    detail = "Ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(NoResultException):
    detail = "Объект не найден"


class HotelNotFoundException(NoResultException):
    detail = "Отель не найден"


class RoomNotFoundException(NoResultException):
    detail = "Номер не найден"


class NotEmptyRoomsException(NoResultException):
    detail = "Таких номеров не осталось"


class UniqueObjIsExistException(Exception):
    detail = 'Такой объект уже существует'


class RoomAlreadyExistException(UniqueObjIsExistException):
    detail = 'Такой номер уже существует'

class ThisUserIsExistException(UniqueObjIsExistException):
    detail = "Такой пользователь уже существует"


class NotValidTimedeltaException(Exception):
    detail = "Дата выаезда не может быть равна или меньше даты въезда"