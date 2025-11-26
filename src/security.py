def check_password_strength(password):
    return len(password) >= 8

def check_firmware_version(firmware_version, latest_version="1.2.0"):
    return firmware_version == latest_version

def analyze_device(device):
    _, name, ip, firmware, password, _ = device
    strong_password = check_password_strength(password)
    up_to_date = check_firmware_version(firmware)
    status = "Secure" if strong_password and up_to_date else "Vulnerable"
    return {"name": name, "ip": ip, "strong_password": strong_password, "up_to_date": up_to_date, "status": status}
