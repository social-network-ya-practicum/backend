from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Подразделение'),
        ),
    ]
