import pandas as pd
from devices import get_all_devices
from security import analyze_device

def generate_report(filename="iot_report.xlsx"):
    devices = get_all_devices()
    report_data = [analyze_device(d) for d in devices]
    df = pd.DataFrame(report_data)
    df.to_excel(filename, index=False)
    print(f"Report saved to {filename}")
