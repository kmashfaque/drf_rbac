from django.core.exceptions import PermissionDenied
from .models import Task

def create_task(validated_data, user):
    "business rules + workflow"
    "# Example cross-module check (could call accounts service)"
    # if user.groups.filter(name__in=['admin', 'manager', 'ie_engineer', 'planning head']).exists():
    task =Task.objects.create(**validated_data, owner=user)
        # e.g. send notification, log audit, etc.
    return task
    # raise PermissionDenied("insuifficient role to create task")

def get_user_tasks(user):
    "Wrokflow Logic: admin sees all, others see own"
    if user.groups.filter(name='admin').exists():
        return Task.objects.all()
    return Task.objects.filter(owner=user)

