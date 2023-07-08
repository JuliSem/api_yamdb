import csv
import os
from django.core.management.base import BaseCommand
from api_yamdb.settings import CSV_FILES_DIR

from reviews.models import (
    Category,
    Genre,
    GenreTitle,
    Review,
    Comment,
    Title
)
from users.models import User

def import_user():
    csv_path = os.path.join(CSV_FILES_DIR, 'users.csv')
   
    with open(csv_path) as csvfile:
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

def import_genge():
    csv_path = os.path.join(CSV_FILES_DIR, 'genre.csv')

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                slug=row['slug'],
                name=row['name'],
            )

def import_category():
    csv_path = os.path.join(CSV_FILES_DIR, 'category.csv')

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                slug=row['slug'],
                name=row['name'],
            )

def import_title():
    csv_path = os.path.join(CSV_FILES_DIR, 'titles.csv')

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.filter(id=row['category']).first(),
            )

def import_genre_title():
    csv_path = os.path.join(CSV_FILES_DIR, 'genre_title.csv')

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            GenreTitle.objects.create(
                id=row['id'],
                genre=Genre.objects.filter(id=row['genre_id']).first(),
                title=Title.objects.filter(id=row['title_id']).first(),
            )

def import_genre_title():
    csv_path = os.path.join(CSV_FILES_DIR, 'genre_title.csv')

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            GenreTitle.objects.create(
                id=row['id'],
                genre=Genre.objects.filter(id=row['genre_id']).first(),
                title=Title.objects.filter(id=row['title_id']).first(),
            )

def import_review():
    csv_path = os.path.join(CSV_FILES_DIR, 'review.csv')

    with open(csv_path) as csvfile:
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

def import_comment():
    csv_path = os.path.join(CSV_FILES_DIR, 'comments.csv')

    with open(csv_path) as csvfile:
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
        import_user()
        import_genge()
        import_category()
        import_title()
        import_genre_title()
        import_review()
        import_comment()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))