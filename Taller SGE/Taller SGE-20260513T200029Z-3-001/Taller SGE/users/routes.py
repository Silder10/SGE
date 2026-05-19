from utilidades import role_required
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from models import Eventos, Registracion
from extensions import db



users_bp = Blueprint('users', __name__)

@users_bp.route('/panel-asistente')
@role_required('asistente')
def panel_asistente():

    eventos_inscritos = Registracion.query.filter_by(
        usuario_id=current_user.id
    ).count()

    eventos_disponibles = Eventos.query.count()

    return render_template(
        'panel_a.html',
        eventos_inscritos=eventos_inscritos,
        eventos_disponibles=eventos_disponibles
    )


@users_bp.route('/mis-eventos')
@role_required('asistente')
def mis_eventos():

    registros = Registracion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        'mis_eventos.html',
        registros=registros
    )


@users_bp.route('/perfil')
@role_required('asistente')
def perfil():

    return render_template(
        'perfil.html',
        usuario=current_user
    )


@users_bp.route('/editar-perfil', methods=['GET', 'POST'])
@role_required('asistente')
def editar_perfil():

    if request.method == 'POST':

        current_user.username = request.form['username']
        current_user.bio = request.form['bio']

        db.session.commit()

        return redirect(url_for('users.perfil'))

    return render_template(
        'editar_perfil.html',
        usuario=current_user
    )

