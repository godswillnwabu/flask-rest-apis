from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    # Foreign key: each item belongs to a store
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    
    # Relationships
    store = db.relationship("StoreModel", back_populates="items")  # Many-to-one relationship with StoreModel
    tags = db.relationship("TagModel", secondary="item_tags", back_populates="items")  # Many-to-many relationship with TagModel through ItemTags