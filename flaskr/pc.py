from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.database import db_session
from flaskr.models import Pc
from sqlalchemy import select

bp = Blueprint('pc', __name__)

@bp.route('/')
def index():
    pc = select(Pc)
    return render_template('pc/index.html', pcs=db_session.scalars(pc))


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        ipv4 = request.form['ipv4']
        error = None

        if not name or not ipv4:
            error = 'Missing required fields.'

        if error is not None:
            flash(error)
        else:
            pc = Pc(name=name, ipv4=ipv4)
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

    if request.method == 'POST':
        name = request.form['name']
        ipv4 = request.form['ipv4']
        error = None
        if not name or not ipv4:
            error = 'Missing required fields.'

        if error is not None:
            flash(error)
        else:
            pc = get_pc(id=id)
            pc.name = name
            pc.ipv4 = ipv4
            db_session.add(pc)
            db_session.commit()
            return redirect(url_for('pc.index'))

    return render_template('pc/update.html', pc=pc)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    pc = get_pc(id=id)
    db_session.delete(pc)
    db_session.commit()
    return redirect(url_for('pc.index'))