#!-*-coding:utf-8-*-
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api_yamdb.reviews.models import Review


class Command(BaseCommand):
    help = 'The Zen of Python'

    def _create_users(self):
        reader = ...
        objs = []
        for row in reader:
            objs.append(User(**row))

        # Создание множества объектов одним запросом.
        User.objects.bulk_create(objs=objs)

    def _create_titles(self):
        ...

    def _create_reviews(self):
        reader = ...
        objs = []
        for row in reader:
            # FK получаем из строки title=row['title_id'],
            # чтобы минимизировать
            # кол-во обращений к БД.
            objs.append(
                Review(**row)
            )

        User.objects.bulk_create(objs=objs)

    def handle(self, *args, **options):
        self._create_users()
        self._create_titles()
        self._create_reviews()
