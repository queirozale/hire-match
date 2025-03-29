from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pymongo import MongoClient, errors

from api.database.models.resume_model import Resume
from api.database.models.user_model import User
from api.database.i_db import DataBase


class MongoDB(DataBase):
    """
    MongoDB implementation of the DataBase interface.
    Handles CRUD operations for Resume and User models.
    """
    def __init__(self, uri: str, db_name: str):
        """
        Initializes the MongoDB client and database connection.
        
        Args:
            uri (str): MongoDB connection URI.
            db_name (str): Name of the database.
        
        Raises:
            ConnectionError: If the connection to MongoDB fails.
        """
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.client.server_info()
        except errors.ServerSelectionTimeoutError:
            raise ConnectionError("Failed to connect to MongoDB. Check your URI and database status.")

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Finds a single document in the specified collection.
        
        Args:
            collection_name (str): Name of the MongoDB collection.
            query (Dict[str, Any]): Query filter.
        
        Returns:
            List[Dict[str, Any]]: List containing the found document.
        
        Raises:
            RuntimeError: If an error occurs during the query.
        """
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception as e:
            raise RuntimeError(f"Error while finding a document: {e}")
    
    def find(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Finds multiple documents in the specified collection.
        
        Args:
            collection_name (str): Name of the MongoDB collection.
            query (Dict[str, Any]): Query filter.
        
        Returns:
            List[Dict[str, Any]]: List of found documents.
        
        Raises:
            RuntimeError: If an error occurs during the query.
        """
        try:
            collection = self.db[collection_name]
            return collection.find(query)
        except Exception as e:
            raise RuntimeError(f"Error while finding documents: {e}")
    
    def insert_one(self, collection_name: str, data: Resume | User) -> Any:
        """
        Inserts a document into the specified collection.
        
        Args:
            collection_name (str): Name of the MongoDB collection.
            data (Resume | User): Data object to insert.
        
        Returns:
            Any: Inserted document ID.
        
        Raises:
            ValueError: If data is not an instance of Resume or User.
            RuntimeError: If an error occurs during insertion.
        """
        try:
            if not isinstance(data, (Resume, User)):
                raise ValueError("Data must be an instance of Resume or User")

            collection = self.db[collection_name]
            result = collection.insert_one(data.dict())
            return result.inserted_id
        except Exception as e:
            raise RuntimeError(f"Error while inserting document: {e}")

    def update_one(self, collection_name: str, query: Dict[str, Any], update_data: Resume | User) -> int:
        """
        Updates a document in the specified collection.
        
        Args:
            collection_name (str): Name of the MongoDB collection.
            query (Dict[str, Any]): Query filter.
            update_data (Resume | User): Updated data.
        
        Returns:
            int: Number of modified documents.
        
        Raises:
            ValueError: If update_data is not an instance of Resume or User.
            RuntimeError: If an error occurs during the update.
        """
        try:
            if not isinstance(update_data, (Resume, User)):
                raise ValueError("Update data must be an instance of Resume or User")

            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except Exception as e:
            raise RuntimeError(f"Error while updating document: {e}")

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Deletes a document from the specified collection.
        
        Args:
            collection_name (str): Name of the MongoDB collection.
            query (Dict[str, Any]): Query filter.
        
        Returns:
            int: Number of deleted documents.
        
        Raises:
            RuntimeError: If an error occurs during deletion.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            raise RuntimeError(f"Error while deleting document: {e}")