from abc import ABC, abstractmethod
from typing import Union


class BaseDBAdapter(ABC):

    @abstractmethod
    async def insert_one(self, collection_name: str, data: dict):
        pass

    @abstractmethod
    async def find_one(self, collection_name: str, db_filter: dict,
                       projection: dict = None) -> Union[dict, None]:
        pass

    @abstractmethod
    async def find(self, collection_name: str, db_filter: dict,
                   projection: dict = None) -> list[dict]:
        pass

    @abstractmethod
    async def update_one(self, collection_name: str, db_filter: dict, update_data: dict) -> int:
        pass

    @abstractmethod
    async def delete_one(self, collection_name: str, db_filter: dict):
        pass
