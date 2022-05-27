from typing import List, Optional, Tuple

class MatchGroup:
    def __init__(self, str_match: str, start: int, end: int):
        self.str_match, *self.extra_settings = str_match.split(":")
        self.start = start
        self.end = end

def get_format_groups(path_fmt: str) -> List[MatchGroup]:
    """Given a format string extract the name of the values to substitute."""
    groups = []
    previous_was_open_curly_brace = False
    is_capture_group = False
    start_index = 0
    capture = ""
    for i, c in enumerate(path_fmt):
        if c == "{" and not previous_was_open_curly_brace:
            previous_was_open_curly_brace = True
            is_capture_group = True
            start_index = i
        elif c == "{" and previous_was_open_curly_brace:
            previous_was_open_curly_brace = False
            is_capture_group = False
        elif c == "}":
            previous_was_open_curly_brace = False
            is_capture_group = False
            if capture.strip() != "":
                groups.append(MatchGroup(capture, start_index, i + 1))
            capture = ""
        else:
            previous_was_open_curly_brace = False
            if not is_capture_group:
                continue

            capture += c
    return groups

def get_next_format_group(path_fmt: str) -> Tuple[Optional[MatchGroup], str]:
    """Given a format string extract the first Match (None if there are none), 
    and return the remainder of the format string (the part not yet parsed)."""
    previous_was_open_curly_brace = False
    is_capture_group = False
    start_index = 0
    capture = ""
    for i, c in enumerate(path_fmt):
        if c == "{" and not previous_was_open_curly_brace:
            previous_was_open_curly_brace = True
            is_capture_group = True
            start_index = i
        elif c == "{" and previous_was_open_curly_brace:
            previous_was_open_curly_brace = False
            is_capture_group = False
        elif c == "}":
            previous_was_open_curly_brace = False
            is_capture_group = False
            if capture.strip() != "":
                return MatchGroup(capture, start_index, i + 1), path_fmt[i + 1:]
            capture = ""
        else:
            previous_was_open_curly_brace = False
            if not is_capture_group:
                continue

            capture += c
    return None, path_fmt