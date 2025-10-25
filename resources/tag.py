from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("tags", __name__, description="Operations on tags")


# --Route: /tag
@blp.route("/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        # Return all tags
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        # create a new tag
        store = StoreModel.query.get(tag_data["store_id"])
        if not store:
            abort(404, message="Store not found to create tag.")
            
        if TagModel.query.filter(TagModel.name == tag_data["name"]).first():
            abort(400, message=f"A tag with name '{tag_data['name']}' already exists.")
            
        tag = TagModel(**tag_data)
        
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the tag.")

        return tag
    
    
# --Route: /tag/<int:tag_id>    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        # Retrieve a tag by its ID
        tag = TagModel.query.get_or_404(tag_id)
        
        if not tag:
            abort(404, message="Tag not found.")
            
        return tag


    def delete(self, tag_id):
        # Delete a tag by its ID
        tag = TagModel.query.get_or_404(tag_id)

        if not tag:
            abort(404, message="Tag not found.")
            
        if tag.items:
            abort(400, message="Cannot delete a tag that is associated with items. Remove the associations first.")
            
        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="Error deleting tag.")
            
        return {"message": "Tag deleted successfully."}


