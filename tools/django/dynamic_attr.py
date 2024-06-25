def get_dynamic_attr(object, name, default=None):
    related_names = name.split("__")
    obj = object
    for index, related_name in enumerate(related_names):
        obj = getattr(obj, related_name, None)
        if callable(obj):
            obj = obj()
        if obj is None:
            break

    if obj is None:
        return default
    return obj
