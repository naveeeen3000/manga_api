# Generated by Django 4.0.4 on 2022-06-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_updated_at_mangauser_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangauser',
            name='password',
            field=models.BinaryField(max_length=255),
        ),
    ]
