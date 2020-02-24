

def get_args_to_hash(args_name, args, kwargs, args_to_ignore):
    # Collect args and kwargs as one kwargs
    to_hash = {
        **dict(zip(args_name, args)),
        **kwargs
    }
    # Remove the arguments to ignore if present
    for arg in args_to_ignore:
        to_hash.pop(arg, None)

    return to_hash