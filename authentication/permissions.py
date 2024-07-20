from .exceptions import BadRequestException


def is_has_permission(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_verified and request.user.role == 2:
            return func(request, *args, **kwargs)
        raise BadRequestException('You dont have permission for this action!')
