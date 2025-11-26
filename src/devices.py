import sqlite3

DB_NAME = "iot_devices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  ip TEXT,
                  firmware_version TEXT,
                  password TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def add_device(name, ip, firmware_version, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO devices (name, ip, firmware_version, password, status) VALUES (?, ?, ?, ?, ?)",
              (name, ip, firmware_version, password, "unknown"))
    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    devices = c.fetchall()
    conn.close()
    return devices
