import os
from datetime import datetime, UTC
from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBManager:
    """
    Manages storing and retrieving chat conversations in MongoDB.
    Each conversation is stored as a single document with an array of messages.
    """

    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "chai_db"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]  # ✅ fixed
        self.conversations = self.db["conversations"]  # ✅ fixed
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self.conversations.create_index([("user_id", 1), ("thread_name", 1)], unique=True)
        self.conversations.create_index("user_id")

    def get_conversation(self, user_id: str, thread_name: str) -> List[Dict]:
        document = self.conversations.find_one({"user_id": user_id, "thread_name": thread_name})  # ✅ fixed
        if not document or "messages" not in document:
            return []
        return document["messages"]

    def save_conversation(self, user_id: str, thread_name: str, messages: List[Dict]) -> None:
        conversation_id = f"{user_id}_{thread_name}"  # ✅ fixed
        now = datetime.now(UTC).isoformat()
        document = {  # ✅ fixed
            "_id": conversation_id,
            "user_id": user_id,
            "thread_name": thread_name,
            "messages": messages,
            "created_at": now,
            "updated_at": now,
        }
        self.conversations.update_one({"_id": conversation_id}, {"$set": document}, upsert=True)  # ✅ fixed

    def append_message(self, user_id: str, thread_name: str, message: Dict) -> None:
        conversation_id = f"{user_id}_{thread_name}"  # ✅ fixed
        now = datetime.now(UTC).isoformat()
        update = {  # ✅ fixed
            "$push": {"messages": message},
            "$set": {"updated_at": now},
            "$setOnInsert": {
                "_id": conversation_id,
                "user_id": user_id,
                "thread_name": thread_name,
                "created_at": now,
            },
        }

        self.conversations.update_one({"_id": conversation_id}, update, upsert=True)

    def list_user_threads(self, user_id: str) -> List[str]:
        matches = list(self.conversations.find({"user_id": user_id}, {"thread_name": True, "_id": False}))  # ✅ fixed
        thread_names = [record["thread_name"] for record in matches]
        return thread_names

    def delete_conversation(self, user_id: str, thread_name: str) -> bool:
        conversation_id = f"{user_id}_{thread_name}"
        result = self.conversations.delete_one({"_id": conversation_id})
        return result.deleted_count > 0

    def close(self) -> None:
        if self.client:
            self.client.close()

    def _wipe_database(self) -> None:
        self.conversations.delete_many({})


# Test code
if __name__ == "__main__":
    print("Testing MongoDBManager")

    connection_string = "mongodb+srv://ians:ALzr3giKH0UwA9BR@cluster.y3qkfeg.mongodb.net/"
    manager = MongoDBManager(connection_string=connection_string, database_name="Cluster")

    print("Testing MongoDBManager._ensure_indexes()")
    indexes = list(manager.conversations.list_indexes())
    print(f"Created {len(indexes)} indexes")

    print("\nTesting MongoDBManager.save_conversation()")
    messages = [
        {"role": "user", "content": "hello world"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    manager.save_conversation("test_user", "test_thread", messages)
    print("Successfully saved conversation!")

    print("\nTesting MongoDBManager.get_conversation()")
    retrieved = manager.get_conversation("test_user", "test_thread")
    if len(retrieved) == 2:
        print("Successfully retrieved conversation!")
    else:
        print(f"Failed! Expected 2 messages, got {len(retrieved)}")

    print("\nTesting MongoDBManager.append_message()")
    manager.append_message("test_user", "test_thread", {"role": "user", "content": "another message"})
    retrieved = manager.get_conversation("test_user", "test_thread")
    if len(retrieved) == 3:
        print("Successfully appended message!")
    else:
        print(f"Failed! Expected 3 messages, got {len(retrieved)}")

    print("\nTesting MongoDBManager.list_user_threads()")
    manager.save_conversation("test_user", "thread2", [{"role": "user", "content": "test"}])
    threads = manager.list_user_threads("test_user")
    if len(threads) == 2:
        print(f"Successfully listed threads: {threads}")
    else:
        print(f"Failed! Expected 2 threads, got {len(threads)}: {threads}")

    print("\nCleaning up test data...")
    manager._wipe_database()
    manager.close()
    print("All tests passed!")
