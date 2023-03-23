from rest_framework.permissions import BasePermission
from .models import Coordinator


class IsCoordinator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            coordinator = Coordinator.objects.get(user=user)
            return True
        except Coordinator.DoesNotExist:
            return False
