from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
import random
import math
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'mallpark360-secret'

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

DB = 'mallpark360.db'
BASE_RATE = 100
GST = 0.18

hash_password = lambda p: hashlib.sha256(p.encode()).hexdigest()


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    with get_db() as db:

        db.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            name TEXT
        )
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS sessions(
            token TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT
        )
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS config(
            id INTEGER PRIMARY KEY,
            slots_per_floor INTEGER,
            floors INTEGER
        )
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS slots(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER,
            pillar TEXT,
            slot_num INTEGER,
            reserved INTEGER DEFAULT 0,
            vehicle TEXT,
            reserved_at TEXT,
            ticket TEXT,
            UNIQUE(floor,pillar,slot_num)
        )
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT UNIQUE,
            floor INTEGER,
            pillar TEXT,
            slot_num INTEGER,
            vehicle TEXT,
            base REAL,
            gst REAL,
            total REAL,
            payment TEXT,
            created_at TEXT
        )
        ''')

        users = [
            ('supervisor@mallpark360.com', 'Supervisor@123', 'supervisor', 'Rajesh Kumar'),
            ('officer@mallpark360.com', 'Officer@123', 'officer', 'Priya Sharma'),
            ('attendant@mallpark360.com', 'Attendant@123', 'attendant', 'Amit Singh')
        ]

        for u in users:
            db.execute('''
            INSERT OR IGNORE INTO users(email,password,role,name)
            VALUES(?,?,?,?)
            ''', (u[0], hash_password(u[1]), u[2], u[3]))

        db.execute('''
        INSERT OR IGNORE INTO config(id,slots_per_floor,floors)
        VALUES(1,20,2)
        ''')

        count = db.execute('SELECT COUNT(*) c FROM slots').fetchone()['c']

        if count == 0:
            generate_slots(db, 20, 2)

        seed_demo_data(db)


def generate_slots(db, slots_per_floor, floors):

    db.execute('DELETE FROM slots')

    pillars = ['A', 'B', 'C', 'D', 'E', 'F']
    needed = math.ceil(slots_per_floor / 10)

    for f in range(1, floors + 1):

        floor = -f

        for p in range(needed):

            pillar = pillars[p]

            for s in range(1, 11):

                db.execute('''
                INSERT INTO slots(floor,pillar,slot_num)
                VALUES(?,?,?)
                ''', (floor, pillar, s))


def seed_demo_data(db):

    count = db.execute('SELECT COUNT(*) c FROM tickets').fetchone()['c']

    if count > 0:
        return

    for i in range(1, 30):

        dt = datetime.now() - timedelta(days=random.randint(0, 7))

        db.execute('''
        INSERT INTO tickets(
            ticket,floor,pillar,slot_num,
            vehicle,base,gst,total,payment,created_at
        )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (
            f"MP-2026-{i:04}",
            random.choice([-1, -2]),
            random.choice(['A', 'B', 'C']),
            random.randint(1, 10),
            str(random.randint(1000, 9999)),
            100,
            18,
            118,
            f"PAY-{i:04}",
            dt.strftime('%Y-%m-%d %H:%M:%S')
        ))


# ---------------- AUTH ----------------

def get_user():

    token = request.headers.get('Authorization', '')
    token = token.replace('Bearer ', '')

    if not token:
        return None

    with get_db() as db:

        user = db.execute('''
        SELECT users.*
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token=?
        ''', (token,)).fetchone()

    return dict(user) if user else None


def protected():

    user = get_user()

    if not user:
        return None, ({'error': 'Unauthorized'}, 401)

    return user, None


# ---------------- PAGES ----------------

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/attendant')
def attendant():
    return send_from_directory('static', 'attendant.html')


@app.route('/supervisor')
def supervisor():
    return send_from_directory('static', 'supervisor.html')


@app.route('/officer')
def officer():
    return send_from_directory('static', 'officer.html')


@app.route('/ticket')
def ticket():
    return send_from_directory('static', 'ticket.html')


# ---------------- LOGIN ----------------

@app.post('/api/login')
def login():

    data = request.json

    email = data.get('email', '').strip().lower()
    password = hash_password(data.get('password', ''))

    with get_db() as db:

        user = db.execute('''
        SELECT * FROM users
        WHERE email=? AND password=?
        ''', (email, password)).fetchone()

        if not user:
            return {'error': 'Invalid credentials'}, 401

        token = secrets.token_hex(16)

        db.execute('''
        INSERT INTO sessions(token,user_id,created_at)
        VALUES(?,?,?)
        ''', (
            token,
            user['id'],
            datetime.now().isoformat()
        ))

    return {
        'token': token,
        'role': user['role'],
        'name': user['name']
    }


@app.post('/api/logout')
def logout():

    user, err = protected()

    if err:
        return err

    token = request.headers.get('Authorization', '')
    token = token.replace('Bearer ', '')

    with get_db() as db:
        db.execute('DELETE FROM sessions WHERE token=?', (token,))

    return {'ok': True}


@app.get('/api/me')
def me():

    user, err = protected()

    if err:
        return err

    return user


# ---------------- CONFIG ----------------

@app.get('/api/config')
def get_config():

    user, err = protected()

    if err:
        return err

    with get_db() as db:
        config = db.execute('SELECT * FROM config WHERE id=1').fetchone()

    return dict(config)


