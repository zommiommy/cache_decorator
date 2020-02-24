"""Package that automatically caches and dispatch serialization and deserialization to the correct functions depending on the extension."""
from .cache import cache

__all__ = ["cache"]