from rest_framework.permissions import BasePermission
from accounts.permissions import IsAdmin

class IsAdminOrOwner(BasePermission):
    "Module Specific  object level rule"
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True
        return obj.owner == request.user