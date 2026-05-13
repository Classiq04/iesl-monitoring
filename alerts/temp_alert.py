#!/usr/bin/env python3
import requests
import time
from datetime import datetime

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "iesl-super-token-2025"
ORG = "iesl"
BUCKET = "wellhead_data"

TELEGRAM_TOKEN = "8787930755:AAH6uIPccijcOa5tNp30HT940j8KLdj42xA"
TELEGRAM_CHAT_ID = "8593240600"

MAX_ALERTS = 2

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("  Telegram: sent OK")
        else:
            print(f"  Telegram error: {response.status_code}")
    except Exception as e:
        print(f"  Telegram failed: {e}")

def check_sensor(topic):
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -10m)
      |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")
      |> filter(fn: (r) => r["topic"] == "{topic}")
      |> filter(fn: (r) => r["_field"] == "value")
      |> mean()
    '''
    
    try:
        response = requests.post(
            f"{INFLUXDB_URL}/api/v2/query?org={ORG}",
            headers={
                "Authorization": f"Token {INFLUXDB_TOKEN}",
                "Content-Type": "application/vnd.flux",
                "Accept": "application/csv"
            },
            data=query,
            timeout=10
        )
        
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            for line in reversed(lines):
                if not line.startswith("#") and line.strip():
                    cols = line.split(',')
                    if len(cols) >= 6:
                        try:
                            return float(cols[5])
                        except ValueError:
                            pass
        else:
            print(f"  InfluxDB error: {response.status_code}")
    except Exception as e:
        print(f"  InfluxDB connection error: {e}")
    
    return None

print("=" * 60)
print("IESL WELLHEAD ALERT MONITOR - TEST MODE")
print("=" * 60)
print("Standard Wellhead Ranges (Oil & Gas):")
print("  Temperature: 100-180°F")
print("  Pressure:    800-1,200 psi")
print("-" * 60)
print(f"Will send {MAX_ALERTS} alert(s) then shut down")
print("=" * 60)
print()

alert_count = 0
trigger_start = None

while alert_count < MAX_ALERTS:
    temp = check_sensor("iesl/wellhead/temperature")
    pressure = check_sensor("iesl/wellhead/pressure")
    
    if temp is not None and pressure is not None:
        now = datetime.now().strftime("%H:%M:%S")
        temp_r = round(temp, 1)
        pressure_r = round(pressure, 1)
        
        print(f"[{now}] Temp: {temp_r}°F | Pressure: {pressure_r} psi")
        
        if temp > 70 and pressure > 700:
            if trigger_start is None:
                trigger_start = datetime.now()
                print(f"  -> Condition met, timing...")
            else:
                duration = (datetime.now() - trigger_start).total_seconds()
                if duration >= 5:
                    message = (
                        f"🚨 <b>IESL WELLHEAD ALERT</b> 🚨\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n"
                        f"<b>Wellhead:</b> WH-03\n"
                        f"<b>Location:</b> Field Alpha\n"
                        f"<b>Temperature:</b> {temp_r}°F\n"
                        f"<b>Pressure:</b> {pressure_r} psi\n"
                        f"<b>Status:</b> TEST ALERT - SYSTEM OPERATIONAL\n"
                        f"<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n"
                        f"<i>Normal: Temp 100-180°F | Press 800-1200 psi</i>"
                    )
                    send_telegram(message)
                    alert_count += 1
                    print(f"  -> ✓ ALERT {alert_count}/{MAX_ALERTS} SENT")
                    trigger_start = None
                    
                    if alert_count >= MAX_ALERTS:
                        print(f"\nAll {MAX_ALERTS} alerts sent. Done!")
                        break
                    
                    time.sleep(30)
        else:
            if trigger_start is not None:
                print(f"  -> Condition cleared")
                trigger_start = None
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for data... (is sensor_simulator running?)")
    
    time.sleep(10)

print("\nAlert test complete. Have a nice day!!!!! ")
