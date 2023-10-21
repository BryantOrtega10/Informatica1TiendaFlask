from datetime import datetime
from db import db, ma


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Double, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "imagen", "precio", "descripcion","id_categoria", "stock", "id_proveedor"]


def registrar_producto(nombre, imagen, precio, descripcion):
    producto = Producto(nombre = nombre, imagen = imagen,precio = precio, descripcion=descripcion)
    db.session.add(producto)
    if db.session.commit():
        producto_schema = ProductoSchema()
        return producto_schema.dump(producto)
    return None


def modificar_producto(id, nombre, imagen, precio, descripcion):
    producto = Producto.query.filter_by(id=id).first()
    if producto != None:
        producto.nombre = nombre
        producto.imagen = imagen
        producto.precio = precio
        producto.descripcion = descripcion
        if db.session.commit():
            producto_schema = ProductoSchema()
            return producto_schema.dump(producto)
    return None


def eliminar_producto(id):
    Producto.delete().where(Producto.c.id == id)
    if db.session.commit():
        return True       
    return None


def producto_x_categoria(categoria):    
    productos = Producto.query.filter(Producto.id_categoria == categoria, Producto.stock >= 1).all();
    producto_schema = ProductoSchema()
    productos_res = [producto_schema.dump(producto) for producto in productos]
    return productos_res

def producto_x_id(id_producto):    
    producto = Producto.query.filter_by(id = id_producto).first();
    producto_schema = ProductoSchema()
    producto_res = producto_schema.dump(producto)
    return producto_res


def restar_stock(id_producto,cantidad):    
    producto = Producto.query.filter_by(id = id_producto).first();
    producto.stock -= int(cantidad)
    db.session.commit()
    return True