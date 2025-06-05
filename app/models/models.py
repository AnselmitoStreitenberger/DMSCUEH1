from app.db import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import DateTime, Boolean, Integer, Text, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

estado_enum = ENUM('para pedir', 'pedido', 'recibido', 'sin stock fabrica', name='estado', create_type=False)


class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(Text)
    ano = db.Column(DateTime)
    codigo_manual = db.Column(Text)


class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    codigo_pieza = db.Column(db.Text, primary_key=True)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float)
    stock_min = db.Column(db.Integer)
    stock_real = db.Column(db.Integer)
    stock_disp = db.Column(db.Integer)

    vehiculos = db.relationship(
        'Vehiculo',
        secondary='repuestosvehiculos',
        backref='repuestos'
    )



class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(Integer, primary_key=True)
    fecha_creacion = db.Column(DateTime)
    codigo_pedido = db.Column(Text)
    fecha_ped_fab = db.Column(DateTime)
    factura = db.Column(Text)
    remito = db.Column(Text)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(Integer, primary_key=True)
    telefono = db.Column(Text)
    nombre = db.Column(Text)


class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'
    id = db.Column(Integer, primary_key=True)
    vehiculo_id = db.Column(Integer, ForeignKey('vehiculos.id'))
    cliente_id = db.Column(Integer, ForeignKey('clientes.id'))
    precio = db.Column(Float)
    se_pidio = db.Column(Boolean)


class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(Integer, primary_key=True)
    cliente_id = db.Column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha = db.Column(DateTime)
    valor_total_dolar = db.Column(Float)
    valor_total_pesos = db.Column(Float)
    factura = db.Column(Text)


class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    id = db.Column(Integer, primary_key=True)
    identificador = db.Column(Text)
    numero_de_cuenta = db.Column(Text)
    saldo = db.Column(Float)


class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(Integer, primary_key=True)
    cuenta_id = db.Column(Integer, ForeignKey('cuentas.id'), nullable=False)
    valor = db.Column(Float)
    detalle = db.Column(Text)
    fecha = db.Column(DateTime)


class PedidoDetalle(db.Model):
    __tablename__ = 'pedidosdetalle'
    id = db.Column(Integer, primary_key=True)
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), nullable=False)
    pedido_id = db.Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    cantidad = db.Column(Integer)
    estado = db.Column(estado_enum, nullable=False)
    fecha_recibido = db.Column(DateTime)


class PedidoCliente(db.Model):
    __tablename__ = 'pedidosclientes'
    cliente_id = db.Column(Integer, ForeignKey('clientes.id'), primary_key=True)
    pedido_detalle_id = db.Column(Integer, ForeignKey('pedidosdetalle.id'), primary_key=True)
    ventas_id = db.Column(Integer, ForeignKey('ventas.id'))
    senia = db.Column(Float)
    entregado = db.Column(Boolean)
    cantidad = db.Column(Integer)


class RepuestoPresupuesto(db.Model):
    __tablename__ = 'repuestospresupuestos'
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    presupuesto_id = db.Column(Integer, ForeignKey('presupuestos.id'), primary_key=True)
    cantidad = db.Column(Integer)


class RepuestoVehiculo(db.Model):
   
    codigo_pieza = db.Column(db.Text, db.ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), primary_key=True)

    # Relaciones
    repuesto = relationship('Repuesto', backref='vehiculos_asociados')
    vehiculo = relationship('Vehiculo', backref='repuestos_asociados')

class VentaRepuesto(db.Model):
    __tablename__ = 'ventasrepuestos'
    venta_id = db.Column(Integer, ForeignKey('ventas.id'), primary_key=True)
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    cantidad = db.Column(Integer)


class VentaMovimiento(db.Model):
    __tablename__ = 'ventasmovimientos'
    venta_id = db.Column(Integer, ForeignKey('ventas.id'), primary_key=True)
    movimiento_id = db.Column(Integer, ForeignKey('movimientos.id'), primary_key=True)
