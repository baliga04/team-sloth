from dataclasses import dataclass
from app.extensions import db

@dataclass
class Transactions(db.Model):
    
    def __repr__(self):
         return f'<Transactions>'