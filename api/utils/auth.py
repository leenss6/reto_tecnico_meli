import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from api.data.models import Auth

# Revisa si el user_name y la password coinciden con los de la BD
def authenticate(username, password):
    user = Auth.query.filter_by(user_name=username).first()
    # Compara la contraseña dado con la contraseña encriptada en la BD
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        # genera el token
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=2))
        return access_token
    return None