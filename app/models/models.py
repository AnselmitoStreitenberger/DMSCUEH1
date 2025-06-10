from app.db import db
from sqlalchemy import DateTime, Boolean, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

# ENUM para estado de pedido
estado_enum = ENUM('para pedir', 'pedido', 'recibido','sin stock fabrica','incompleto', name='estado', create_type=False)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(Text)
    ano = db.Column(Text)  # ← lo corregí a TEXT como pediste
    codigo_manual = db.Column(Text)

    repuestos_asociados = relationship('RepuestoVehiculo', back_populates='vehiculo')

class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    codigo_pieza = db.Column(Text, primary_key=True)
    descripcion = db.Column(Text)
    precio = db.Column(Float)
    stock_min = db.Column(Integer)
    stock_real = db.Column(Integer)
    stock_disp = db.Column(Integer)

    vehiculos_asociados = relationship('RepuestoVehiculo', back_populates='repuesto')


class RepuestoVehiculo(db.Model):
    __tablename__ = 'repuestosvehiculos'
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    vehiculo_id = db.Column(Integer, ForeignKey('vehiculos.id'), primary_key=True)

    repuesto = relationship('Repuesto', back_populates='vehiculos_asociados')
    vehiculo = relationship('Vehiculo', back_populates='repuestos_asociados')


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
    direccion = db.Column(Text)
    correo_electronico = db.Column(Text)


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
    cantidad_recibida = db.Column(Integer)


class PedidoCliente(db.Model):
    __tablename__ = 'pedidosclientes'
    cliente_id = db.Column(Integer, ForeignKey('clientes.id'), primary_key=True)
    pedido_detalle_id = db.Column(Integer, ForeignKey('pedidosdetalle.id'), primary_key=True)
    ventas_id = db.Column(Integer, ForeignKey('ventas.id'))
    senia = db.Column(Float)
    entregado = db.Column(Boolean)
    cantidad = db.Column(Integer)
    fecha_creacion = db.Column(DateTime)
    cantidad_recibida = db.Column(Integer)


class RepuestoPresupuesto(db.Model):
    __tablename__ = 'repuestospresupuestos'
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    presupuesto_id = db.Column(Integer, ForeignKey('presupuestos.id'), primary_key=True)
    cantidad = db.Column(Integer)


class VentaRepuesto(db.Model):
    __tablename__ = 'ventasrepuestos'
    venta_id = db.Column(Integer, ForeignKey('ventas.id'), primary_key=True)
    codigo_pieza = db.Column(Text, ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    cantidad = db.Column(Integer)


class VentaMovimiento(db.Model):
    __tablename__ = 'ventasmovimientos'
    venta_id = db.Column(Integer, ForeignKey('ventas.id'), primary_key=True)
    movimiento_id = db.Column(Integer, ForeignKey('movimientos.id'), primary_key=True)
    
class RepuestoCompatible(db.Model):
    __tablename__ = 'repuestoscompatibles'

    codigo_pieza_1 = db.Column(Text, db.ForeignKey('repuestos.codigo_pieza'), primary_key=True)
    codigo_pieza_2 = db.Column(Text, db.ForeignKey('repuestos.codigo_pieza'), primary_key=True)

    __table_args__ = (
        db.CheckConstraint('codigo_pieza_1 < codigo_pieza_2', name='check_orden_codigo_pieza'),
    )

    repuesto_1 = relationship('Repuesto', foreign_keys=[codigo_pieza_1])
    repuesto_2 = relationship('Repuesto', foreign_keys=[codigo_pieza_2])
