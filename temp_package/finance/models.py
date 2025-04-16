from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class AccountCategory(models.Model):
    CATEGORY_TYPES = (
        ('INCOME', _('Income')),
        ('EXPENSE', _('Expense')),
        ('ASSET', _('Asset')),
        ('LIABILITY', _('Liability')),
        ('EQUITY', _('Equity')),
    )

    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    entry_date = models.DateField()
    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_entries')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.reference} - {self.entry_date}"

class JournalItem(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(AccountCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    debit_credit = models.CharField(max_length=1, choices=(('D', 'Debit'), ('C', 'Credit')))
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.entry.reference} - {self.account.name}"

class Invoice(models.Model):
    INVOICE_TYPES = (
        ('SALE', _('Sale')),
        ('PURCHASE', _('Purchase')),
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES)
    date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    related_entry = models.ForeignKey(JournalEntry, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.get_invoice_type_display()}"

class Budget(models.Model):
    BUDGET_STATUS = (
        ('DRAFT', _('Draft')),
        ('SUBMITTED', _('Submitted')),
        ('APPROVED', _('Approved')),
        ('REJECTED', _('Rejected')),
    )

    name = models.CharField(max_length=100)
    fiscal_year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=BUDGET_STATUS, default='DRAFT')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_budgets')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_budgets')
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.fiscal_year})"

class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(AccountCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    q1_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    q2_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    q3_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    q4_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.budget.name} - {self.account.name}"