

def get_params(function_info, args, kwargs):
    # Collect args and kwargs as one kwargs
    params = {
        **dict(zip(function_info["args_name"], args)),
        **kwargs
    }
    # Remove the arguments to ignore if present
    for arg in function_info["args_to_ignore"]:
        params.pop(arg, None)

    # if it's a method we don't want to serialize the instance
    params.pop("self", None)

    return params