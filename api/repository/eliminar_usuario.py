from api.data.models import db, Usuarios
from flask import jsonify, request

def eliminar_usuario():
    # Obtener el ID del usuario a eliminar desde la solicitud
    user_id = request.json.get('id')

    # Buscar el usuario por ID
    usuario = Usuarios.query.get(user_id)

    if usuario:
        # Eliminar el usuario si existe
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario eliminado con éxito"}), 200
    else:
        # Si el usuario no fue encontrado
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
