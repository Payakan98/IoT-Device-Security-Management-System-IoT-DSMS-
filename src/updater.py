import sqlite3

DB_NAME = "iot_devices.db"

def update_firmware(device_id, new_version="1.2.0"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE devices SET firmware_version = ? WHERE id = ?", (new_version, device_id))
    conn.commit()
    conn.close()
