# system/views.py
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import SystemSetting, FiscalYear
from .serializers import SystemSettingSerializer, FiscalYearSerializer

class SystemSettingViewSet(viewsets.ModelViewSet):
    """
    系统设置CRUD接口
    """
    queryset = SystemSetting.objects.filter(is_active=True)
    serializer_class = SystemSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'key'  # 使用key而非id作为查询参数

    def get_queryset(self):
        queryset = super().get_queryset()
        setting_type = self.request.query_params.get('type')
        if setting_type:
            queryset = queryset.filter(setting_type=setting_type.upper())
        return queryset

class FiscalYearViewSet(viewsets.ModelViewSet):
    """
    财年管理接口
    """
    queryset = FiscalYear.objects.all().order_by('-year')
    serializer_class = FiscalYearSerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrentFiscalYearView(generics.RetrieveAPIView):
    """
    获取当前财年
    """
    serializer_class = FiscalYearSerializer

    def get_object(self):
        return FiscalYear.objects.filter(is_current=True).first()

class SettingsByTypeView(generics.ListAPIView):
    """
    按类型获取系统设置
    """
    serializer_class = SystemSettingSerializer

    def get_queryset(self):
        setting_type = self.kwargs['setting_type'].upper()
        return SystemSetting.objects.filter(
            setting_type=setting_type,
            is_active=True
        )
