# audit/serializers.py
from rest_framework import serializers
from .models import AuditLog
from accounts.serializers import UserSerializer  # 假设存在简化用户序列化器

class AuditLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 嵌套用户信息

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'action', 'model',
            'object_id', 'timestamp', 'ip_address',
            'before_state', 'after_state'
        ]
        read_only_fields = fields