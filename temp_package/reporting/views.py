# reporting/views.py
from datetime import date

from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import FinancialReport, ReportTemplate
from .serializers import FinancialReportSerializer, ReportTemplateSerializer
from .services import ReportGenerator

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

class BalanceSheetView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date', date.today().replace(month=1, day=1))
        end_date = request.query_params.get('end_date', date.today())
        report_data = ReportGenerator.generate_balance_sheet(start_date, end_date)
        return Response(report_data)


class IncomeStatementView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date', date.today().replace(month=1, day=1))
        end_date = request.query_params.get('end_date', date.today())

        # 调用服务层生成利润表数据（需在 services.py 中实现）
        report_data = ReportGenerator.generate_income_statement(start_date, end_date)
        return Response(report_data)