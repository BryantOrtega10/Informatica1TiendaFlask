from flask import Flask, render_template
from controllers.ClientesController import clientes
from controllers.TiendaController import tienda
from controllers.VentasController import ventas
from controllers.AdministradorController import administrador
from controllers.AdministrarTiendaController import admin

from config.config import DevelpmentConfig, ProductionConfig
from flask_migrate import Migrate, upgrade
from db import db, ma
from flask_wtf import CSRFProtect


ACTIVE_ENDPOINTS = [('/clientes',clientes), 
                    ('/',tienda), 
                    ('/carrito',ventas), 
                    ('/administrador',administrador),
                    ('/admin',admin)]


def create_app(config=ProductionConfig):
    app = Flask(__name__)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)    
    csrf.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    
    # Agregar los blueprints
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    
    app_flask.run()
