from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    # Relationships
    items = db.relationship("ItemModel", back_populates="store", cascade="all, delete-orphan")  # One-to-many relationship with ItemModel
    tags = db.relationship("TagModel", back_populates="store", cascade="all, delete-orphan")  # One-to-many relationship with TagModel
    
    def __repr__(self):
        return f"<StoreModel name={self.name}>"