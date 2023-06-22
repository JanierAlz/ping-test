from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('pc', __name__)

@bp.route('/')
def index():
    db = get_db()
    pc = db.execute(
        'SELECT id, name, created, ipv4'
        ' FROM pc '
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('pc/index.html', pcs=pc)


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
            db = get_db()
            db.execute(
                'INSERT INTO pc (name, ipv4)'
                ' VALUES (?, ?)',
                (name, ipv4)
            )
            db.commit()
            return redirect(url_for('pc.index'))

    return render_template('pc/create.html')


def get_pc(id):
    pc = get_db().execute(
        'SELECT id, name, ipv4, created '
        ' FROM pc '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

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
            db = get_db()
            db.execute(
                'UPDATE pc SET name = ?, ipv4 = ?'
                ' WHERE id = ?',
                (name, ipv4, id)
            )
            db.commit()
            return redirect(url_for('pc.index'))

    return render_template('pc/update.html', pc=pc)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_pc(id)
    db = get_db()
    db.execute('DELETE FROM pc WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('pc.index'))