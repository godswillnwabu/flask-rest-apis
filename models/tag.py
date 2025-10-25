from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    # Each tag belongs to one store
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    
    # Relationships
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", secondary="item_tags", back_populates="tags")  # Many-to-many relationship with items