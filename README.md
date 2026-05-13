 Run
```bash
docker compose up -d
python3 scripts/sensor_simulator.py
# Access Grafana at http://localhost:3000 (admin/admin)



# IESL Wellhead Monitoring Pipeline

## Industry Context
This project simulates an oil & gas remote monitoring system for wellhead assets (pressure, temperature, flow rate). 


## Architecture

- **Mosquitto (MQTT)** | Lightweight broker — field sensors publish here |
- **Telegraf** | Subscribes to MQTT topics, parses the JSON, ships it to InfluxDB |
- **InfluxDB 2.7** | Time-series database — all that telemetry has to live somewhere |
- **Grafana** | Dashboards with proper oilfield units (psi, °F, barrels/day) |
- **Telegram Alerts** | Pings you when temp or pressure step out of line |

## How to Run

```bash
# Fire up the stack
docker compose up -d

# Start pumping fake sensor data
python3 scripts/sensor_simulator.py

# Kick off Telegram alerting (optional — run in a separate terminal)
python3 alerts/temp_alert.py

# Grafana lives at http://localhost:3000 — login with admin / admin.

## Standard Operating Ranges
These are the baselines for a typical onshore wellhead:

- Temperature: 100–180°F

- Pressure: 800–1,200 psi

- Flow Rate: 200–600 barrels/day

The simulator runs a bit cooler (60–95°F) so alerts are easier to trigger during testing.

# Alerts
alerts/temp_alert.py polls InfluxDB every 10 seconds. If temperature and pressure both stay above threshold for 5 seconds straight, it fires a Telegram message.

Right now it's wired for testing — it'll alert on normal conditions so you don't have to sit around waiting. Flip the comparison operators when you're ready for production.

# Alert flow:

Sensor Simulator → MQTT → Telegraf → InfluxDB → temp_alert.py → Telegram

---

## Final Thoughts 

This was a quick-and-dirty telemetry pipeline — MQTT ingest, time-series storage, dashboards, and alerting, all containerized and ready to demo. The whole thing spins up with one `docker compose` command and starts pushing data within seconds.

It's not production (obviously), but it hits all the beats a real wellhead monitoring system would: sensor ingestion, a proper time-series backend, live dashboards in oilfield units, and alerting routed straight to a phone.

Built, tested, documented. Moving on.



Cheers :))


































