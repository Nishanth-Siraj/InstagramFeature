# Generated by Django 4.2.7 on 2023-12-02 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
