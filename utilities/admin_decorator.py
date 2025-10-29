from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Ensure the JWT is valid
        verify_jwt_in_request()
        jwt = get_jwt()
        
        # Check if the user has admin privileges
        if not jwt.get("is_admin"):
            return {"message": "Admin access required."}, 403
        
        return fn(*args, **kwargs)
    return wrapper
