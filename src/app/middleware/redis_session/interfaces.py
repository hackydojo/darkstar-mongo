from abc import abstractmethod, ABCMeta
from typing import Optional, Any


# ---------------------------------------------------------
# CLASS SESSION BACKEND
# ---------------------------------------------------------
class SessionBackend:
    __metaclass__ = ABCMeta

    # -----------------------------------------------------
    # METHOD GET
    # -----------------------------------------------------
    @abstractmethod
    async def get(
            self,
            key: str
    ) -> Optional[dict]:
        raise NotImplementedError()  # pragma: no cover

    # -----------------------------------------------------
    # METHOD SET
    # -----------------------------------------------------
    @abstractmethod
    async def set(
            self,
            key: str,
            value: dict,
            exp: Optional[int]
    ) -> Optional[str]:
        raise NotImplementedError()  # pragma: no cover

    # -----------------------------------------------------
    # METHOD SET
    # -----------------------------------------------------
    @abstractmethod
    async def delete(
            self,
            key: str
    ) -> Any:
        raise NotImplementedError()  # pragma: no cover
