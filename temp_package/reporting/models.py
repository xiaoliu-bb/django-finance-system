from django.db import models
from django.utils.translation import gettext_lazy as _
from finance.models import AccountCategory

class FinancialReport(models.Model):
    REPORT_TYPES = (
        ('BALANCE', _('Balance Sheet')),
        ('INCOME', _('Income Statement')),
        ('CASHFLOW', _('Cash Flow Statement')),
    )

    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    report_data = models.JSONField()

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.start_date} - {self.end_date})"

class ReportTemplate(models.Model):
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=10, choices=FinancialReport.REPORT_TYPES)
    template_data = models.JSONField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name