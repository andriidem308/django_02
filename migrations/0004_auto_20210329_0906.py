# Generated by Django 3.1.7 on 2021-03-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210328_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Заголовок поста'),
        ),
    ]
