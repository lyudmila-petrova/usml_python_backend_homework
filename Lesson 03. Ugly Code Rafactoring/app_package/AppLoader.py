from AppConfig import AppConfig
from app_package.SQLiteDbConnection import SQLiteDbConnection
from lib.mailer.NullMailer import NullMailer
from lib.mailer.SMTPMailer import SMTPMailer


class AppLoader:

    @staticmethod
    def init_db():
        return SQLiteDbConnection(AppConfig.DB_PATH)

    @staticmethod
    def init_mailer():

        if AppConfig.DEV:
            return NullMailer()
        else:
            return SMTPMailer(email_from=AppConfig.SITE_MAIL, smtp_host=AppConfig.SMTP_HOST)
