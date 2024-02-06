from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.repository.obtener_y_almacenar import obtener_y_almacenar_datos
from api.repository.usuarios import lista_usuarios
from api.repository.agregar_usuario import agregar_usuario
from api.repository.eliminar_usuario import eliminar_usuario
from api.repository.update_usuario import update_usuario
from api.data.models import db, Usuarios, TarjetasCredito, CuentasBancarias, Automoviles, Compras, Auth
from api.utils.auth import authenticate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, request
from datetime import timedelta
import os, re

app = Flask(__name__)

# Variable de entorno para conectarse a la BD
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Variable de entorno para la autenticacion JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.environ.get('JWT_KEY_EXPIRES')

jwt = JWTManager(app)
db.init_app(app)

# Validación de campos 
def validar_email(email):
    regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex_url = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    regex_sql = r'(SELECT|UPDATE|DELETE|INSERT|DROP|;)'

    if re.fullmatch(regex_email, email) and not re.search(regex_url, email) and not re.search(regex_sql, email):
        return True
    else:
        return False

def validar_contrasena(contrasena):
    if len(contrasena) < 10:
        return False
    if not re.search("[A-Z]", contrasena):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not validar_email(username):
        return jsonify({"error": "Formato no válido"}), 400
    if not validar_contrasena(password):
        return jsonify({"error": "La contraseña debe tener al menos 10 caracteres, favor incluir una mayúscula, un número y un caracter especial"}), 400

    new_user = Auth(user_name=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado exitosamente"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    access_token = authenticate(username, password)
    if access_token:
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Nombre de usuario o contraseña incorrectos"}), 401


@app.route('/obtener_y_almacenar', methods=['GET'])
@jwt_required()
def ruta_para_obtener_y_almacenar():
    resultado = obtener_y_almacenar_datos()
    return resultado

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    return lista_usuarios()

@app.route('/crear_usuario', methods=['POST'])
@jwt_required()
def manejar_agregar_usuario():
    return agregar_usuario()

@app.route('/eliminar_usuario', methods=['DELETE'])
@jwt_required()
def borrar_usuario():
    return eliminar_usuario()

@app.route('/update_usuario/<int:user_id>', methods=['PUT'])
@jwt_required()
def manejar_update_usuario(user_id):
    return update_usuario(user_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
