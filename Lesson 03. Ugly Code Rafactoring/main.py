import logging

import app
from ThreadsManager import ThreadsManager
from AppConfig import AppConfig
from consumers import *

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    manager = ThreadsManager()

    manager.add(ConsumerOne(
        queue_name='queue_one',
        connection_params=AppConfig.RABBITMQ_CONNECTION_PARAMS,
        database_connection=app.create_new_dn_conn()
    ))

    manager.add(ConsumerTwo(
        queue_name='queue_two',
        connection_params=AppConfig.RABBITMQ_CONNECTION_PARAMS,
        database_connection=app.create_new_dn_conn()
    ))

    try:
        manager.run_all()
    except KeyboardInterrupt:
        manager.stop_all()


if __name__ == '__main__':
    main()
