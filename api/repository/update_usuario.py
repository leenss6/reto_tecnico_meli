from api.data.models import db, Usuarios, TarjetasCredito, CuentasBancarias
from flask import request, jsonify
from api.utils.encrypt import encrypt_data
import re

# Define explícitamente los campos que necesitan ser encriptados al momento de actualizar/almacenar
campos_encriptados = {
    'codigo_zip',
    'direccion',
    'geo_latitud',
    'geo_longitud',
    'foto_dni',
    'ip'
}

def validar_sqlinjection(datos):
    # Revisar que no contengan comandos para inyeccion SQL
    regex_sql = r'(SELECT|UPDATE|DELETE|INSERT|DROP|;)'
    return re.search(regex_sql, str(datos), re.IGNORECASE) is None

def update_usuario(user_id):
    data = request.json
    usuario = Usuarios.query.get(user_id)

    # Mensaje de error por si el ID entregado no existe
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    for campo, valor in data.items():
        if not validar_sqlinjection(valor):
            return jsonify({"error": "Datos no válidos"}), 400

    # Actualiza los campos del usuario con la encriptación cuando sea necesario
    for campo, valor in data.items():
        if hasattr(usuario, campo):
            if campo in campos_encriptados:
                valor = encrypt_data(valor) if valor is not None else None
            setattr(usuario, campo, valor)
        else:
            # Mensaje por si se intenta actualizar un campo que no existe
            return jsonify({"error": f"Campo '{campo}' no actualizable"}), 400

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado con éxito"}), 200
