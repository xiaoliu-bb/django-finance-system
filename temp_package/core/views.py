# core/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])  # 允许匿名访问
def api_root(request):
    """系统API入口目录"""
    return Response({
        '账户模块': '/api/accounts/',
        '财务模块': '/api/finance/',
        '报表模块': '/api/reporting/',
        '审计模块': '/api/audit/',
        '系统设置': '/api/system/'
    })