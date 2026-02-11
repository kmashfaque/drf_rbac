# core/admin.py  (or accounts/admin.py — whichever app has CustomUser & Department)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Department


# Register Department with a clean admin interface
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


# Custom admin for CustomUser — makes group assignment easy
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Main fields to show in list view
    list_display = (
        'email',
        'username',
        'department',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    )
    
    # Filters on the right sidebar
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'department',
        'groups',           # ← very important: filter by group
    )
    
    # Search in these fields
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # Order by most recent
    ordering = ('-date_joined',)
    
    # Fieldsets in edit form — make groups easy to manage
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone', 'is_verified')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',             # ← this is the key field for existing groups
                'user_permissions',
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Department', {'fields': ('department',)}),
    )
    
    # When adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'department'),
        }),
    )
    
    # Show many-to-many fields nicely (groups & permissions)
    filter_horizontal = ('groups', 'user_permissions',)
    
    # Make email the main identifier
    readonly_fields = ('last_login', 'date_joined')


# Optional: make Group admin nicer (so you see users per group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count')
    search_fields = ('name',)
    
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = "Number of users"

# Unregister default Group admin and use our custom one
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)