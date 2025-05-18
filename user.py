import os
import hashlib
import datetime
from uuid import uuid4
import json
class User:
    DATA_FILE = "data/users.txt"
    
    def __init__(self, username, password=None, hashed_password=None, id=None, created_at=None):
        self.id = id if id else str(uuid4())
        self.username = username
        self.hashed_password = hashed_password if hashed_password else self._hash_password(password)
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
    
    def _hash_password(self, password):
        # Simple hashing for demonstration (consider bcrypt for production)
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
            username=data["username"],
            hashed_password=data["hashed_password"],
            id=data["id"],
            created_at=data["created_at"]
        )
    
    @classmethod
    def _ensure_data_file_exists(cls):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(cls.DATA_FILE):
            with open(cls.DATA_FILE, "w") as f:
                f.write("")
    
    @classmethod
    def get_all(cls):
        cls._ensure_data_file_exists()
        users = []
        with open(cls.DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        user_data = json.loads(line)
                        users.append(cls.from_dict(user_data))
                    except json.JSONDecodeError:
                        continue
        return users
    
    @classmethod
    def get_by_username(cls, username):
        users = cls.get_all()
        for user in users:
            if user.username == username:
                return user
        return None
    
    def save(self):
        self._ensure_data_file_exists()
        users = self.get_all()
        
        # Update existing user or add new
        existing_index = next((i for i, u in enumerate(users) if u.username == self.username), None)
        if existing_index is not None:
            users[existing_index] = self
        else:
            users.append(self)
        
        # Save all users
        with open(self.DATA_FILE, "w") as f:
            for user in users:
                f.write(json.dumps(user.to_dict()) + "\n")