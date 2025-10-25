from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import StoreModel  # Import the in-memory items dictionary
from schemas import StoreSchema  # Import the StoreSchema for validation

blp = Blueprint("stores", __name__, description="Operations on stores")


# ---Route: /store 
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # Return all stores
        stores = StoreModel.query.all()
        return stores
    

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # create a new store
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")

        return store


# ---Route: /store/<int:store_id>
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # Retrieve a store by its ID
        store = StoreModel.query.get_or_404(store_id)
        
        return store
    
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        # Update an existing store
        store = StoreModel.query.get_or_404(store_id)
        store.name = store_data["name"]
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the store.")
        
        return store


    @jwt_required()
    def delete(self, store_id):
        
        # Check if Admin: Only Admins can delete a store 
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")
            
        # Delete a store by its ID
        store = StoreModel.query.get_or_404(store_id)
        
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the store.")

        return {"message": "Store deleted successfully"}
