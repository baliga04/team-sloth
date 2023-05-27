from dataclasses import dataclass
from app.extensions import db

@dataclass
class Budgets(db.Model):
    UserID: int = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
    Category: str = db.Column(db.String(50), primary_key=True)
    Budget: float = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
         return f'<Budget>'