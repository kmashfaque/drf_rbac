from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    "Global role check -reusable across all modules"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='admin').exists()
    
from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        print("===== DEBUG: IsManagerOrAdmin.has_permission() running =====")
        print("Request user:", request.user)
        print("Is authenticated?", request.user.is_authenticated)
        print("User ID:", request.user.id if request.user.is_authenticated else "anonymous")
        
        if not request.user.is_authenticated:
            print("→ Not authenticated → returning False")
            return False

        # This is the critical line — let's debug it
        groups_qs = request.user.groups.filter(name__in=['admin', 'manager'])
        matching_groups = list(groups_qs.values_list('name', flat=True))
        
        print("QuerySet of matching groups:", groups_qs)
        print("Matching group names:", matching_groups)
        print("Has admin or manager group?", bool(matching_groups))
        
        return bool(matching_groups)