# reporting/serializers.py
from rest_framework import serializers
from .models import FinancialReport, ReportTemplate

class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = '__all__'
        read_only_fields = ('generated_at', 'generated_by')

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'