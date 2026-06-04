
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
  "labels": ["29 May", "30 May", ...],
  "values": [1770, 2360, ...]
}
```

---

## Database Schema (SQLite)

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

## Role-Based Features
### Parking Supervisor
  - View comprehensive dashboards with all statistics
  - Monitor daily parking and revenue
  - Access 7-day income analytics
    <img width="1517" height="815" alt="PS-1" src="https://github.com/user-attachments/assets/2de868bb-5411-41db-9071-5241ac95d1c0" />
  - View all tickets and parking history
  - <img width="1521" height="527" alt="PS-2" src="https://github.com/user-attachments/assets/3a6f8fa9-729e-4c01-967d-4191a8eca76c" />
  - Generate reports
  - Permissions: Can clear/reserve slots
    <img width="293" height="157" alt="PS-3" src="https://github.com/user-attachments/assets/799dc1d4-7843-4faf-b103-6ce6b5604b11" />
    <img width="1517" height="392" alt="PS-5" src="https://github.com/user-attachments/assets/b482ef85-86e4-4f5a-9b6b-489764b28414" />
    <img width="291" height="157" alt="PS-4" src="https://github.com/user-attachments/assets/e3fb10af-43f6-478d-a399-00801b562411" />
    <img width="1518" height="345" alt="PS-6" src="https://github.com/user-attachments/assets/94caf5a9-4f85-41b6-a9fc-f02b188330ca" />
  - View all the data

### Parking Officer
  - Monitor parking violations
  - Track vehicle movements
  - Manage enforcement actions
  - Access parking lot overview
  - Permissions: View-only

    <img width="1276" height="717" alt="image" src="https://github.com/user-attachments/assets/5d9c2f51-3c04-42f7-9b6c-8cb85c7dc455" />
    <img width="1536" height="861" alt="PO-1" src="https://github.com/user-attachments/assets/0f663af1-7a93-48f7-9fb4-a0cf2746f91b" />

  ### Parking Lot Attendant
  - Manage slot reservations
  - Release parked vehicles
    <img width="1532" height="864" alt="PLA-1" src="https://github.com/user-attachments/assets/ffd48ef1-949e-4e77-ad18-d2e91bdb5b99" />

  - Configure parking lot layout
  - Adjust slots per floor and number of floors
    <img width="1108" height="607" alt="PLA-2" src="https://github.com/user-attachments/assets/4a3f902a-6d45-43ee-9d21-09657b807383" />
    <img width="1139" height="532" alt="PLA-3" src="https://github.com/user-attachments/assets/85253fec-a879-46da-a9c6-65a0ea644bd4" />
  - Create tickets and manage payments
  - Permissions: Full slot management and configuration
---

## Pricing Model 
- Base Rate: ₹100 per parking session
- GST (18%): Automatically calculated
- Total: Base + GST
  
<img width="523" height="864" alt="Screenshot 2026-06-04 154507" src="https://github.com/user-attachments/assets/4a290ecc-144b-4818-b614-dc246bb3e5a7" />

