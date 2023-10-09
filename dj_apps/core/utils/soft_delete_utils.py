from datetime import datetime

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def manual_refresh_from_db(obj):
    """
    Used as a bug workaround: obj.refresh_from_db() does NOT work with safemodel.
    So we're reloading the object from the class manually as a workaround, using the
    safedelete all_objects manager.
    """
    model = apps.get_model(obj._meta.app_label, obj._meta.model_name)
    return model.all_objects.get(pk=obj.pk)


def all_objs_hard_deleted(*objs) -> bool:
    """
    Return True if all given objects are hard deleted.
    """
    for obj in objs:
        try:
            obj = manual_refresh_from_db(obj)
        except ObjectDoesNotExist:
            pass
        else:
            return False

    return True


def all_objs_soft_deleted(*objs) -> bool:
    """
    Return True if all given objects are soft deleted.
    (work with safemodel models only)
    """
    for obj in objs:
        try:
            obj = manual_refresh_from_db(obj)
        except ObjectDoesNotExist:
            return False  # means the object has been hard deleted
        if not obj.id > 0:
            return False
        if not isinstance(obj.deleted, datetime):
            return False

    return True


def all_objs_not_deleted(*objs) -> bool:
    """
    Return True if all given objects are not deleted at all.
    (work with safemodel models only)
    """
    for obj in objs:
        obj = manual_refresh_from_db(obj)
        if not obj.id > 0:
            return False
        if obj.deleted is not None:
            return False

    return True
