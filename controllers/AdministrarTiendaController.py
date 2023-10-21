from http import HTTPStatus
from flask import Blueprint, jsonify, session, Response, request, render_template, redirect, url_for
from models.AdministradorModel import login_administrador


admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/", methods=["GET"])
def inicio():
    
    return 'a'

