from django.db import models
from django.contrib.auth.models import AbstractUser

class RolePermissions(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('FINANCE', 'Finance Staff'),
        ('MANAGER', 'Manager'),
        ('AUDITOR', 'Auditor'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='role_permissions'
    )

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()

