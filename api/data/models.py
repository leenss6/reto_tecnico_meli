from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
import bcrypt

# Creacion de models.py para evitar la interacción directa con la BD
db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    fec_alta = db.Column(db.DateTime)
    user_name = db.Column(db.String(255))
    codigo_zip = db.Column(LargeBinary)
    direccion = db.Column(LargeBinary)
    geo_latitud = db.Column(LargeBinary)
    geo_longitud = db.Column(LargeBinary)
    color_favorito = db.Column(db.String(50))
    foto_dni = db.Column(LargeBinary)
    ip = db.Column(LargeBinary)
    fec_birthday = db.Column(db.Date)

    tarjetas_credito = db.relationship("TarjetasCredito", back_populates="usuario", cascade="all, delete-orphan")
    cuentas_bancarias = db.relationship("CuentasBancarias", back_populates="usuario", cascade="all, delete-orphan")
    automoviles = db.relationship("Automoviles", back_populates="usuario", cascade="all, delete-orphan")
    compras = db.relationship("Compras", back_populates="usuario", cascade="all, delete-orphan")

class TarjetasCredito(db.Model):
    __tablename__ = 'TarjetasCredito'
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    credit_card_num = db.Column(LargeBinary)
    credit_card_ccv = db.Column(LargeBinary)
    id = db.Column(db.Integer, primary_key=True)

    usuario = db.relationship("Usuarios", back_populates="tarjetas_credito")

class CuentasBancarias(db.Model):
    __tablename__ = 'CuentasBancarias'
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    cuenta_numero = db.Column(LargeBinary)
    id = db.Column(db.Integer, primary_key=True)

    usuario = db.relationship("Usuarios", back_populates="cuentas_bancarias")

class Automoviles(db.Model):
    __tablename__ = 'Automoviles'
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    auto = db.Column(db.String(255))
    auto_modelo = db.Column(db.String(255))
    auto_tipo = db.Column(db.String(255))
    auto_color = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)

    usuario = db.relationship("Usuarios", back_populates="automoviles")

class Compras(db.Model):
    __tablename__ = 'Compras'
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    cantidad_compras_realizadas = db.Column(db.BigInteger)
    id = db.Column(db.Integer, primary_key=True)

    usuario = db.relationship("Usuarios", back_populates="compras")

class Auth(db.Model):
    __tablename__ = 'Auth'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Almacenar la versión hasheada de la contraseña 
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')