# Generated by Django 3.0.6 on 2021-03-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_auto_20210327_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_input',
            name='status',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]