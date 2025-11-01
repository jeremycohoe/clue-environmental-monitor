"""
Data Logger - Log sensor data to CSV format
============================================

This script logs environmental data to the serial console in CSV format.
You can redirect the output to a file for analysis.

On Linux/Mac:
  screen -L /dev/ttyACM0 115200
  or
  picocom /dev/ttyACM0 -b 115200 | tee data_log.csv

The data can then be imported into Excel, Google Sheets, or analyzed with Python/R.
"""

import time
import board
from adafruit_clue import clue

# Configuration
LOG_INTERVAL = 60  # Log every 60 seconds (1 minute)
TEMP_OFFSET = -1.0  # Your calibration offset

# Print CSV header
print("timestamp,uptime_sec,temperature_c,humidity_pct,pressure_hpa,altitude_m")

start_time = time.monotonic()
log_count = 0

# Set NeoPixel to indicate logging
clue.pixel.brightness = 0.05
clue.pixel.fill((0, 0, 255))

try:
    while True:
        current_time = time.monotonic()
        uptime = int(current_time - start_time)

        # Read sensors
        temp = clue.temperature + TEMP_OFFSET
        humidity = clue.humidity
        pressure = clue.pressure
        altitude = clue.altitude

        # Log in CSV format: timestamp, uptime, temp, humidity, pressure, altitude
        import rtc
        r = rtc.RTC()
        current_dt = r.datetime

        # Format: YYYY-MM-DD HH:MM:SS
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            current_dt.tm_year, current_dt.tm_mon, current_dt.tm_mday,
            current_dt.tm_hour, current_dt.tm_min, current_dt.tm_sec
        )

        print(f"{timestamp},{uptime},{temp:.2f},{humidity:.1f},{pressure:.2f},{altitude:.1f}")

        log_count += 1

        # Blink LED to show activity
        if log_count % 2 == 0:
            clue.pixel.fill((0, 0, 255))
        else:
            clue.pixel.fill((0, 0, 50))

        time.sleep(LOG_INTERVAL)

except KeyboardInterrupt:
    print("# Logging stopped")
    clue.pixel.fill((255, 0, 0))
