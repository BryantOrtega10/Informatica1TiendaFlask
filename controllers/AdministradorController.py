from http import HTTPStatus
from flask import Blueprint, jsonify, session, Response, request, render_template, redirect, url_for
from models.AdministradorModel import login_administrador


administrador = Blueprint("administrador", __name__, url_prefix="/administrador")

@administrador.route("/loggout", methods=["GET"])
def loggout():
    del session['a_correo'];
    del session['a_id'];
    return redirect(url_for('tienda.inicio'))

@administrador.route("/login", methods=["GET", "POST"])
def login():
    if 'c_correo' in session:
        return redirect(url_for('admin.inicio'))
    
    if request.method == "POST":
        if 'correo' not in request.form or len(request.form.get('correo').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo correo vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'contrasena' not in request.form or len(request.form.get('contrasena').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo password vacio"}) , HTTPStatus.BAD_REQUEST
        
        req_correo = request.form.get('correo')
        req_contrasena = request.form.get('contrasena')
        clienteLoggedo = login_administrador(req_correo, req_contrasena)
        if clienteLoggedo is None:
            return jsonify({"success": False, "error" : "Usuario o contraseña incorrectos"}) , HTTPStatus.BAD_REQUEST
        
        session['c_correo'] = req_correo
        session['c_id'] = clienteLoggedo["id"]
        return jsonify({"success": True, "message" : "Bienvenido!"}), HTTPStatus.OK

    return render_template("admin_login.html")
