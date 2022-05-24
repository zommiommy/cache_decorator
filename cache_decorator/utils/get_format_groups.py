from typing import Dict, Any, List, Set

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
