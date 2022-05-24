from typing import Dict, Any, List, Set
from .backends import Backend

# Dictionary are not hashable and the python hash is not consistent
# between runs so we have to use an external dictionary hashing package
# else we will not be able to load the saved caches.
from dict_hash import sha256

def get_format_groups(path_fmt: str) -> List[str]:
    """Given a format string extract the name of the values to substitute."""
    groups = []
    previous_was_open_curly_brace = False
    is_capture_group = False
    capture = ""
    for c in path_fmt:
        if c == "{" and not previous_was_open_curly_brace:
            previous_was_open_curly_brace = True
            is_capture_group = True
        elif c == "{" and previous_was_open_curly_brace:
            previous_was_open_curly_brace = False
            is_capture_group = False
        elif c == "}":
            previous_was_open_curly_brace = False
            is_capture_group = False
            if capture.strip() != "":
                groups.append(capture)
            capture = ""
        else:
            previous_was_open_curly_brace = False
            if not is_capture_group:
                continue

            capture += c
    return groups


class PathFormatter:
    def __init__(self, function_info: Dict[str, Any], params: Dict[str, Any], cache_dir: str):
        self.function_info = function_info
        self.params = params
        self.cache_dir = cache_dir
        self._hash = None

    def validate_path(self, path_fmt: str, extra_args_names: Set[str]):
        groups = get_format_groups(path_fmt)

        # Compute all the values we can insert in the  formatting
        available_keys = set(self.function_info.keys()) \
            | set(self.params.keys()) \
            | {"_hash"} \
            | {"cache_dir"} \
            | extra_args_names

        for group in groups:
            if group not in available_keys:
                raise ValueError((
                    "The given path `{}` contains the format group `{}` which "
                    "is not one of the available ones: {}"
                ).format(
                    path_fmt, group, list(sorted(available_keys))
                ))

        # Check that given all the wanted groups, the path is actually formattable
        dummy_args = {
            group: ""
            for group in groups
        }
        try:
            path_fmt.format(**dummy_args)
        except ValueError:
            raise ValueError((
                "The given path '{}' has all the right groups but has some "
                "spurious curly braces and thus it can't be formatted."
            ).format(
                path_fmt
            ))
        # check that the format is serializable
        # THIS DOES NOT ALLOWS FOR THE EXTENSION TO BE THE RESULT OF THE FORMATTING!!!!
        if not Backend().support_path(path_fmt):
            raise ValueError((
                "The given path `{}` is not serializable with the current backend. "
                "The available extensions are: {}"
            ).format(
                path_fmt,
                Backend().get_supported_extensions()
            ))

        
    def format_path(self, path_fmt:str, extra_args: Dict[str, Any]) -> str:

        # Compute the hash if needed (and not already done)
        if "{_hash}" in path_fmt and self._hash is None:
            self._hash = sha256({"params": self.params, "function_info": self.function_info})

        return path_fmt.format(
            **self.function_info,
            **self.params,
            **extra_args,
            _hash=self._hash,
            cache_dir=self.cache_dir,
        )