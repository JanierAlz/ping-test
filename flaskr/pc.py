import re
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.database import db_session
from flaskr.models import Pc, Ping
from sqlalchemy import select

bp = Blueprint('pc', __name__)

@bp.route('/')
def index():
    pc = select(Pc)
    """pc = db_session.scalars(pc).all()
    response = [row.to_json() for row in pc]
    return response"""
    return render_template('pc/index.html', pcs=db_session.scalars(pc))



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        ipv4 = request.form['ipv4']
        error = None
        pattern = "https?://"
        if not name or not ipv4:
            error = 'Missing required fields.'

        if error is not None:
            flash(error)
        else:
            ip= re.sub(pattern, "", ipv4)
            pc = Pc(name=name, ipv4=re.sub(pattern, "", ipv4))
            db_session.add(pc)
            db_session.commit()
            return redirect(url_for('pc.index'))

    return render_template('pc/create.html')


def get_pc(id):
    pc = db_session.scalars(select(Pc).where(Pc.id == id)).first()
    return pc


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    pc = get_pc(id)
    pings = db_session.scalars(select(Ping).where(Ping.current_pc_id == id)).all()
    delete = False if len(pings) > 0 else True
    if request.method == 'POST':
        name = request.form['name']
        ipv4 = request.form['ipv4']
        error = None

        pattern = "https?://"
        if not name or not ipv4:
            error = 'Missing required fields.'

        if error is not None:
            flash(error)
        else:
            pc = get_pc(id=id)
            pc.name = name
            pc.ipv4 = re.sub(pattern, "", ipv4)
            db_session.add(pc)
            db_session.commit()
            return redirect(url_for('pc.index'))

    return render_template('pc/update.html', pc=pc, delete=delete )

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    pc = get_pc(id=id)
    ping = db_session.scalars(select(Ping).where(Ping.current_pc_id == id)).all()
    if len(ping) == 0:
        db_session.delete(pc)
        db_session.commit()
    else:
        flash("Se ha realizado una prueba de latencia, el equipo no puede ser eliminado")
        return redirect(url_for('pc.update', id=id))
    return redirect(url_for('pc.index'))