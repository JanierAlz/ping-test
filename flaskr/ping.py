from flask import (
    Blueprint, flash,render_template
)
from flaskr.auth import login_required
from pythonping import ping
from flaskr.database import db_session
from flaskr.models import Ping, Pc
from sqlalchemy import desc

bp = Blueprint('ping', __name__)

@bp.route('/<int:id>/history')
@login_required
def index(id):
    pc = Pc.query.filter(Pc.id == id).first()
    history = Ping.query.join(Pc, Ping.pc_id == Pc.id).filter(Pc.id == id, Pc.disabled== False).order_by(desc(Ping.created)).all()
    return render_template('ping/index.html', pings=history, pc=pc)


@bp.route('/<int:id>/ping')
@login_required
def create(id):
    ping_stats = {}
    pc = Pc.query.filter(Pc.id == id).first()
    error = None
    if pc is None:
        error = "PC no se encuentra"
    if error:
        flash(error)
    ping_pc = ping(pc.ipv4)
    ping_stats = Ping()
    ping_stats.success = False if ping_pc.stats_lost_ratio == 1 else True
    ping_stats.lost = ping_pc.stats_packets_lost
    ping_stats.sent = ping_pc.stats_packets_sent
    ping_stats.max_ms = ping_pc.rtt_max_ms
    ping_stats.min_ms  = ping_pc.rtt_min_ms
    ping_stats.avg_ms =  ping_pc.rtt_avg_ms
    ping_stats.pc_id = pc.id
    db_session.add(ping_stats)
    db_session.commit()
    return render_template('ping/ping.html', ping=ping_stats, pc=pc)

