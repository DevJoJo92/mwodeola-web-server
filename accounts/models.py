import uuid

from django.db import models
from mwodeola_users.models import MwodeolaUser

ICON_TYPE = [
    (0, 'TEXT'),
    (1, 'IMAGE'),
    (2, 'INSTALLED_APP_LOGO'),
]


# SNS
class SNS(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=20, null=False, blank=False)


# AccountGroup
class AccountGroup(models.Model):
    mwodeola_user = models.ForeignKey(MwodeolaUser, on_delete=models.CASCADE, related_name='mwodeola_user',
                                      null=False, blank=False)
    sns = models.ForeignKey(SNS, on_delete=models.CASCADE, related_name='sns',
                            null=True, blank=False, default=None)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=30, null=False, blank=False)
    app_package_name = models.CharField(max_length=100, null=True, blank=False, default=None)
    web_url = models.CharField(max_length=500, null=True, blank=False, default=None)
    icon_type = models.SmallIntegerField(choices=ICON_TYPE, default=0)
    icon_image_url = models.URLField(null=True, default=None)
    is_favorite = models.BooleanField(null=False, blank=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['mwodeola_user', 'group_name'],
                name='Unique group name for user'
            ),
            models.UniqueConstraint(
                fields=['mwodeola_user', 'sns'],
                name='Unique sns_group name for user'
            )
        ]


# AccountDetail
class AccountDetail(models.Model):
    group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE, related_name='account_group')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, null=False, blank=False)
    user_password = models.CharField(max_length=255, null=False, blank=False)
    user_password_pin = models.CharField(max_length=128, null=True, blank=False, default=None)
    user_password_pattern = models.CharField(max_length=128, null=True, blank=False, default=None)
    memo = models.TextField(default='')

    created_at = models.DateTimeField(auto_now_add=True)
    last_confirmed_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)


# Account
class Account(models.Model):
    own_group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE, related_name='account_own_group')
    sns_group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE, related_name='account_sns_group', null=True)
    detail = models.ForeignKey(AccountDetail, on_delete=models.CASCADE, related_name='account_detail')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['own_group', 'detail'],
                name='Unique detail within group'
            ),
        ]
