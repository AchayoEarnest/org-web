from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("admin", "staff")

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ("admin", "staff"):
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "author", None)
        return owner == request.user

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class DocumentAccessPermission(BasePermission):
    ACCESS_HIERARCHY = {"public": 0, "members": 1, "staff": 2, "admin": 3}
    ROLE_LEVEL = {"member": 1, "staff": 2, "admin": 3}

    def has_object_permission(self, request, view, obj):
        if obj.access_level == "public":
            return True
        if not request.user.is_authenticated:
            return False
        user_level = self.ROLE_LEVEL.get(request.user.role, 0)
        req_level = self.ACCESS_HIERARCHY.get(obj.access_level, 99)
        return user_level >= req_level
