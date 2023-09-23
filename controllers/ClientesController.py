from http import HTTPStatus
from flask import Blueprint, jsonify, session, Response, request, render_template, redirect, url_for
from models.ClienteModel import cliente_login


clientes = Blueprint("clientes", __name__, url_prefix="/clientes")

@clientes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if 'correo' not in request.form or len(request.form.get('correo').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo correo vacio"}) , HTTPStatus.BAD_REQUEST
        
        if 'password' not in request.form or len(request.form.get('password').strip()) == 0:
            return jsonify({"success": False, "error" : "Campo password vacio"}) , HTTPStatus.BAD_REQUEST
        
        req_correo = request.form.get('correo')
        req_pass = request.form.get('password')
        clienteLoggedo = cliente_login(req_correo, req_pass)
        if clienteLoggedo is None:
            return jsonify({"success": False, "error" : "Usuario o contraseña incorrectos"}) , HTTPStatus.BAD_REQUEST
        
        session['correo'] = req_correo
        return jsonify({"success": True, "message" : "Bienvenido!"}), HTTPStatus.OK

    return render_template("login.html")