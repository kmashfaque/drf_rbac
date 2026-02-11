from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Global role check - reusable across all modules.
    Allows superusers + users in 'admin' group.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            print("DEBUG: IsAdmin - superuser detected → allowed")
            return True
        
        has_admin = request.user.groups.filter(name='admin').exists()
        print(f"DEBUG: IsAdmin - user '{request.user}' has 'admin' group? {has_admin}")
        return has_admin


class IsManagerOrAdmin(BasePermission):
    """
    Allows superusers + users in 'admin' or 'manager' group.
    """
    def has_permission(self, request, view):
        print("===== DEBUG: IsManagerOrAdmin.has_permission() running =====")
        print(f"Request user: {request.user}")
        print(f"Is authenticated? {request.user.is_authenticated}")
        print(f"Is superuser? {request.user.is_superuser}")
        print(f"User ID: {request.user.id if request.user.is_authenticated else 'anonymous'}")
        
        if not request.user.is_authenticated:
            print("→ Not authenticated → returning False")
            return False

        # Superuser always allowed - most important fix
        if request.user.is_superuser:
            print("→ Superuser detected → returning True")
            return True
        
        # Check groups
        groups_qs = request.user.groups.filter(name__in=['admin', 'manager'])
        matching_groups = list(groups_qs.values_list('name', flat=True))
        
        print("QuerySet of matching groups:", groups_qs)
        print("Matching group names:", matching_groups)
        print(f"Has admin or manager group? {bool(matching_groups)}")
        
        return bool(matching_groups)