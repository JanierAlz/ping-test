import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.models import User
from flaskr.database import db_session
from sqlalchemy import select

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user(id):
    user = db_session.scalars(select(User).where(User.id == id)).first()
    return user


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'El correo de usuario es requerido.'
        elif not password:
            error = 'Una clave es requerida.'

        if error is None:
            try:
                user = User(email= email, password=generate_password_hash(password))
                db_session.add(user)
                db_session.commit()
            except:
                error = f"El correo {email} ya se encuentra registrado."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']        
        user = db_session.scalars(select(User).where(User.email == email)).first()
        error = None
        if user is None:
            error = 'Usuario incorrecto.'
        elif not check_password_hash(user.password, password):
            error = 'Clave incorrecta.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user(id=user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

