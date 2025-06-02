from .vehiculos_routes import vehiculos_bp
from .vehiculos_routes import vehiculos_bp
from .clientes_routes import clientes_bp
from .repuestos_routes import repuestos_bp
from .pedidos_routes import pedidos_bp
from .presupuestos_routes import presupuestos_bp
from .ventas_routes import ventas_bp
from .cuentas_routes import cuentas_bp
from .movimientos_routes import movimientos_bp
from .pedidosdetalle_routes import pedidosdetalle_bp
from .pedidosclientes_routes import pedidosclientes_bp
from .repuestospresupuestos_routes import repuestospresupuestos_bp
from .repuestosvehiculos_routes import repuestosvehiculos_bp
from .ventasrepuestos_routes import ventasrepuestos_bp
from .ventasmovimientos_routes import ventasmovimientos_bp
# Importar más rutas acá

def register_routes(app):
    app.register_blueprint(vehiculos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(repuestos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(presupuestos_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(cuentas_bp)
    app.register_blueprint(movimientos_bp)
    app.register_blueprint(pedidosdetalle_bp)
    app.register_blueprint(pedidosclientes_bp)
    app.register_blueprint(repuestospresupuestos_bp)
    app.register_blueprint(repuestosvehiculos_bp)
    app.register_blueprint(ventasrepuestos_bp)
    app.register_blueprint(ventasmovimientos_bp)