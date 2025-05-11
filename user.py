import json
import os
import hashlib
import datetime
from uuid import uuid4

class User:
    def __init__(self, username, password=None, hashed_password=None, id=None, created_at=None):
        self.id = id if id else str(uuid4())
        self.username = username
        self.hashed_password = hashed_password if hashed_password else self._hash_password(password)
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
    
    def _hash_password(self, password):
        # Simple hashing for demonstration purposes
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self.hashed_password == self._hash_password(password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            hashed_password=data.get("hashed_password"),
            id=data.get("id"),
            created_at=data.get("created_at")
        )
    
    @classmethod
    def get_all(cls):
        users = []
        if os.path.exists("data/users.json"):
            with open("data/users.json", "r") as f:
                try:
                    data = json.load(f)
                    for user_data in data:
                        users.append(cls.from_dict(user_data))
                except json.JSONDecodeError:
                    # Handle empty or invalid JSON file
                    pass
        return users
    
    @classmethod
    def get_by_username(cls, username):
        users = cls.get_all()
        for user in users:
            if user.username == username:
                return user
        return None
    
    def save(self):
        users = self.get_all()
        # Check if user already exists
        for i, user in enumerate(users):
            if user.username == self.username:
                # Update existing user
                users[i] = self
                break
        else:
            # Add new user
            users.append(self)
        
        # Save all users to file
        os.makedirs("data", exist_ok=True)
        with open("data/users.json", "w") as f:
            json.dump([user.to_dict() for user in users], f, indent=2)
        return self