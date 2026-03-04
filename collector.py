#!/usr/bin/env python3
"""
collector.py
Continuously sample MPU-6050 (accel+gyro), DS18B20 (temp), ADS1115 (current via SCT-013)
and write timestamped raw readings to CSV. Run as a systemd service for persistence.
"""

import time
import csv
import os
from datetime import datetime
import threading

# hardware libs
from smbus2 import SMBus
from w1thermsensor import W1ThermSensor
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

# config
OUT_CSV = "/home/pi/edge_pm/data/raw_readings.csv"
SAMPLE_HZ = 50  # frames per second (adjust as needed)
SAMPLE_INTERVAL = 1.0 / SAMPLE_HZ

# MPU6050 config (I2C)
MPU_ADDR = 0x68

# simple MPU6050 driver (minimal)
class MPU6050:
    def __init__(self, bus=1, addr=MPU_ADDR):
        self.bus = SMBus(bus)
        self.addr = addr
        # wake up sensor
        self.bus.write_byte_data(self.addr, 0x6B, 0)

    def read_raw(self):
        # read accel and gyro registers (big-endian)
        def read_word(reg):
            high = self.bus.read_byte_data(self.addr, reg)
            low = self.bus.read_byte_data(self.addr, reg+1)
            val = (high << 8) + low
            if val >= 0x8000:
                val = -((65535) - val + 1)
            return val
        ax = read_word(0x3B) / 16384.0
        ay = read_word(0x3D) / 16384.0
        az = read_word(0x3F) / 16384.0
        gx = read_word(0x43) / 131.0
        gy = read_word(0x45) / 131.0
        gz = read_word(0x47) / 131.0
        return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}

# temperature sensor (DS18B20)
temp_sensor = W1ThermSensor()

# ADS1115 for current sensor
ads = Adafruit_ADS1x15.ADS1115()
GAIN = 1  # choose gain appropriate for your burden resistor

# LED pins (example)
LED_PIN = 17
BUZZER_PIN = 27

def ensure_csv(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline='') as f:
            writer = csv.writer(f)
            header = ["ts", "ax", "ay", "az", "gx", "gy", "gz", "temp_c", "adc_raw"]
            writer.writerow(header)

def sample_loop():
    mpu = MPU6050()
    ensure_csv(OUT_CSV)
    while True:
        ts = datetime.utcnow().isoformat()
        m = mpu.read_raw()
        try:
            temp_c = temp_sensor.get_temperature()
        except Exception:
            temp_c = None
        try:
            adc_raw = ads.read_adc(0, gain=GAIN)
        except Exception:
            adc_raw = None

        row = [ts, m["ax"], m["ay"], m["az"], m["gx"], m["gy"], m["gz"], temp_c, adc_raw]
        with open(OUT_CSV, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        time.sleep(SAMPLE_INTERVAL)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

if __name__ == "__main__":
    setup_gpio()
    print("Starting collector: writing to", OUT_CSV)
    sample_loop()
