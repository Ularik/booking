from src.utils.utils import DbManager


class BaseService:

    def __init__(self, db: DbManager | None = None):
        self.db = db