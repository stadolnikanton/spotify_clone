from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        print(request, "Вот тут отработало всё")
        return False


class IsClient(BasePermission):
    def has_permission(self, request, view):
        # return request.user.groups.filter(name="Client").exists()
        print(request, "тут не должно отрабатывать")
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        print(request, "тут не должно отрабатывать")
        return request.user.groups.filter(name="Moderator").exists()
