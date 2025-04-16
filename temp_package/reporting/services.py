from datetime import date
from django.db.models import Sum
from finance.models import JournalItem, AccountCategory

class ReportGenerator:
    @staticmethod
    def generate_balance_sheet(start_date, end_date):
        # 获取资产、负债和所有者权益账户
        asset_accounts = AccountCategory.objects.filter(category_type='ASSET')
        liability_accounts = AccountCategory.objects.filter(category_type='LIABILITY')
        equity_accounts = AccountCategory.objects.filter(category_type='EQUITY')

        # 计算资产总额
        assets = []
        total_assets = 0
        for account in asset_accounts:
            balance = JournalItem.objects.filter(
                account=account,
                entry__entry_date__range=(start_date, end_date)
            ).aggregate(
                balance=Sum('amount')
            )['balance'] or 0
            assets.append({
                'account': account.name,
                'balance': balance
            })
            total_assets += balance

        # 计算负债总额
        liabilities = []
        total_liabilities = 0
        for account in liability_accounts:
            balance = JournalItem.objects.filter(
                account=account,
                entry__entry_date__range=(start_date, end_date)
            ).aggregate(
                balance=Sum('amount')
            )['balance'] or 0
            liabilities.append({
                'account': account.name,
                'balance': balance
            })
            total_liabilities += balance

        # 计算所有者权益总额
        equity = []
        total_equity = 0
        for account in equity_accounts:
            balance = JournalItem.objects.filter(
                account=account,
                entry__entry_date__range=(start_date, end_date)
            ).aggregate(
                balance=Sum('amount')
            )['balance'] or 0
            equity.append({
                'account': account.name,
                'balance': balance
            })
            total_equity += balance

        return {
            'report_type': 'BALANCE',
            'start_date': start_date,
            'end_date': end_date,
            'assets': assets,
            'total_assets': total_assets,
            'liabilities': liabilities,
            'total_liabilities': total_liabilities,
            'equity': equity,
            'total_equity': total_equity,
            'liabilities_and_equity': total_liabilities + total_equity
        }


class ReportGenerator:
    @staticmethod
    def generate_income_statement(start_date, end_date):
        revenue_accounts = AccountCategory.objects.filter(category_type='REVENUE')
        expense_accounts = AccountCategory.objects.filter(category_type='EXPENSE')

        # 计算总收入
        revenues = []
        total_revenue = 0
        for account in revenue_accounts:
            balance = JournalItem.objects.filter(
                account=account,
                entry__entry_date__range=(start_date, end_date)
            ).aggregate(balance=Sum('amount'))['balance'] or 0
            revenues.append({'account': account.name, 'balance': balance})
            total_revenue += balance

        # 计算总支出（同理实现）
        # ...

        return {
            'report_type': 'INCOME',
            'start_date': start_date,
            'end_date': end_date,
            'revenues': revenues,
            'total_revenue': total_revenue,
            # 其他字段...
        }