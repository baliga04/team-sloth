from dataclasses import dataclass
from app.extensions import db

@dataclass
class Transactions(db.Model):
    TransactionID: int = db.Column(db.Integer, primary_key=True)
    UserID: int = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    Amount: float = db.Column(db.Float, nullable=False)
    Category: str = db.Column(db.String(50), nullable=False)
    DateTime: str = db.Column(db.DateTime(timezone=True), nullable=False)
    Description: str = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
         return f'<Transactions>'