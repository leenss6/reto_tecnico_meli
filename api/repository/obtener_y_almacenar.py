from api.data.models import db, Usuarios, TarjetasCredito, CuentasBancarias, Automoviles, Compras
import requests
import datetime
from api.utils.encrypt import encrypt_data

def obtener_y_almacenar_datos():
    # Consultar el endpoint dado en el reto
    url = "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for user_data in data:
            if Usuarios.query.get(int(user_data['id'])):
                # Verificar si ya existe el registro en la BD
                return f"Error: Usuario con ID {user_data['id']} ya existe.", 400
            
        for user_data in data:
            # Manejo de fec_alta por formato
            try:
                fec_alta = datetime.datetime.strptime(user_data['fec_alta'], '%d/%m/%Y')
            except ValueError:
                fec_alta = datetime.datetime.strptime(user_data['fec_alta'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # Manejo de fec_birthday por formato
            try:
                fec_birthday = datetime.datetime.strptime(user_data.get('fec_birthday', '2021-01-01T00:00:00.000Z'), '%Y-%m-%dT%H:%M:%S.%fZ').date()
            except ValueError:
                fec_birthday = datetime.datetime.strptime(user_data['fec_birthday'], '<otro formato>').date()
            print(int(user_data['id']))
            usuario = Usuarios(
                # Se guardan los datos y se encriptan algunos considerados sensibles 
                id=int(user_data['id']),
                fec_alta=fec_alta,
                user_name=user_data['user_name'],
                codigo_zip=encrypt_data(user_data['codigo_zip']),
                direccion=encrypt_data(user_data['direccion']),
                geo_latitud=encrypt_data(user_data['geo_latitud']),
                geo_longitud=encrypt_data(user_data['geo_longitud']),
                color_favorito=user_data['color_favorito'],
                foto_dni=encrypt_data(user_data['foto_dni']),
                ip=encrypt_data(user_data['ip']),
                fec_birthday=fec_birthday
            )
            db.session.add(usuario)

            tarjeta = TarjetasCredito(
                user_id=int(user_data['id']),
                credit_card_num=encrypt_data(user_data['credit_card_num']),
                credit_card_ccv=encrypt_data(user_data['credit_card_ccv'])
            )
            usuario.tarjetas_credito.append(tarjeta)

            cuenta = CuentasBancarias(
                user_id=int(user_data['id']),
                cuenta_numero=encrypt_data(user_data['cuenta_numero'])
            )
            usuario.cuentas_bancarias.append(cuenta)

            auto = Automoviles(
                user_id=int(user_data['id']),
                auto=user_data['auto'],
                auto_modelo=user_data['auto_modelo'],
                auto_tipo=user_data['auto_tipo'],
                auto_color=user_data['auto_color']
            )
            usuario.automoviles.append(auto)

            compra = Compras(
                user_id=int(user_data['id']),
                cantidad_compras_realizadas=user_data['cantidad_compras_realizadas']
            )
            usuario.compras.append(compra)

        db.session.commit()
        return "Datos obtenidos y almacenados con éxito."
    else:
        return "Error al obtener datos: " + str(response.status_code)
