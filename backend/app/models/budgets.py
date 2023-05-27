from dataclasses import dataclass
from app.extensions import db

@dataclass
class Budgets(db.Model):
    
    def __repr__(self):
         return f'<Budget>'