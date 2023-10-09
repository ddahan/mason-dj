from django.conf import settings

##########################################################################################
# Database Decorators
##########################################################################################


def annotate_to_property(queryset_method_name, key_name):
    """
    allow an annotated attribute to be used as property.
    Adapted to work with secret ids (not classic pks)
    """
    from django.apps import apps

    def decorator(func):
        def inner(self):
            attr = "_" + key_name
            if not hasattr(self, attr):
                klass = apps.get_model(self._meta.app_label, self._meta.object_name)
                to_eval = (
                    f"klass.objects.{queryset_method_name}().get(id='{self.id}').{attr}"
                )
                value = eval(to_eval, {"klass": klass})
                setattr(self, attr, value)

            return getattr(self, attr)

        return property(inner)

    return decorator


##########################################################################################
# Environment Decorators
##########################################################################################


class ForbiddenEnvironment(PermissionError):
    pass


def accepted_environments(*envs):
    """
    The decorated function can be executed only in specified envs
    """

    def my_decorator(func_to_be_decorated):
        def wrapper(*args, **kwargs):
            if settings.ENV_NAME not in envs:
                raise ForbiddenEnvironment
            return func_to_be_decorated(*args, **kwargs)

        return wrapper

    return my_decorator


def excluded_environments(*envs):
    """
    The decorated function can NOT be executed in specified envs
    NOTE: if ENV_NAME is not set, it won't raise any error
    """

    def my_decorator(func_to_be_decorated):
        def wrapper(*args, **kwargs):
            if settings.ENV_NAME in envs:
                raise ForbiddenEnvironment
            return func_to_be_decorated(*args, **kwargs)

        return wrapper

    return my_decorator
