from devices import init_db, add_device
from reports import generate_report
from updater import update_firmware
from security import analyze_device

init_db()

# Exemple : ajouter des appareils
add_device("Sensor1", "192.168.1.2", "1.0.0", "12345678")
add_device("Camera1", "192.168.1.3", "1.2.0", "password123")

# Analyser et mettre à jour les appareils
devices = [(1, "Sensor1", "192.168.1.2", "1.0.0", "12345678", "unknown")]
for d in devices:
    analysis = analyze_device(d)
    if not analysis["up_to_date"]:
        update_firmware(d[0])

# Générer le rapport
generate_report()
