# Generated by Django 4.0.1 on 2022-03-28 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_user_password_pin_accountdetail_user_password_pin4_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='memo',
            field=models.TextField(default=None, max_length=2000, null=True),
        ),
    ]