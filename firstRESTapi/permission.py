
from rest_framework import permissions


class AlreadyAuthenticated(permissions.BasePermission):
    message = "Sorry You are already authenticated"

    def has_permission(self, request, *args, **kwargs):
        print("Hello all")
        return not request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "You dont have permission to access this object"
    # print("Yes i am inside")

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(obj)
        print("inside Permissions")
        if request.method in permissions.SAFE_METHODS:
            return True
        # print(obj.objectOwner())
        print(request.user)
        # Instance must have an attribute named `owner`.
        return obj.Owner == request.user
