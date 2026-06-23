'''
Desarrollado por: Ing. Ivan Oviedo. Vanchox® 2025
Adaptado HOME SECURITY
Arquitectura Empresarial Flask + MySQL
'''

from flask import Flask, render_template, session, redirect, url_for

# CONFIG
from Config import Config

# EXTENSIONES
from extensions import mysql, mail, db


# ==============================
# CREAR APP
# ==============================
app = Flask(__name__)
app.config.from_object(Config)


# ==============================
# INICIALIZAR EXTENSIONES
# ==============================
mysql.init_app(app)
mail.init_app(app)
db.init_app(app)


# ==============================
# IMPORTAR BLUEPRINTS (DESPUÉS)
# ==============================
from routes.auth import auth
from routes.admin import admin
from routes.agente import agente
from routes.citas import citas
from routes.avaluos import avaluos
from routes.dashboard_citas import dashboard_citas


# ==============================
# REGISTRAR BLUEPRINTS
# ==============================
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(agente)
app.register_blueprint(citas)
app.register_blueprint(avaluos)
app.register_blueprint(dashboard_citas)


# ==============================
# MODELOS
# ==============================
from models.vivienda import Vivienda


# ==============================
# RUTAS PRINCIPALES
# ==============================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registro')
def registro():
    return render_template('agregarUsuarios.html')


@app.route('/home')
def home_usuario():
    if 'usuario' in session:
        return redirect(url_for('agente.catalogo_publico'))
    return redirect(url_for('index'))


@app.route('/quienes-somos')
def quienes_somos():
    if 'usuario' in session:
        return render_template('clientes/quienes_somos.html')
    return redirect(url_for('index'))


@app.route('/admin')
def admin_menu():
    if session.get('rol') == "ADMIN":
        return render_template('menu.html')
    return redirect(url_for('index'))


from flask import request

@app.route('/viviendasLog')
def viviendas():
    # 1. Capturamos lo que el usuario escribió en el HTML
    loc = request.args.get('localidad')
    tipo = request.args.get('tipo')
    p_max = request.args.get('precio_max')
    hab = request.args.get('habitaciones')

    # 2. Empezamos la consulta base
    query = Vivienda.query

    # 3. Aplicamos los filtros solo si el usuario eligió algo
    if loc:
        query = query.filter(Vivienda.localidad == loc)
    if tipo:
        query = query.filter(Vivienda.tipo_inmueble == tipo)
    if p_max:
        query = query.filter(Vivienda.precio <= float(p_max))
    if hab:
        query = query.filter(Vivienda.habitaciones == int(hab))

    # 4. Ejecutamos la consulta final y la mandamos al HTML
    lista_viviendas = query.all()
    return render_template('viviendasLog.html', viviendas=lista_viviendas)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ==============================
# RUN
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
