from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import RoleModels

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModels
        fields = '__all__'

# 获取自定义用户模型（已在settings.py中配置为AUTH_USER_MODEL）
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)  # 显示角色名称而非值

    class Meta:
        model = User
        fields = [
            '用户编号',
            '用户名称',
            '邮件',
            'is_staff',
            '角色',          # 新增角色字段
            '部门',    # 新增部门字段
            '电话'          # 新增电话字段
        ]