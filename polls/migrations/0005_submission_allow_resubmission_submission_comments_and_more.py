# Generated by Django 4.2.15 on 2024-09-18 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_homework_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='allow_resubmission',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
