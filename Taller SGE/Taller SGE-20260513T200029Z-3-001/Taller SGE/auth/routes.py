from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuarios
from extensions import db
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():   
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Usuarios.query.filter_by(email=email).first()

        if user is None:
            return "Usuario no encontrado"

        if check_password_hash(user.password_hash, password):

            login_user(user)

            if user.rol == 'organizador':
                return redirect(url_for('events.panel_organizador'))

            elif user.rol == 'asistente':
                return redirect(url_for('users.panel_asistente'))

        else:
            return "Contraseña incorrecta"

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('auth.login'))



@auth_bp.route('/sign_up', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        bio = request.form['bio']

        password_hash = generate_password_hash(password)

        N_usuario = Usuarios(
            username = username,
            email = email,
            password_hash = password_hash,
            rol = rol,
            bio = bio
        )

        db.session.add(N_usuario)
        db.session.commit()

        flash('Usuario registrado correctamente', 'exito')

        return redirect(url_for('auth.login')) 

    return render_template('sign_up.html')