from AppConfig import AppConfig
from app_package.SQLiteDbConnection import SQLiteDbConnection


class AppLoader:
    @staticmethod
    def init_db():
        return SQLiteDbConnection(AppConfig.DB_PATH)
