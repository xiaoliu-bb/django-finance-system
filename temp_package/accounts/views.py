from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .permissions import RolePermissions
from .serializers import UserSerializer, RoleSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class RoleViewSet(viewsets.ModelViewSet):
    queryset = RolePermissions.objects.all()
    serializer_class = RoleSerializer
@login_required
def profile_view(request):
    """用户个人中心页面"""
    return render(request, 'accounts\profile.html')
