# Generated by Django 4.1.3 on 2023-03-30 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_dislike_post_dislikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
    ]
