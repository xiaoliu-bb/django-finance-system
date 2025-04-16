# audit/views.py
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API端点：查询所有审计日志（仅读）
    """
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 支持按用户、动作类型、模型过滤
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        action = self.request.query_params.get('action')
        model = self.request.query_params.get('model')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if action:
            queryset = queryset.filter(action=action.upper())
        if model:
            queryset = queryset.filter(model__iexact=model)
        return queryset

class UserLoginHistoryView(generics.ListAPIView):
    """
    获取指定用户的登录历史
    """
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', self.request.user.id)
        return AuditLog.objects.filter(
            user_id=user_id, 
            action='LOGIN'
        ).order_by('-timestamp')

class ModelChangeListView(generics.ListAPIView):
    """
    获取指定模型的所有变更记录
    """
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        return AuditLog.objects.filter(
            model__iexact=model_name
        ).exclude(action__in=['LOGIN', 'LOGOUT']).order_by('-timestamp')