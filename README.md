# IESL Wellhead Monitoring Pipeline

A real-time telemetry stack for monitoring wellhead assets pressure, temperature, and flow rate. Built to mirror the kind of monitoring International Energy Services Limited runs in the field.


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
```
```bash
# Start the sensor simulator
python3 scripts/sensor_simulator.py
```
```bash
# Kick off Telegram alerting (separate terminal)
python3 alerts/temp_alert.py
```

> Grafana is at **http://localhost:3000** — login with default username and password (admin/admin)
                                                                                                     
## Standard Operating Ranges

Baselines for a typical onshore wellhead:

| Metric | Normal Range |
|--------|-------------|
| **Temperature** | 100–180°F |
| **Pressure** | 800–1,200 psi |
| **Flow Rate** | 200–600 barrels/day |

> The simulator runs cooler (60–95°F) so alerts trigger more often during testing.
                                                                                                    

## Alerts

`alerts/temp_alert.py` polls InfluxDB every **10 seconds**. If temperature and pressure both stay above threshold for **5 seconds** straight, it fires a Telegram alert.

Currently wired for testing — it alerts on **normal** conditions so you see results immediately. Flip the comparison operators for production use.

### Alert Pipeline

```
**Sensor Simulator → MQTT → Telegraf → InfluxDB → temp_alert.py → Telegram**
```


## Project Structure

```
iesl-monitoring/
├── docker-compose.yml
├── telegraf.conf
├── README.md
├── .gitignore
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
├── scripts/
│   └── sensor_simulator.py
├── alerts/
│   └── temp_alert.py
└── screenshots/
    ├── grafana-dashboard.png
    └── telegram-alert.png
```


## Final Thoughts

This was a quick-and-dirty telemetry pipeline....... MQTT ingest, time-series storage, dashboards, and alerting, all containerized and ready to demo. The whole thing spins up with one `docker compose` command and starts pushing data within seconds.
It's not production (obviously), but it hits all the beats a real wellhead monitoring system would: sensor ingestion, a proper time-series backend, live dashboards in oilfield units, and alerting routed straight to a phone.

Built, tested, documented. Moving on.

Cheers :)






















