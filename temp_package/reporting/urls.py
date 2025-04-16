# reporting/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'report-templates', views.ReportTemplateViewSet, basename='report-template')
router.register(r'financial-reports', views.FinancialReportViewSet, basename='financial-report')

urlpatterns = [
    path('balance-sheet/', views.BalanceSheetView.as_view(), name='balance-sheet'),
    path('income-statement/', views.IncomeStatementView.as_view(), name='income-statement'),
    # 其他报表路径...
] + router.urls