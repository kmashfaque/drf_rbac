from rest_framework.permissions import BasePermission
from accounts.permissions import IsAdmin

class IsAdminOrOwner(BasePermission):
    "Module Specific  object level rule"
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True
        return obj.owner == request.user
    

class CanViewTask(BasePermission):
    "anyone authenticated can view tasks"
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return True # everyone can see any task (or restrict later)
    

    
class CanMarkCompleted(BasePermission):
    """
    Roles that can mark tasks as completed:
    - quality_inspector
    - production_operator
    - planning_head
    """
    allowed_groups = ['quality_inspector', 'production_operator', 'planning_head']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name__in=self.allowed_groups).exists()
    
    def has_object_permission(self, request, view, obj):
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
    allowed_groups = ['planning_head', 'cutting_supervisor', 'sewing_supervisor']

    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=self.allowed_groups).exists()
    

class IsViewerOnly(BasePermission):
    """Only view – no edit/complete"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='viewer').exists()
    