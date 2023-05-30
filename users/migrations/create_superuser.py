import os

from django.contrib.auth import get_user_model
from django.db import migrations
from dotenv import load_dotenv


def create_superuser(apps, schema_editor):

    load_dotenv()

    CustomUser = get_user_model()

    CustomUser.objects.create_superuser(
        email=os.getenv("SU_EMAIL"),
        first_name=os.getenv("SU_FIRST_NAME"),
        last_name=os.getenv("SU_LAST_NAME"),
        middle_name=os.getenv("SU_MIDDLE_NAME"),
        phone_number=os.getenv("SU_PHONE_NUMBER"),
        birthday_date=os.getenv("SU_BIRTHDAY_DATE"),
        password=os.getenv("SU_PASSWORD"), 
        is_active=True, is_staff=True
    )
    print(f'Superuser {os.getenv("SU_EMAIL")} is created.')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
