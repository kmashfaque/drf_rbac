# tasks/permissions.py
from rest_framework.permissions import BasePermission
from accounts.permissions import IsAdmin  # assuming this exists

class IsAdminOrOwner(BasePermission):
    """
    Module-specific object-level rule: admin or owner can access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or IsAdmin().has_permission(request, view):
            return True
        return obj.owner == request.user


class CanViewTask(BasePermission):
    """
    Any authenticated user can view tasks.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return True  # everyone can see any task (customize later if needed)


class CanMarkCompleted(BasePermission):
    """
    Roles allowed to mark tasks as completed:
    - quality_inspector
    - production_operator
    - planning_head
    """
    allowed_groups = ['quality_inspector', 'production_operator', 'planning_head']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True  # superuser always allowed
        return request.user.groups.filter(name__in=self.allowed_groups).exists()

    def has_object_permission(self, request, view, obj):
        # Optional: restrict by department
        if request.user.department and obj.department:
            return request.user.department == obj.department
        return True


class CanManageTask(BasePermission):
    """
    Full management (create, update, delete, assign):
    - planning_head
    - cutting_supervisor
    - sewing_supervisor
    """
    allowed_groups = ['planning_head', 'cutting_supervisor', 'sewing_supervisor',"ie_engineer"]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True  # superuser always allowed
        return request.user.groups.filter(name__in=self.allowed_groups).exists()


class IsViewerOnly(BasePermission):
    """
    Read-only access – no edit or complete.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='viewer').exists()