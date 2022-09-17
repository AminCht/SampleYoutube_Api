from rest_framework import permissions

from app.models import AppUser


class HistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            (user, created) = AppUser.objects.get_or_create(user_id=request.user.id)
            if user.MEMBERSHIP_STATUS == 'P':
                return True
            return False