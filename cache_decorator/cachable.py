from typing import List, Any, Dict, Tuple, Type
from .backends import Backend

from numpy import isin
from .path_formatter import PathFormatter

class CacheObject:
    def get_paths_fmt_and_objects(self, path_formatter: PathFormatter) -> List[Tuple[str, Any]]:
        raise NotImplementedError()

class CacheListVariableLength(CacheObject):
    def __init__(self, path_fmt: str, objects_to_cache: List[Any], index_arg_name: str="index", allow_empty_list: bool = False):

        if not isinstance(objects_to_cache, list):
            raise ValueError((
                "The objects to cache passed to the {} are not a list "
                "but an object of type '{}'."
            ).format(type(self.__class__.__name__, objects_to_cache)))

        if  not allow_empty_list and len(objects_to_cache) == 0:
            raise ValueError((
                "The parameter `allow_empty_list` for {} is False but "
                "the given list to cache is empty!"
            ).format(self.__class__.__name__))

        if "{" in index_arg_name or "}" in index_arg_name:
            raise ValueError((
                "The `index_arg_name` provided is `{}` and curly "
                "brace are not allowed."
            ).format(index_arg_name))

        # TODO: handle also weird gimmigcks like {{{{{{{{{}}}}}}}}}
        if "{" + index_arg_name + "}" not in path_fmt:
            raise ValueError((
                "We expected the provided path_fmt `{}` to contain the provided "
                "index_arg_name `{}` wrapped in curly braces like so: `{{{}}}`"
            ).format(
                path_fmt,
                index_arg_name,
                index_arg_name,
            ))

        self.path_fmt = path_fmt
        self.objects_to_cache = objects_to_cache
        self.index_arg_name = index_arg_name

    def get_paths_fmt_and_objects(self, path_formatter: PathFormatter) -> List[Tuple[str, Any]]:
        return [
            (
                path_formatter.format_path(self.path_fmt, extra_args={self.index_arg_name:index}),
                obj_to_cache,
            )
            for index, obj_to_cache in enumerate(self.objects_to_cache)
        ]

class CacheValue(CacheObject):
    def __init__(self, path_fmt: str, object_to_cache: Any):
        self.path_fmt = path_fmt
        self.object_to_cache = object_to_cache
    
    def get_paths_fmt_and_objects(self, path_formatter: PathFormatter) -> List[Tuple[str, Any]]:
        return [
            (
                path_formatter.format_path(self.path_fmt),
                self.obj_to_cache,
            )
        ]
        


class Cachable:

    @staticmethod
    def get_metadata_fmt_path(path_formatter: PathFormatter) -> str:
        raise NotImplementedError("")

    @staticmethod
    def load(objs: Dict[str, Any]) -> Cachable:
        raise NotImplementedError()

    def dump(self, metadata: Dict[str, Any]) -> Dict[str, Type[CachableObject]]:
        raise NotImplementedError()


def cachable_factory(path_formatter: PathFormatter, path: Union[str, Tuple[Any], List[Any], Dict[str, Any]]) -> CachableFactory:
    if isinstance(path, str):
        return CachableValueFactory(path_formatter, path)
    elif isinstance(path, tuple):
        return CachableTupleFactory(path_formatter, path)
    elif isinstance(path, list):
        return CachableListFactory(path_formatter, path)
    elif isinstance(path, dict):
        return CachableDictFactory(path_formatter, path)
    elif issubclass(path, Cachable):
        return path

    raise ValueError(
        "The given value of type `{}` cannot be used as a cache path.".format(type(path))
    )


class CachableListFactory(CachableFactory):
    def __init__(self, path_formatter: PathFormatter, paths: List[str]):
        for path in paths:
            path_formatter.validate_path(path)

        self.path = paths


    def make(self, objs: List[Any]) -> CachableList:
        return CachableList(objs, self.paths)

class CachableList:

    def __init__(self, paths: List[str], objects: List[Any]):

    @staticmethod
    def get_metadata_fmt_path(path_formatter: PathFormatter) -> str:
        raise NotImplementedError("")

    @staticmethod
    def load(objs: Dict[str, Any]) -> Cachable:
        raise NotImplementedError()

    def dump(self) -> Dict[str, Type[CachableObject]]:

        raise NotImplementedError()
