
# Mall-Park-360

A comprehensive parking management system designed for shopping malls with role-based dashboards for *Parking Supervisors*, *Parking Officers*, and *Parking Lot Attendants*. 

---

- Features

- **Role-Based Access Control**
  - Parking Supervisors: Full dashboard with analytics and reporting
  - Parking Officers: Monitoring and enforcement
  - Parking Lot Attendants: Slot management and configuration

- **Parking Slot Management**
  - Real-time slot availability tracking
  - Multi-floor and multi-pillar organization
  - Dynamic slot reservation and release
  - Vehicle tracking and parking history

- **Financial Management**
  - Automated ticket generation and payment processing
  - GST (Goods and Services Tax) calculation
  - Revenue analytics and income reports
  - Daily statistics and earnings tracking

- **Real-Time Updates**
  - WebSocket-based live slot updates
  - Instant notification system for all connected clients
  - Synchronized parking status across all interfaces

- **Comprehensive Reporting**
  - Daily parking statistics
  - 7-day income analytics with charts
  - Ticket history and management
  - Payment tracking

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3, Flask, Flask-SocketIO |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite3 |
| **Real-time Communication** | WebSockets (Socket.IO) |
| **API** | RESTful API |
| **Server** | Uvicorn / Gunicorn |
| **Dependencies** | FastAPI, python-multipart |

---


## Project Structure

```bash
Mall-Park-360/
│
├── app.py                  # Main Flask application
├── Requirements            # Python dependencies
├── Setup                   # Installation scripts 
├── Contribution.md         # Contribution 
├── LICENSE                 # MIT License
├── mallpark360.db          # SQLite database 
│
├── static/                 # Frontend files
│   ├── index.html          # Login page
│   ├── supervisor.html     # Parking Supervisor dashboard
│   ├── officer.html        # Parking Officer dashboard
│   ├── attendant.html      # Lot Attendant dashboard
│   └── ticket.html         # Ticket view
│
└── README.md               # Project documentation
```

---

## Installation


### Prerequisites

- Python 3.8 + 
- pip 
- SQLite3 

### Step 1: Clone the Repository

```bash
git clone https://github.com/avnish0709/Mall-Park-360.git
cd Mall-Park-360
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

###Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
- Requirements
  - fastapi = 0.104.1
  - uvicorn = 0.24.0
  - python-multipart = 0.0.6

---

## Configuration

- Parking Layout Configuration
  - Parking Layout Configuration
    - You can configure the parking lot structure by setting:
    - Slots per Floor: Default is 20 slots per floor
    - Number of Floors: Default is 2 floors

  - The system organizes slots by:
    - Floors: Represented as negative numbers (-1, -2, etc.)
    - Pillars: A, B, C, D, E, F (6 pillars, 10 slots each)
    - Slot Numbers: 1-10 per pillar
    
  - Current Configuration:
    - Total Slots: 40 (20 per floor × 2 floors)
    - Floors: 2 (B1, B2)
    - Pillars per Floor: 2 (A, B, C for 20 slots)

---

## Default Credentials 
Default Credentials
Use these credentials to test different roles:

| Role | Email | Password |
|------|-------|----------|
| Supervisor |	supervisor@mallpark360.com | Supervisor@123 |
| Officer	| officer@mallpark360.com | Officer@123 |
| Attendant	| attendant@mallpark360.com	| Attendant@123 |

---

## Running the Application
```bash
python3 app.py
```
- Access the Application
  - Main Portal: http://localhost:5000
  - API Docs: http://localhost:5000/docs

---

## API Documentation

### 1) Authentication Endpoints
- Login

```bash
  POST /api/login
Content-Type: application/json

{
  "email": "supervisor@mallpark360.com",
  "password": "Supervisor@123"
}

Response:
{
  "token": "auth_token_here",
  "role": "supervisor",
  "name": "Rajesh Kumar"
}
```
### 2) Parking Slot Endpoint 

- 1) Get All Slots
  
```bash
GET /api/slots
Authorization: Bearer {token}

Response:
{
  "slots": [
    {
      "id": 1,
      "floor": -1,
      "pillar": "A",
      "slot_num": 1,
      "reserved": 0,
      "vehicle": null,
      "reserved_at": null,
      "ticket": null
    }
  ]
}
```


- 2) Reserve a Slot 

```bash
POST /api/reserve
Authorization: Bearer {token}
Content-Type: application/json

{
  "floor": -1,
  "pillar": "A",
  "slot_num": 1,
  "vehicle": "KA01AB1234"
}

Response:
{
  "ok": true,
  "ticket": {
    "ticket": "MP-12345",
    "payment": "PAY-1234",
    "total": 118
  }
}
```

- 3) Release a Slot 

```Bash
POST /api/release
Authorization: Bearer {token}
Content-Type: application/json

{
  "floor": -1,
  "pillar": "A",
  "slot_num": 1
}
```

### Ticket Endpoints 

- 7-Day Income Report (Supervisor Only)
```Bash
GET /api/stats/income
Authorization: Bearer {token}

Response:
{
  "labels": ["27 May", "28 May", ...],
  "values": [1770, 2360, ...]
}
```

---

## Database Schema (SQL)

### Users Table 
```Bash
CREATE TABLE users(
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE,
  password TEXT,
  role TEXT,
  name TEXT
)
```

### Session Table 
```Bash
CREATE TABLE sessions(
  token TEXT PRIMARY KEY,
  user_id INTEGER,
  created_at TEXT
)
```

### Slots Table

```Bash
CREATE TABLE slots(
  id INTEGER PRIMARY KEY,
  floor INTEGER,
  pillar TEXT,
  slot_num INTEGER,
  reserved INTEGER DEFAULT 0,
  vehicle TEXT,
  reserved_at TEXT,
  ticket TEXT,
  UNIQUE(floor, pillar, slot_num)
)
```

### Tickets Table
```Bash
CREATE TABLE tickets(
  id INTEGER PRIMARY KEY,
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
```

### Configuration Table 
```Bash
CREATE TABLE config(
  id INTEGER PRIMARY KEY,
  slots_per_floor INTEGER,
  floors INTEGER
)
```
