from flask import jsonify
from api.utils.encrypt import decrypt_data
import json
from api.data.models import Usuarios, TarjetasCredito, CuentasBancarias, Automoviles, Compras

def usuario_a_json(usuario):
    usuario_dict = {
        "id": usuario.id,
        "user_name": usuario.user_name,
        "informacion_personal": {
            # Mostrar los datos y desencriptar aquellos que estaban almacenados con el algoritmo de cifrado
            "fec_alta": usuario.fec_alta.strftime("%Y-%m-%d %H:%M:%S") if usuario.fec_alta else None,
            "fec_birthday": usuario.fec_birthday.strftime("%Y-%m-%d") if usuario.fec_birthday else None,
            "codigo_zip": decrypt_data(usuario.codigo_zip),
            "direccion": decrypt_data(usuario.direccion),
            "geo_latitud": float(decrypt_data(usuario.geo_latitud)) if usuario.geo_latitud else None,
            "geo_longitud": float(decrypt_data(usuario.geo_longitud)) if usuario.geo_longitud else None,
            "color_favorito": usuario.color_favorito,
            "foto_dni": decrypt_data(usuario.foto_dni),
            "ip": decrypt_data(usuario.ip)
        },
        "vehiculos": [
            {
                "auto": auto.auto, 
                "modelo": auto.auto_modelo, 
                "tipo": auto.auto_tipo, 
                "color": auto.auto_color
            } for auto in usuario.automoviles
        ],
        "compras_realizadas": [
            {
                "cantidad": compra.cantidad_compras_realizadas
            } for compra in usuario.compras
        ],
        "financiero": {
            "cuentas": [{"numero": decrypt_data(cuenta.cuenta_numero)} for cuenta in usuario.cuentas_bancarias],
            "tarjetas": [{"numero": decrypt_data(tarjeta.credit_card_num), "ccv": decrypt_data(tarjeta.credit_card_ccv)} for tarjeta in usuario.tarjetas_credito]
        }
    }
    return usuario_dict

def lista_usuarios():
    usuarios = Usuarios.query.all()
    resultado = [usuario_a_json(usuario) for usuario in usuarios]
    return json.dumps(resultado, sort_keys=False, indent=4)
