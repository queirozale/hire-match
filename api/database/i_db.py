from abc import ABC, abstractmethod
from typing import Any, Dict, List

class DataBase(ABC):
    """
    Abstract base class for a database interface.
    """
    @abstractmethod
    def insert_one(self, collection: str, data: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def find(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_one(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_one(self, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def delete_one(self, collection: str, query: Dict[str, Any]) -> int:
        pass