import os
import json
import datetime

class User:
    DATA_FILE = "data/users.txt"
    _next_id = 1  # Class variable to track next available ID
    
    def __init__(self, username, password=None, hashed_password=None, id=None, created_at=None):
        self.id = id if id is not None else self._get_next_id()
        self.username = username
        self.hashed_password = hashed_password if hashed_password else self._hash_password_FNV1a_32(password)
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
    
    @classmethod
    def _get_next_id(cls):
        # Get all users to determine next ID
        users = cls.get_all()
        if users:
            cls._next_id = max(user.id for user in users) + 1
        return cls._next_id
    
    def _hash_password_FNV1a_32(self, password):
        """32-bit FNV-1a hash implementation"""
        FNV_OFFSET_BASIS = 0x811C9DC5
        FNV_PRIME = 0x01000193
        
        hash_value = FNV_OFFSET_BASIS
        for byte in password.encode('utf-8'):
            hash_value ^= byte
            hash_value = (hash_value * FNV_PRIME) & 0xFFFFFFFF  # 32-bit mask
        
        return str(hash_value)
    
    def verify_password(self, password):
        return self.hashed_password == self._hash_password_FNV1a_32(password)
    
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
        
        # Initialize ID counter
        cls._next_id = 1
        
        try:
            with open(cls.DATA_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            user_data = json.loads(line)
                            user = cls.from_dict(user_data)
                            users.append(user)
                            # Track highest ID
                            if user.id >= cls._next_id:
                                cls._next_id = user.id + 1
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            pass
            
        return users
    
    @classmethod
    def get_by_username(cls, username):
        users = cls.get_all()
        for user in users:
            if user.username == username:
                return user
        return None
    
    @classmethod
    def get_by_id(cls, user_id):
        users = cls.get_all()
        for user in users:
            if user.id == user_id:
                return user
        return None
    
    def save(self):
        self._ensure_data_file_exists()
        users = self.get_all()
        
        # Update existing user or add new
        existing_index = next((i for i, u in enumerate(users) if u.id == self.id), None)
        if existing_index is not None:
            users[existing_index] = self
        else:
            users.append(self)
        
        # Save all users
        with open(self.DATA_FILE, "w") as f:
            for user in users:
                f.write(json.dumps(user.to_dict()) + "\n")