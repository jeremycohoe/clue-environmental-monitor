"""
Weather Station Display
=======================

A comprehensive weather station that displays:
- Temperature (calibrated)
- Humidity
- Pressure (with trend)
- Altitude
- Compass heading
- Weather forecast based on pressure trends

Uses the full capabilities of the CLUE sensor suite.
"""

import time
import math
import board
import displayio
import terminalio
from adafruit_clue import clue
from adafruit_display_text import label

# Configuration
TEMP_OFFSET = -1.0  # Calibration offset in Celsius
UPDATE_INTERVAL = 5  # Update display every 5 seconds
PRESSURE_HISTORY_SIZE = 12  # Keep 1 hour of pressure data (at 5-min intervals)

# Pressure trend tracking
pressure_history = []
pressure_log_interval = 300  # Log pressure every 5 minutes for trend
last_pressure_log = 0

# Setup display
display = board.DISPLAY
display.brightness = 0.8
screen = displayio.Group()
display.root_group = screen

# Create display elements
# Title
title = label.Label(terminalio.FONT, text="Weather Station", color=0xFFFF00,
                   x=30, y=8, scale=2)
screen.append(title)

# Temperature
temp_label = label.Label(terminalio.FONT, text="Temp: --.-C", color=0xFF6600,
                        x=5, y=40, scale=2)
screen.append(temp_label)

# Humidity
humidity_label = label.Label(terminalio.FONT, text="RH: --.-%%", color=0x00CCFF,
                            x=5, y=65, scale=2)
screen.append(humidity_label)

# Pressure
pressure_label = label.Label(terminalio.FONT, text="P: ----.-hPa", color=0xFFFFFF,
                            x=5, y=90, scale=2)
screen.append(pressure_label)

# Pressure trend
trend_label = label.Label(terminalio.FONT, text="Trend: --", color=0xCCCCCC,
                         x=5, y=115, scale=1)
screen.append(trend_label)

# Altitude
altitude_label = label.Label(terminalio.FONT, text="Alt: ---- m", color=0x88FF88,
                            x=5, y=135, scale=2)
screen.append(altitude_label)

# Compass heading
compass_label = label.Label(terminalio.FONT, text="Heading: ---", color=0xFF88FF,
                           x=5, y=165, scale=2)
screen.append(compass_label)

# Weather forecast
forecast_label = label.Label(terminalio.FONT, text="Forecast: --", color=0xFFAA00,
                            x=5, y=195, scale=1)
screen.append(forecast_label)

# Status
status_label = label.Label(terminalio.FONT, text="Initializing...", color=0x666666,
                          x=5, y=225, scale=1)
screen.append(status_label)

# Helper functions
def get_compass_direction(heading):
    """Convert heading in degrees to compass direction."""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((heading + 11.25) / 22.5) % 16
    return directions[index]

def get_pressure_trend():
    """Calculate pressure trend from history."""
    if len(pressure_history) < 2:
        return "Insufficient data", 0xCCCCCC

    # Calculate trend (hPa per hour)
    oldest = pressure_history[0]
    newest = pressure_history[-1]
    time_span = len(pressure_history) * pressure_log_interval / 3600  # hours

    if time_span == 0:
        return "Calculating...", 0xCCCCCC

    change = newest - oldest
    change_per_hour = change / time_span

    # Interpret the trend
    if change_per_hour > 1.5:
        return "Rising rapidly", 0x00FF00
    elif change_per_hour > 0.5:
        return "Rising", 0x88FF88
    elif change_per_hour > -0.5:
        return "Steady", 0xFFFFFF
    elif change_per_hour > -1.5:
        return "Falling", 0xFF8888
    else:
        return "Falling rapidly", 0xFF0000

