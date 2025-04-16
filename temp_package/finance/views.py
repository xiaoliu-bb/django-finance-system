from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import JournalEntry, JournalItem, Invoice, AccountCategory
from .serializers import (
    JournalEntrySerializer,
    JournalItemSerializer,
    InvoiceSerializer,
    AccountCategorySerializer
)
from .models import Budget, BudgetItem
from .serializers import BudgetSerializer, BudgetItemSerializer

class AccountCategoryViewSet(viewsets.ModelViewSet):
    queryset = AccountCategory.objects.all()
    serializer_class = AccountCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category_type', 'parent']
    search_fields = ['name', 'code']

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all().order_by('-entry_date')
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['entry_date', 'created_by', 'approved_by']
    search_fields = ['reference', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JournalItemViewSet(viewsets.ModelViewSet):
    queryset = JournalItem.objects.all()
    serializer_class = JournalItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['entry', 'account', 'debit_credit']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-date')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['invoice_type', 'date', 'is_paid']
    search_fields = ['invoice_number', 'description']

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().order_by('-fiscal_year')
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['fiscal_year', 'status']
    search_fields = ['name', 'notes']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BudgetItemViewSet(viewsets.ModelViewSet):
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['budget', 'account']


class FinanceReportsView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 可选权限控制

    def get(self, request):
        # 示例：聚合财务数据
        entries = JournalEntry.objects.all()
        invoices = Invoice.objects.all()

        # 使用序列化器（需提前定义）
        entry_serializer = JournalEntrySerializer(entries, many=True)
        invoice_serializer = InvoiceSerializer(invoices, many=True)

        return Response({
            "journal_entries": entry_serializer.data,
            "invoices": invoice_serializer.data
        })