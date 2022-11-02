import json
import logging
import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def load_album(album):
    url = 'http://localhost:8000/api/'  # TODO edit url
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, json=album)
    response.raise_for_status()


class Command(BaseCommand):
    help = 'Create albums from json'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'albums.json')

        try:
            with open(path, 'r', encoding='utf-8') as albums_json:
                albums = json.load(albums_json)
        except FileNotFoundError:
            logger.info(f"Отсутствует в корне проекта файл albums.json")
        else:
            for album in albums:
                try:
                    load_album(album)
                    logger.info(f"{album['name']}. Success")
                except HTTPError:
                    logger.info(f"{album['name']}. Ошибка")

    # TODO Add argument to load albums from url
