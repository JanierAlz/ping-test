from flask import (
    Blueprint, flash,render_template, request
)
from werkzeug.exceptions import abort
from .pc import get_pc
from flaskr.auth import login_required
from flaskr.db import get_db
from pythonping import ping

bp = Blueprint('ping', __name__)

@bp.route('/<int:id>/history')
@login_required
def index(id):
    db = get_db()
    history = db.execute(
        'SELECT History.id, success, sent, lost, History.created, pc_id, PC.name, PC.ipv4 '
        ' FROM ping History JOIN pc PC ON History.pc_id = PC.id '
        ' WHERE PC.id = ?'
        ' ORDER BY History.created DESC ',
        (id,)
    ).fetchall()
    return render_template('ping/index.html', pings=history)



@bp.route('/<int:id>/ping')
@login_required
def create(id):
    ping_stats = {}
    pc = get_pc(id=id)
    error = None
    if pc is None:
        error = "PC no se encuentra"
    if error:
        flash(error)
    ping_pc = ping(pc['ipv4'])
    ping_stats["success"] = False if ping_pc.stats_lost_ratio == 1 else True
    ping_stats["lost"] = ping_pc.stats_packets_lost
    ping_stats["sent"] = ping_pc.stats_packets_sent
    ping_stats["max_ms"] = ping_pc.rtt_max_ms
    ping_stats["min_ms"] = ping_pc.rtt_min_ms
    ping_stats["avg_ms"] = ping_pc.rtt_min_ms
    ping_stats["pc_id"] = pc["id"]
    db = get_db()
    db.execute(
        'INSERT INTO ping (success, lost, sent, max_ms, min_ms, avg_ms, pc_id)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?)',
        (ping_stats["success"], ping_stats["lost"], ping_stats["sent"], 
        ping_stats["max_ms"], ping_stats["min_ms"], ping_stats["avg_ms"], ping_stats["pc_id"])
    )
    db.commit()
    ping_stats["name"] = pc["name"]
    ping_stats["ipv4"] = pc["ipv4"]
    return render_template('ping/ping.html', ping=ping_stats)

