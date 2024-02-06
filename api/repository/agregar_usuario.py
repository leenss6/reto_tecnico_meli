from api.data.models import db, Usuarios, TarjetasCredito, CuentasBancarias, Automoviles, Compras
from flask import request, jsonify
import datetime
from api.utils.encrypt import encrypt_data
import re

# Validar que no contengan comandos para inyección SQL
def validar_sqlinyection(datos):
    regex_sql = r'(SELECT|UPDATE|DELETE|INSERT|DROP|;)'
    return re.search(regex_sql, datos) is None

def agregar_usuario():
    data = request.get_json()

    # Rescatar el último ID de usuario en tabla Usuarios
    ultimo_id = db.session.query(db.func.max(Usuarios.id)).scalar()
    if ultimo_id is None:
        ultimo_id = 0 

    # Validar que otros campos no contengan comandos para inyeccion SQL
    campos = [data.get('user_name'), data.get('codigo_zip'), data.get('geo_latitud'), data.get('geo_longitud'), data.get('color_favorito'), data.get('foto_dni'), data.get('ip')]
    for campo in campos:
        if not validar_sqlinyection(campo):
            return jsonify({"error": "Datos no válidos"}), 400

    # Crear un nuevo usuario
    nuevo_usuario = Usuarios(
        id=ultimo_id + 1,
        user_name=data.get('user_name'),
        fec_alta=datetime.datetime.now(),  # Fecha y hora actual
        fec_birthday=datetime.datetime.strptime(data.get('fec_birthday'), '%Y-%m-%d'),
        codigo_zip=encrypt_data(data.get('codigo_zip')),
        direccion=encrypt_data(data.get('direccion')),
        geo_latitud=encrypt_data(data.get('geo_latitud')),
        geo_longitud=encrypt_data(data.get('geo_longitud')),
        color_favorito=data.get('color_favorito'),
        foto_dni=encrypt_data(data.get('foto_dni')),
        ip=encrypt_data(data.get('ip'))
    )

    # Agregar demás datos
    tarjeta = TarjetasCredito(
        credit_card_num=encrypt_data(data.get('credit_card_num')),
        credit_card_ccv=encrypt_data(data.get('credit_card_ccv'))
    )
    cuenta = CuentasBancarias(
        cuenta_numero=encrypt_data(data.get('cuenta_numero'))
    )
    automovil = Automoviles(
        auto=data.get('auto'),
        auto_modelo=data.get('auto_modelo'),
        auto_tipo=data.get('auto_tipo'),
        auto_color=data.get('auto_color')
    )
    compra = Compras(
        cantidad_compras_realizadas=data.get('cantidad_compras_realizadas')
    )

    # Asociar las tarjetas de crédito, cuentas bancarias, automóviles y compras al usuario
    nuevo_usuario.tarjetas_credito.append(tarjeta)
    nuevo_usuario.cuentas_bancarias.append(cuenta)
    nuevo_usuario.automoviles.append(automovil)
    nuevo_usuario.compras.append(compra)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario agregado con éxito", "id": nuevo_usuario.id}), 201



