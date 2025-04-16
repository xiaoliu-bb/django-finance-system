from django.db import models
from django.utils.translation import gettext_lazy as _

class SystemSetting(models.Model):
    SETTING_TYPES = (
        ('FINANCIAL', _('Financial')),
        ('SYSTEM', _('System')),
        ('NOTIFICATION', _('Notification')),
    )

    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    value = models.JSONField()
    setting_type = models.CharField(max_length=15, choices=SETTING_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FiscalYear(models.Model):
    year = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_current:
            # 确保只有一个当前财年
            FiscalYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"FY {self.year}"