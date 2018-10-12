from AppConfig import AppConfig
from app_package.SQLiteDbConnection import SQLiteDbConnection


class AppLoader:

    @classmethod
    def init_db(cls):
        return SQLiteDbConnection(AppConfig.DB_PATH)
