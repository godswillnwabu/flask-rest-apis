from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import ItemModel, StoreModel, TagModel
from schemas import ItemSchema, ItemUpdateSchema 

blp = Blueprint("items", __name__, description="Operations on items")


# ---Route: /item
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # Return all items
        return ItemModel.query.all()


    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # create a new item
        store = StoreModel.query.get(item_data["store_id"])
        if not store:
            abort(400, message="Store not found to create item.")
            
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item, maybe the item already exists.")            
            
        return item
    
    
# ---Route: /item/<int:item_id> 
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Retrieve an item by its ID
        item = ItemModel.query.get_or_404(item_id)
        return item
    

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # Update an existing item
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")

        return item


    @jwt_required()
    def delete(self, item_id):
        # Delete an item by its ID
        item = ItemModel.query.get_or_404(item_id)
        
        if not item:
            abort(404, message="Item not found.")

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the item.")

        return {"message": "Item deleted successfully"}
    
    
    
# --Route: /item/<int:item_id>/tag/<int:tag_id>   
@jwt_required() 
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201, ItemSchema)
    def post(self, item_id, tag_id):
        # Link tag to item
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if tag.store_id != item.store_id:
            abort(400, message="Item and Tag must belong to the same store before linking.")
            
        if tag in item.tags:
            abort(400, message="Tag is already linked to the item.")

        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error linking tag and item.")

        return {"message": "Tag added to item successfully."}

    
    @jwt_required()
    def delete(self, item_id, tag_id):
        # Unlink tag from item
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        if tag not in item.tags:
            abort(400, message="Tag is not linked to the item.")
        
        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error unlinking tag and item.")

        return {"message": "Tag removed from item successfully."}
    

   