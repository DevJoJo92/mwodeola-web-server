# Generated by Django 4.0.1 on 2022-03-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_accountgroup_unique group name for user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='user_id',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='accountdetail',
            name='user_password',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
