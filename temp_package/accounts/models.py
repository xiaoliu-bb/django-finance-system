from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('ADMIN', _('Administrator')),
        ('FINANCE', _('Finance Staff')),
        ('MANAGER', _('Manager')),
        ('AUDITOR', _('Auditor')),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='FINANCE')
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # 解决冲突：为 groups 和 user_permissions 指定唯一的 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # 修改为唯一名称
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # 修改为唯一名称
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

class PermissionGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField('auth.Permission')

    def __str__(self):
        return self.name

class RoleModels(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.TextField(blank=True)

    def __str__(self):
        return self.name