# Edge-AI Predictive Maintenance for CNC Machines

An IoT-based Edge data acquisition system for CNC machine health monitoring. The system runs automatically at Raspberry Pi boot and continuously logs vibration, temperature, and current data for predictive maintenance and anomaly detection.

---

## 📌 Overview

This project implements a Raspberry Pi–based multi-sensor monitoring system designed for industrial CNC machines. It samples machine health parameters at **50 Hz**, timestamps the readings, and stores structured data locally for further AI-driven analysis.

The collector is designed to run as a **systemd service**, ensuring automatic startup on boot and uninterrupted data collection.

---

## 🧠 Key Features

* Automatic execution at Raspberry Pi boot
* Real-time 50 Hz sensor sampling
* Multi-sensor integration (I2C + ADC + 1-Wire)
* Structured CSV logging with UTC timestamps
* Edge-ready architecture for ML deployment
* GPIO support for LED/Buzzer alerts
* Lightweight and optimized for continuous operation

---

## 🛠 Hardware Stack

* Raspberry Pi
* MPU6050 – Vibration (Accelerometer + Gyroscope)
* DS18B20 – Temperature sensor
* SCT-013 – Current transformer
* ADS1115 – 16-bit ADC

---

## 📊 Data Format

Each record:

```
ts, ax, ay, az, gx, gy, gz, temp_c, adc_raw
```

* Acceleration (g)
* Angular velocity (°/s)
* Temperature (°C)
* Raw current sensor value

---

## 🏗 System Architecture

Sensors → Raspberry Pi (collector.py) → CSV Logging →
Feature Engineering → Edge ML Model → Anomaly Detection → Alerts

---

## 🚀 Deployment

The system is configured as a **systemd service**, allowing:

* Auto-start at boot
* Persistent background execution
* Industrial-grade reliability

Run manually:

```bash
python3 collector.py
```

---

## 🔮 Future Enhancements

* Real-time FFT vibration analysis
* Edge ML inference (TinyML)
* MQTT cloud dashboard integration
* Remaining Useful Life (RUL) estimation
* Intelligent fault alert triggering

---

If you want, I can also generate the actual **systemd service file template** you can include in your repo.