def get_weather_forecast():
    """Predict weather based on pressure and trend."""
    if len(pressure_history) < 3:
        return "Collecting data..."

    current_pressure = pressure_history[-1]
    trend = pressure_history[-1] - pressure_history[0]

    # Simple forecast based on pressure and trend
    if current_pressure > 1022:
        if trend > 0:
            return "Clear & stable"
        else:
            return "Clear, changing"
    elif current_pressure > 1012:
        if trend > 2:
            return "Improving"
        elif trend < -2:
            return "Deteriorating"
        else:
            return "Partly cloudy"
    else:
        if trend < -2:
            return "Storm warning!"
        elif trend < 0:
            return "Rain likely"
        else:
            return "Clearing up"

# NeoPixel to indicate status
clue.pixel.brightness = 0.1
clue.pixel.fill((255, 100, 0))  # Orange during startup

print("Weather Station Starting...")
print("Warming up sensors...")
time.sleep(3)

clue.pixel.fill((0, 255, 0))  # Green when ready
print("Ready!")

start_time = time.monotonic()

# Main loop
while True:
    current_time = time.monotonic()
    uptime = int(current_time - start_time)

    # Read sensors
    temperature = clue.temperature + TEMP_OFFSET
    humidity = clue.humidity
    pressure = clue.pressure
    altitude = clue.altitude

    # Calculate compass heading
    mag_x, mag_y, mag_z = clue.magnetic
    heading = math.atan2(mag_y, mag_x) * 180 / math.pi
    if heading < 0:
        heading += 360
    compass_dir = get_compass_direction(heading)

    # Log pressure for trend analysis
    if current_time - last_pressure_log >= pressure_log_interval:
        pressure_history.append(pressure)
        if len(pressure_history) > PRESSURE_HISTORY_SIZE:
            pressure_history.pop(0)
        last_pressure_log = current_time
        print(f"Pressure logged: {pressure:.1f} hPa ({len(pressure_history)} points)")

    # Get pressure trend and forecast
    trend_text, trend_color = get_pressure_trend()
    forecast_text = get_weather_forecast()

    # Update display
    temp_label.text = f"Temp: {temperature:.1f}C"

    # Color-code temperature
    if temperature < 18:
        temp_label.color = 0x0088FF  # Blue - cold
    elif temperature > 26:
        temp_label.color = 0xFF4400  # Orange - hot
    else:
        temp_label.color = 0x00FF00  # Green - comfortable

    humidity_label.text = f"RH: {humidity:.1f}%"

    # Color-code humidity
    if humidity < 30:
        humidity_label.color = 0xFF8800  # Orange - dry
    elif humidity > 70:
        humidity_label.color = 0x0088FF  # Blue - humid
    else:
        humidity_label.color = 0x00CCFF  # Cyan - comfortable

    pressure_label.text = f"P: {pressure:.1f}hPa"
    trend_label.text = f"Trend: {trend_text}"
    trend_label.color = trend_color

    altitude_label.text = f"Alt: {altitude:.0f} m"
    compass_label.text = f"Head: {heading:.0f} {compass_dir}"
    forecast_label.text = f"Fcst: {forecast_text}"

    # Update status
    status_label.text = f"Up: {uptime}s | Pts: {len(pressure_history)}"

    # Print to serial
    print(f"[{uptime:5d}s] T:{temperature:5.1f}C RH:{humidity:4.1f}% "
          f"P:{pressure:7.1f}hPa Alt:{altitude:5.0f}m "
          f"Head:{heading:3.0f}° {forecast_text}")

    # Animate NeoPixel based on weather forecast
    if "Clear" in forecast_text:
        clue.pixel.fill((255, 255, 0))  # Yellow - sunny
    elif "Rain" in forecast_text or "Storm" in forecast_text:
        clue.pixel.fill((0, 0, 255))  # Blue - rainy
    elif "Improving" in forecast_text:
        clue.pixel.fill((0, 255, 0))  # Green - improving
    else:
        clue.pixel.fill((100, 100, 100))  # Gray - overcast

    time.sleep(UPDATE_INTERVAL)
