# Generated by Django 4.0.1 on 2022-02-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
