from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
import json

try:
    from audit.models import AuditLog
except ImportError:
    import sys
    from pathlib import Path
    # 确保能正确导入audit应用
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from audit.models import AuditLog

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    # 跳过审计日志和会话的保存记录
    if sender.__name__ in ['AuditLog', 'Session']:
        return

    action = 'CREATE' if created else 'UPDATE'

    try:
        AuditLog.objects.create(
            user=getattr(instance, '_current_user', None),
            action=action,
            model=sender.__name__,
            object_id=str(instance.pk),
            after_state=json.loads(json.dumps(instance.__dict__, default=str))
        )
    except Exception as e:
        print(f"Failed to create audit log: {e}")

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender.__name__ in ['AuditLog', 'Session']:
        return

    try:
        AuditLog.objects.create(
            user=getattr(instance, '_current_user', None),
            action='DELETE',
            model=sender.__name__,
            object_id=str(instance.pk),
            before_state=json.loads(json.dumps(instance.__dict__, default=str))
        )
    except Exception as e:
        print(f"Failed to create delete audit log: {e}")

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='LOGIN',
        model='User',
        object_id=str(user.pk),
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='LOGOUT',
        model='User',
        object_id=str(user.pk),
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )