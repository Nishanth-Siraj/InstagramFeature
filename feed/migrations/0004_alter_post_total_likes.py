# Generated by Django 4.2.7 on 2023-12-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_alter_post_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='total_likes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
