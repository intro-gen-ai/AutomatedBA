def get_instance(module, class_name):
    return getattr(module, class_name)()