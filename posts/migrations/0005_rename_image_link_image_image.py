# Generated by Django 4.1 on 2023-06-02 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_image_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_link',
            new_name='image',
        ),
    ]