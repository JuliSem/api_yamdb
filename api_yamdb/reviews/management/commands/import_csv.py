import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import (
    Category,
    Genre,
    Review,
    Comment,
    Title
)
from users.models import User

FILES = (
    'users',
    'genre',
    'category',
    'titles',
    'genre_title',
    'review',
    'comments'
)


def import_users(csv_path):
    if User.objects.exists():
        print('Данные для User уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )


def import_genre(csv_path):
    if Genre.objects.exists():
        print('Данные для Genre уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    slug=row['slug'],
                    name=row['name'],
                )


def import_category(csv_path):
    if Category.objects.exists():
        print('Данные для Category уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    slug=row['slug'],
                    name=row['name'],
                )


def import_titles(csv_path):
    if Title.objects.exists():
        print('Данные для Title уже загружены')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.filter(
                        id=row['category']
                    ).first(),
                )


def import_genre_title(csv_path):
    if Title.objects.exists():
        print('Данные для Genre title уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(id=row['title_id']),
                title = title[0]
                title.genre.add(row['genre_id'])


def import_review(csv_path):
    if Review.objects.exists():
        print('Данные для Review уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title=Title.objects.filter(id=row['title_id']).first(),
                    text=row['text'],
                    author=User.objects.filter(id=row['author']).first(),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )


def import_comments(csv_path):
    if Comment.objects.exists():
        print('Данные для Comment уже загружены!')
    else:
        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review=Review.objects.filter(id=row['review_id']).first(),
                    text=row['text'],
                    author=User.objects.filter(id=row['author']).first(),
                    pub_date=row['pub_date'],
                )


class Command(BaseCommand):
    help = 'Imports data from a CSV file into the YourModel model'

    def handle(self, *args, **options):
        for file in FILES:
            csv_path = f'{settings.BASE_DIR}/static/data/{file}.csv'
            eval(f'import_{file}(r"{csv_path}")')

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
