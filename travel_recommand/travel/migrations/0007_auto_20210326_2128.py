# Generated by Django 3.1.5 on 2021-03-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20210326_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_image',
            name='image_of_place',
            field=models.ImageField(upload_to=''),
        ),
    ]
