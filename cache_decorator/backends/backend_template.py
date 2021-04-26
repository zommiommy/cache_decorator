from typing import List

class BackendTemplate:
    """To serialize and de-serialize data we need double dynamic dispatching, 
    thus this is the template for all the implementations.
    
    The backends must be implemented in such a way that:
    backend = Backend(load_kwargs, dump_kwargs)
    backend.load(backend.dump(object, "./test"), "./test") == object
    """
    SUPPORTED_EXTENSIONS = []

    def __init__(self, load_kwargs, dump_kwargs):
        """The init must always handle kwargs since """
        self._load_kwargs = load_kwargs
        self._dump_kwargs = dump_kwargs

    @staticmethod
    def support_path(path:str) -> bool:
        """Returns if the current backend MIGHT serialize and deserialize the given path.
        This is a might because the given object might not be serializable, but we
        support the extension."""
        return any(
            path.endswith(extension)
            for extension in BackendTemplate.SUPPORTED_EXTENSIONS
        ) 
        
    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        """Must return if the current backend can handle the type of data."""
        raise NotImplementedError(
            "This backend function has to be implemented by its subclass."
        )

    def dump(self, obj_to_serialize: object, path:str) -> dict:
        """Serialize and save the object at the given path.
        If this backend needs extra informations to de-serialize data, it can 
        return them as a dictionary which will be serialized as a json."""     
        raise NotImplementedError(
            "This backend function has to be implemented by its subclass."
        )

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        """Must return if the current backend can handle the type of data."""
        raise NotImplementedError(
            "This backend function has to be implemented by its subclass."
        )

    def load(self, metadata:dict, path:str) -> object:
        """Load the method at the given path. If the medod need extra
        informations it can read them form the metadata dictionary which is
        the return value of the dump method."""
        raise NotImplementedError(
            "This backend function has to be implemented by its subclass."
        )