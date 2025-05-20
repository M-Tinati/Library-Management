import hashlib
import json
import os

class User:
    def __init__(self, username, password, role="member"):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.role = role
        self.borrow_history = []

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "borrow_history": self.borrow_history
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], "", data["role"])
        user.password_hash = data["password_hash"]
        user.borrow_history = data.get("borrow_history", [])
        return user

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = {}
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                data = json.load(file)
                self.users = {user["username"]: User.from_dict(user) for user in data}
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump([user.to_dict() for user in self.users.values()], file, indent=4)

    def register(self, username, password, role="member"):
        if username in self.users:
            return False, "Username already exists."
        self.users[username] = User(username, password, role)
        self.save_users()
        return True, "User registered successfully."

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            return True, user
        return False, "Invalid username or password."
