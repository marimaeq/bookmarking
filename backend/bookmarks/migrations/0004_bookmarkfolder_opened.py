# Generated by Django 3.2.18 on 2023-04-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_bookmark_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarkfolder',
            name='opened',
            field=models.BooleanField(default=False),
        ),
    ]
