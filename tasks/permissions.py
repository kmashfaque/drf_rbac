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




class IsTaskOwner(BasePermission):
    """
    Strict ownership-based access:
    - Normal users can ONLY see tasks they own.
    - Superuser can see ALL tasks.
    - No group check — ownership is the only rule for normal users.
    """
    def has_permission(self, request, view):
        """
        Allow the request to proceed only if user is authenticated.
        The real restriction happens in has_object_permission or queryset filtering.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(f"Checking ownership for user {request.user} on task {obj.id}")
        print(f"Owner: {obj.owner}, Current: {request.user}")
        if request.user.is_superuser:
            print("→ Superuser → allowed")
            return True
        allowed = obj.owner == request.user
        print(f"→ Ownership check result: {allowed}")
        return allowed

class CanMarkCompleted(BasePermission):
    """
    Roles allowed to mark tasks as completed:
    - quality_inspector
    - production_operator
    - planning_head
    """
    allowed_groups = ['quality_inspector', 'production_operator', 'planning head']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True  # superuser always allowed
        return request.user.groups.filter(name__in=self.allowed_groups).exists()

    def has_object_permission(self, request, view, obj):
        # Enforce group check here too — so even for specific objects
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if not request.user.groups.filter(name__in=self.allowed_groups).exists():
            return False


class CanManageTask(BasePermission):
    """
    Full management (create, update, delete, assign):
    - planning_head
    - cutting_supervisor
    - sewing_supervisor
    """
    allowed_groups = ['planning head', 'cutting_supervisor', 'sewing_supervisor',"ie_engineer"]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True  # superuser always allowed
        return request.user.groups.filter(name__in=self.allowed_groups).exists()
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level check: can this user access THIS SPECIFIC task?
        (used for detail/update/delete on /api/tasks/<id>/)
        """
        if request.user.is_superuser:
            return True  # superuser sees everything
        
        # Only owner can access their own task
        return obj.owner == request.user


class IsViewerOnly(BasePermission):
    """
    Read-only access – no edit or complete.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='viewer').exists()
    
