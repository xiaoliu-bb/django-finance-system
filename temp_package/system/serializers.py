# system/serializers.py
from rest_framework import serializers
from .models import SystemSetting, FiscalYear

class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ['key', 'name', 'value', 'setting_type', 'description', 'is_active']
        extra_kwargs = {
            'key': {'validators': []}  # 禁用key的唯一性验证（更新时需允许）
        }

class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalYear
        fields = ['id', 'year', 'start_date', 'end_date', 'is_current']