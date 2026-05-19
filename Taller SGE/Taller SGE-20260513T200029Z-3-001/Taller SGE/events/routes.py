from utilidades import role_required
from flask import Blueprint, flash, render_template, request, redirect, url_for
from models import Eventos, Registracion
from flask_login import current_user,login_required
from extensions import db
from datetime import datetime


events_bp = Blueprint('events', __name__)

@events_bp.route('/panel-organizador')
@role_required('organizador')
def panel_organizador():
    return render_template('panel_o.html')

@events_bp.route('/crear_evento', methods=['GET', 'POST'])
@role_required('organizador')
def create_event():

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        capacity = request.form.get('capacity')
        category = request.form.get('category')

        N_evento = Eventos(
            titulo = title,
            descripcion = description,
            fecha = date,
            capacidad = capacity,
            categoria = category,
            organizador_id = current_user.id
        )
        db.session.add(N_evento)
        db.session.commit()

        return redirect(url_for('events.listar_eventos'))

    return render_template('crear_evento.html')

@events_bp.route('/eventos-organizador')
@role_required('organizador')
def listar_eventos():
    eventos = Eventos.query.all()

    return render_template('listar_ev.html', eventos = eventos)



@events_bp.route('/eventos-asistente')
@role_required('asistente')
def eventos_a():

    busqueda = request.args.get('busqueda', '')

    categoria = request.args.get('categoria', '')

    eventos = Eventos.query
    if busqueda:

        eventos = eventos.filter(
            Eventos.titulo.ilike(f'%{busqueda}%')
        )

    if categoria:

        eventos = eventos.filter_by(
            categoria=categoria
        )

    eventos = eventos.order_by(
        Eventos.fecha.asc()
    ).all()

    categorias = Eventos.query.with_entities(
        Eventos.categoria
    ).distinct()

    return render_template(
        'eventos.html',
        eventos=eventos,
        categorias=categorias,
        busqueda=busqueda,
        categoria=categoria
    )


@events_bp.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@role_required('organizador')
def editar_ev(id):

    evento = Eventos.query.get_or_404(id)

    if evento.organizador_id != current_user.id:
        return "No tienes permiso"

    if request.method == 'POST':

        evento.titulo = request.form.get('title')

        evento.descripcion = request.form.get('description')

        evento.fecha = datetime.strptime(request.form.get('date'),'%Y-%m-%d').date()

        evento.capacidad = request.form.get('capacity')

        evento.categoria = request.form.get('category')

        db.session.commit()

        return redirect(url_for('events.listar_eventos'))

    return render_template('editar_evento.html', evento = evento)


@events_bp.route('/eliminar_evento/<int:id>')
@role_required('organizador')
def eliminar_evento(id):

    evento = Eventos.query.get_or_404(id)

    if evento.organizador_id != current_user.id:
        return "No tienes permiso"

    db.session.delete(evento)

    db.session.commit()

    return redirect(url_for('events.listar_eventos'))

@events_bp.route('/inscritos/<int:id>')
@role_required('organizador')
def ver_inscritos(id):

    evento = Eventos.query.get_or_404(id)

    if evento.organizador_id != current_user.id:
        return "No tienes permiso"

    inscritos = Registracion.query.filter_by(
        evento_id=id
    ).all()

    return render_template(
        'inscritos.html',
        evento=evento,
        inscritos=inscritos
    )


@events_bp.route('/evento/<int:id>')
@role_required('asistente')
def detalle_evento(id):

    evento = Eventos.query.get_or_404(id)

    inscritos = Registracion.query.filter_by(
        evento_id=evento.id
    ).count()

    usuario_inscrito = Registracion.query.filter_by(
        usuario_id=current_user.id,
        evento_id=evento.id
    ).first()

    cupos_disponibles = evento.capacidad - inscritos

    return render_template(
        'detalle_evento.html',
        evento=evento,
        inscritos=inscritos,
        usuario_inscrito=usuario_inscrito,
        cupos_disponibles=cupos_disponibles
    )


@events_bp.route('/inscribirse/<int:id>')
@role_required('asistente')
def inscribirse_evento(id):

    evento = Eventos.query.get_or_404(id)

    registro_existente = Registracion.query.filter_by(
        usuario_id=current_user.id,
        evento_id=id
    ).first()

    if registro_existente:

        flash(
            'Ya estás inscrito en este evento.',
            'warning'
        )

        return redirect(
            url_for('events.detalle_evento', id=id)
        )

    if evento.fecha < datetime.utcnow().date():

        flash(
            'Este evento ya finalizó.',
            'danger'
        )

        return redirect(
            url_for('events.detalle_evento', id=id)
        )

    inscritos = Registracion.query.filter_by(
        evento_id=id
    ).count()

    if inscritos >= evento.capacidad:

        flash(
            'No hay cupos disponibles.',
            'danger'
        )

        return redirect(
            url_for('events.detalle_evento', id=id)
        )

    nueva_inscripcion = Registracion(
        usuario_id=current_user.id,
        evento_id=id
    )

    db.session.add(nueva_inscripcion)
    db.session.commit()

    flash(
        'Te inscribiste correctamente.',
        'success'
    )

    return redirect(
        url_for('users.mis_eventos')
    )


@events_bp.route('/cancelar-inscripcion/<int:id>')
@role_required('asistente')
def cancelar_inscripcion(id):

    registro = Registracion.query.filter_by(
        usuario_id=current_user.id,
        evento_id=id
    ).first()

    if registro:

        db.session.delete(registro)
        db.session.commit()

        flash(
            'Inscripción cancelada correctamente.',
            'info'
        )

    else:

        flash(
            'No estás inscrito en este evento.',
            'warning'
        )

    return redirect(
        url_for('users.mis_eventos')
    )