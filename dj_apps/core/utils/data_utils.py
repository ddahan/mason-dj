def is_attr_identical(obj, attr: str) -> bool:
    """
    Return True if a given object is currently the same in database, for the given
    attribute.
    """
    in_db_obj = obj._meta.model.objects.get(pk=obj.pk)
    return getattr(in_db_obj, attr) == getattr(obj, attr)
