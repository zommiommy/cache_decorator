

def get_params(function_info, args, kwargs):
    params = {}

    # add args default
    if function_info["defaults"]:
        for arg, default in zip(reversed(function_info["args"]), reversed(function_info["defaults"])):
            params[arg] = default

    # Add kwonly defaults
    params.update(function_info["kwonlydefaults"])

    # Collect args and kwargs as one kwargs
    args_and_kwargs = {
        **dict(zip(function_info["args"], args)),
        **kwargs
    }
    params.update(args_and_kwargs)

    # Remove the arguments to ignore if present
    for arg in function_info["args_to_ignore"]:
        params.pop(arg, None)

    return params