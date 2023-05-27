from dataclasses import dataclass
from app.extensions import db
from sqlalchemy.orm import relationship

@dataclass
class User(db.Model):
    UserID: int = db.Column(db.Integer, primary_key=True)
    FirstName: str = db.Column(db.String(50), nullable=False)
    LastName: str = db.Column(db.String(50), nullable=False)
    Email: str = db.Column(db.String(50), nullable=False)
    Password: str = db.Column(db.Text, nullable=False)
    Balance: float = db.Column(db.Float, nullable=False,default=0.0)

    # On Delete Cascade
    transactions = relationship("Transactions", backref="User",cascade="all, delete-orphan") 

    def __repr__(self):
         return f'<User>'