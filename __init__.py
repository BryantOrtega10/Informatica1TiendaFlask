from flask import Flask, render_template


app = Flask(__name__)

# Registro de los controladores
# app.register_blueprint(usuario_bp, url_prefix='/usuario')
# app.register_blueprint(sede_bp, url_prefix='/sede')
# app.register_blueprint(reserva_bp, url_prefix='/reserva')
# app.register_blueprint(reportes_bp, url_prefix='/reportes')
# app.register_blueprint(estadisticas_bp, url_prefix='/estadisticas')
@app.route("/",methods=["GET","POST"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)