@app.post('/api/config')
def set_config():

    user, err = protected()

    if err:
        return err

    if user['role'] != 'attendant':
        return {'error': 'Forbidden'}, 403

    data = request.json

    slots = int(data.get('slots_per_floor', 20))
    floors = int(data.get('floors', 2))

    with get_db() as db:

        db.execute('''
        UPDATE config
        SET slots_per_floor=?, floors=?
        WHERE id=1
        ''', (slots, floors))

        generate_slots(db, slots, floors)

        all_slots = db.execute('SELECT * FROM slots').fetchall()

    socketio.emit('slot_update', {
        'slots': [dict(s) for s in all_slots]
    })

    return {'ok': True}


# ---------------- SLOTS ----------------

@app.get('/api/slots')
def get_slots():

    user, err = protected()

    if err:
        return err

    with get_db() as db:

        slots = db.execute('''
        SELECT * FROM slots
        ORDER BY floor,pillar,slot_num
        ''').fetchall()

    return {'slots': [dict(s) for s in slots]}


@app.post('/api/reserve')
def reserve_slot():

    user, err = protected()

    if err:
        return err

    if user['role'] not in ['attendant', 'supervisor']:
        return {'error': 'Forbidden'}, 403

    data = request.json

    floor = data['floor']
    pillar = data['pillar']
    slot = data['slot_num']
    vehicle = data.get('vehicle', '')

    ticket = f"MP-{random.randint(10000,99999)}"
    payment = f"PAY-{random.randint(1000,9999)}"

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    base = BASE_RATE
    gst = round(base * GST, 2)
    total = base + gst

    with get_db() as db:

        row = db.execute('''
        SELECT * FROM slots
        WHERE floor=? AND pillar=? AND slot_num=?
        ''', (floor, pillar, slot)).fetchone()

        if not row:
            return {'error': 'Slot not found'}, 404

        if row['reserved']:
            return {'error': 'Already reserved'}, 400

        db.execute('''
        UPDATE slots
        SET reserved=1,
            vehicle=?,
            reserved_at=?,
            ticket=?
        WHERE floor=? AND pillar=? AND slot_num=?
        ''', (
            vehicle,
            now,
            ticket,
            floor,
            pillar,
            slot
        ))

        db.execute('''
        INSERT INTO tickets(
            ticket,floor,pillar,slot_num,
            vehicle,base,gst,total,payment,created_at
        )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (
            ticket,
            floor,
            pillar,
            slot,
            vehicle,
            base,
            gst,
            total,
            payment,
            now
        ))

        slots_data = db.execute('SELECT * FROM slots').fetchall()

    socketio.emit('slot_update', {
        'slots': [dict(s) for s in slots_data]
    })

    return {
        'ok': True,
        'ticket': {
            'ticket': ticket,
            'payment': payment,
            'total': total
        }
    }


@app.post('/api/release')
def release_slot():

    user, err = protected()

    if err:
        return err

    if user['role'] not in ['attendant', 'supervisor']:
        return {'error': 'Forbidden'}, 403

    data = request.json

    with get_db() as db:

        db.execute('''
        UPDATE slots
        SET reserved=0,
            vehicle=NULL,
            reserved_at=NULL,
            ticket=NULL
        WHERE floor=? AND pillar=? AND slot_num=?
        ''', (
            data['floor'],
            data['pillar'],
            data['slot_num']
        ))

        slots_data = db.execute('SELECT * FROM slots').fetchall()

    socketio.emit('slot_update', {
        'slots': [dict(s) for s in slots_data]
    })

    return {'ok': True}


# ---------------- TICKETS ----------------

@app.get('/api/tickets')
def get_tickets():

    user, err = protected()

    if err:
        return err

    with get_db() as db:

        tickets = db.execute('''
        SELECT * FROM tickets
        ORDER BY id DESC
        ''').fetchall()

    return {'tickets': [dict(t) for t in tickets]}


@app.get('/api/ticket/<ticket>')
def get_ticket(ticket):

    user, err = protected()

    if err:
        return err

    with get_db() as db:

        row = db.execute('''
        SELECT * FROM tickets
        WHERE ticket=?
        ''', (ticket,)).fetchone()

    if not row:
        return {'error': 'Ticket not found'}, 404

    return dict(row)


# ---------------- STATS ----------------

@app.get('/api/stats/today')
def stats_today():

    user, err = protected()

    if err:
        return err

    if user['role'] != 'supervisor':
        return {'error': 'Forbidden'}, 403

    today = datetime.now().strftime('%Y-%m-%d')

    with get_db() as db:

        row = db.execute('''
        SELECT
            COUNT(*) count,
            SUM(base) base,
            SUM(gst) gst,
            SUM(total) total
        FROM tickets
        WHERE date(created_at)=?
        ''', (today,)).fetchone()

    return {
        'count': row['count'] or 0,
        'base': row['base'] or 0,
        'gst': row['gst'] or 0,
        'total': row['total'] or 0
    }


@app.get('/api/stats/income')
def stats_income():

    user, err = protected()

    if err:
        return err

    labels = []
    values = []

    with get_db() as db:

        for i in range(6, -1, -1):

            day = datetime.now() - timedelta(days=i)
            date = day.strftime('%Y-%m-%d')

            total = db.execute('''
            SELECT SUM(total) t
            FROM tickets
            WHERE date(created_at)=?
            ''', (date,)).fetchone()['t']

            labels.append(day.strftime('%d %b'))
            values.append(total or 0)

    return {
        'labels': labels,
        'values': values
    }


# ---------------- SOCKET ----------------

@socketio.on('connect')
def connect():

    with get_db() as db:

        slots = db.execute('''
        SELECT * FROM slots
        ORDER BY floor,pillar,slot_num
        ''').fetchall()

    emit('init', {
        'slots': [dict(s) for s in slots]
    })


# ---------------- MAIN ----------------

if __name__ == '__main__':

    init_db()

    print('MallPark360 running on http://localhost:5000')

    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True
    )
