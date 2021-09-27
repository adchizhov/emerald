import argparse
import socket
import sys
import time

from src.conf import settings
from src.log import get_logger

logger = get_logger('app')
parser = argparse.ArgumentParser()

SERVICES_TO_WAIT = ['redis']

parser.add_argument(
    "--service-name",
    help="название сервиса, с которым ожидаем получить успешный коннект",
    required=True,
    choices=SERVICES_TO_WAIT,
)

if __name__ == '__main__':
    arg = parser.parse_args()
    service_name = arg.service_name
    if service_name == 'redis':
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
    else:
        raise ValueError('Неверно выбран сервис который ждем')

    retry_counter = 0
    max_retry_count = 10
    sleep_between_iterations = 5

    while retry_counter <= max_retry_count:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        retry_counter += 1
        logger.info(f'Пытаюсь подключиться к {host}:{port} итерация {retry_counter}...')
        try:
            s.connect((host, port))
            s.close()
            logger.info(f'Успешное подключение к {service_name}')
            sys.exit(0)
        except socket.error as ex:
            time.sleep(sleep_between_iterations)
    sys.exit(1)
