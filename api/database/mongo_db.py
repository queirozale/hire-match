# from abc import ABC, abstractmethod
# from typing import Any, Dict, List, Optional
# from pymongo import MongoClient

# from i_db import DataBase
# from 

# config = 

# class MongoDB(DataBase):
#     """
#     MongoDB implementation of the DataBase interface.
#     """
#     def __init__(self, uri: str, db_name: str):
#         self.client = MongoClient(uri)
#         self.db = self.client[db_name]

#     def insert(self, collection: str, data: Dict[str, Any]) -> Any:
#         result = self.db[collection].insert_one(data)
#         return result.inserted_id

#     def find(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
#         return list(self.db[collection].find(query))

#     def update(self, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
#         result = self.db[collection].update_many(query, {'$set': update_data})
#         return result.modified_count

#     def delete(self, collection: str, query: Dict[str, Any]) -> int:
#         result = self.db[collection].delete_many(query)
#         return result.deleted_count