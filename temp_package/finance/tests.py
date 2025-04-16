from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AccountCategory, JournalEntry

User = get_user_model()


class FinanceModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='FINANCE'
        )

        self.account = AccountCategory.objects.create(
            name='Test Account',
            category_type='EXPENSE',
            code='5000'
        )

    def test_account_creation(self):
        self.assertEqual(self.account.name, 'Test Account')
        self.assertEqual(self.account.category_type, 'EXPENSE')

    def test_journal_entry_creation(self):
        entry = JournalEntry.objects.create(
            entry_date='2023-01-01',
            reference='TEST-001',
            description='Test entry',
            created_by=self.user
        )
        self.assertEqual(entry.reference, 'TEST-001')
        self.assertEqual(entry.created_by.username, 'testuser')
