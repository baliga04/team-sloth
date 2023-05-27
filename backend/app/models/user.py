from dataclasses import dataclass
from app.extensions import db

@dataclass
class User(db.Model):
    
    def __repr__(self):
         return f'<User>'