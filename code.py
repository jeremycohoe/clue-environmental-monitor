"""
Adafruit CLUE - Calibrated Environmental Monitor
=================================================

Features:
- Temperature with calibration offset
- Humidity monitoring
- Pressure and altitude
- Historical trending (2 hours)
- Visual feedback with color-coded warnings
- Button controls for display modes

Buttons:
- Button A: Cycle through display modes
- Button B: Toggle between Celsius and Fahrenheit

Author: Created for CLUE sensor project
Date: November 2025
"""

import time
import board
import displayio
import terminalio
from adafruit_clue import clue
from adafruit_display_text import label

# ============================================
# CONFIGURATION - ADJUST THESE VALUES
# ============================================

# Temperature calibration offset (in Celsius)
# Calibrated: 2025-11-01 - Reference 27.5C, Raw sensor averaged to ~30.9C
# Offset calculated by calibrate_interactive.py
TEMP_OFFSET = -3.4  # Exact calibration from sensor readings

# Update interval in seconds
UPDATE_INTERVAL = 2  # Display updates every 2 seconds

# Data logging interval in seconds
LOG_INTERVAL = 60  # Log data point every minute

# Historical data size (number of readings to keep)
HISTORY_SIZE = 120  # 120 readings = 2 hours at 1-minute intervals

# Comfort zone thresholds
TEMP_MIN_COMFORT = 20.0  # Celsius
TEMP_MAX_COMFORT = 24.0  # Celsius
HUMIDITY_MIN_COMFORT = 30.0  # Percentage
HUMIDITY_MAX_COMFORT = 60.0  # Percentage

# ============================================
# GLOBAL VARIABLES
# ============================================

# Historical data storage
temp_history = [None] * HISTORY_SIZE
humidity_history = [None] * HISTORY_SIZE
pressure_history = [None] * HISTORY_SIZE

# Tracking variables
history_index = 0
last_log_time = 0
uptime_seconds = 0
use_fahrenheit = False
display_mode = 0  # 0: Main, 1: Trends, 2: Stats

# Button state tracking
button_a_pressed = False
button_b_pressed = False

# ============================================
# DISPLAY SETUP
# ============================================

display = board.DISPLAY
display.brightness = 0.7  # Adjust brightness (0.0 to 1.0)

# Create display groups for different modes
main_group = displayio.Group()
trends_group = displayio.Group()
stats_group = displayio.Group()

# Start with main display
display.root_group = main_group

# ============================================
# HELPER FUNCTIONS
# ============================================

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32

def get_calibrated_temperature():
    """Get temperature with calibration offset applied."""
    raw_temp = clue.temperature
    calibrated_temp = raw_temp + TEMP_OFFSET
    return calibrated_temp

def get_temp_color(temp):
    """Return color based on temperature comfort level."""
    if temp < TEMP_MIN_COMFORT:
        return 0x0099FF  # Blue - too cold
    elif temp > TEMP_MAX_COMFORT:
        return 0xFF4400  # Orange/Red - too hot
    else:
        return 0x00FF00  # Green - comfortable

def get_humidity_color(humidity):
    """Return color based on humidity comfort level."""
    if humidity < HUMIDITY_MIN_COMFORT:
        return 0xFFAA00  # Orange - too dry
    elif humidity > HUMIDITY_MAX_COMFORT:
        return 0x0099FF  # Blue - too humid
    else:
        return 0x00FF00  # Green - comfortable

def calculate_trend(data):
    """Calculate trend from historical data."""
    valid_data = [d for d in data if d is not None]
    if len(valid_data) < 2:
        return "Insufficient data"

    # Compare recent average to older average
    mid_point = len(valid_data) // 2
    old_avg = sum(valid_data[:mid_point]) / mid_point
    new_avg = sum(valid_data[mid_point:]) / len(valid_data[mid_point:])

    diff = new_avg - old_avg

    if abs(diff) < 0.2:  # Within 0.2 units - stable
        return "Stable"
    elif diff > 0:
        return f"Rising +{diff:.1f}"
    else:
        return f"Falling {diff:.1f}"

def get_stats(data):
    """Calculate min, max, and average from historical data."""
    valid_data = [d for d in data if d is not None]
    if not valid_data:
        return None, None, None

    return min(valid_data), max(valid_data), sum(valid_data) / len(valid_data)

def format_uptime(seconds):
    """Format uptime as human-readable string."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

# ============================================
# DISPLAY MODE: MAIN VIEW
# ============================================

def setup_main_display():
    """Setup the main display view."""
    # Clear group
    while len(main_group) > 0:
        main_group.pop()

    # Title
    title = label.Label(terminalio.FONT, text="CLUE Monitor", color=0xFFFFFF,
                       x=60, y=8, scale=2)
    main_group.append(title)

    # Temperature label
    temp_label = label.Label(terminalio.FONT, text="Temp: --.-C", color=0xFFFFFF,
                            x=5, y=40, scale=2)
    main_group.append(temp_label)

    # Humidity label
    humidity_label = label.Label(terminalio.FONT, text="RH: --.-%%", color=0xFFFFFF,
                                x=5, y=70, scale=2)
    main_group.append(humidity_label)

    # Pressure label
    pressure_label = label.Label(terminalio.FONT, text="P: ---- hPa", color=0xFFFFFF,
                                x=5, y=100, scale=2)
    main_group.append(pressure_label)

    # Altitude label
    altitude_label = label.Label(terminalio.FONT, text="Alt: ---- m", color=0xFFFFFF,
                                x=5, y=130, scale=2)
    main_group.append(altitude_label)

    # Status info (small text)
    status_label = label.Label(terminalio.FONT, text="Uptime: --", color=0x888888,
                              x=5, y=170, scale=1)
    main_group.append(status_label)

    # Help text
    help_label = label.Label(terminalio.FONT, text="A:Mode B:C/F", color=0x666666,
                            x=5, y=225, scale=1)
    main_group.append(help_label)

    return main_group

def update_main_display(temp, humidity, pressure, altitude):
    """Update the main display with current readings."""
    # Temperature (index 1)
    temp_str = f"{temp:.1f}"
    unit = "F" if use_fahrenheit else "C"
    main_group[1].text = f"Temp: {temp_str}{chr(176)}{unit}"
    main_group[1].color = get_temp_color(temp if not use_fahrenheit else (temp - 32) * 5/9)

    # Humidity (index 2)
    main_group[2].text = f"RH: {humidity:.1f}%"
    main_group[2].color = get_humidity_color(humidity)

    # Pressure (index 3)
    main_group[3].text = f"P: {pressure:.0f} hPa"
    main_group[3].color = 0xFFFFFF

    # Altitude (index 4)
    main_group[4].text = f"Alt: {altitude:.0f} m"
    main_group[4].color = 0xFFFFFF

    # Status (index 5)
    main_group[5].text = f"Uptime: {format_uptime(uptime_seconds)}"

# ============================================
# DISPLAY MODE: TRENDS VIEW
# ============================================

def setup_trends_display():
    """Setup the trends display view."""
    while len(trends_group) > 0:
        trends_group.pop()

    # Title
    title = label.Label(terminalio.FONT, text="Trends", color=0xFFFFFF,
                       x=80, y=8, scale=2)
    trends_group.append(title)

    # Temperature trend
    temp_trend_label = label.Label(terminalio.FONT, text="Temp: --", color=0xFFFFFF,
                                   x=5, y=40, scale=2)
    trends_group.append(temp_trend_label)

    # Humidity trend
    humidity_trend_label = label.Label(terminalio.FONT, text="RH: --", color=0xFFFFFF,
                                       x=5, y=80, scale=2)
    trends_group.append(humidity_trend_label)

    # Pressure trend
    pressure_trend_label = label.Label(terminalio.FONT, text="Pres: --", color=0xFFFFFF,
                                       x=5, y=120, scale=2)
    trends_group.append(pressure_trend_label)

    # Data points info
    info_label = label.Label(terminalio.FONT, text="-- data points", color=0x888888,
                            x=5, y=170, scale=1)
    trends_group.append(info_label)

    # Help text
    help_label = label.Label(terminalio.FONT, text="A:Mode B:C/F", color=0x666666,
                            x=5, y=225, scale=1)
    trends_group.append(help_label)

    return trends_group

def update_trends_display():
    """Update the trends display."""
    temp_trend = calculate_trend(temp_history)
    humidity_trend = calculate_trend(humidity_history)
    pressure_trend = calculate_trend(pressure_history)

    valid_points = sum(1 for x in temp_history if x is not None)

    trends_group[1].text = f"Temp: {temp_trend}"
    trends_group[2].text = f"RH: {humidity_trend}"
    trends_group[3].text = f"Pres: {pressure_trend}"
    trends_group[4].text = f"{valid_points} data points"

# ============================================
# DISPLAY MODE: STATISTICS VIEW
# ============================================

def setup_stats_display():
    """Setup the statistics display view."""
    while len(stats_group) > 0:
        stats_group.pop()

    # Title
    title = label.Label(terminalio.FONT, text="Statistics", color=0xFFFFFF,
                       x=60, y=8, scale=2)
    stats_group.append(title)

    # Temperature stats
    temp_stats_label = label.Label(terminalio.FONT, text="Temp: --/--/--", color=0xFFFFFF,
                                   x=5, y=40, scale=1)
    stats_group.append(temp_stats_label)

    # Humidity stats
    humidity_stats_label = label.Label(terminalio.FONT, text="RH: --/--/--", color=0xFFFFFF,
                                       x=5, y=70, scale=1)
    stats_group.append(humidity_stats_label)

    # Pressure stats
    pressure_stats_label = label.Label(terminalio.FONT, text="Pres: --/--/--", color=0xFFFFFF,
                                       x=5, y=100, scale=1)
    stats_group.append(pressure_stats_label)

    # Labels for min/avg/max
    legend_label = label.Label(terminalio.FONT, text="(min/avg/max)", color=0x888888,
                              x=5, y=130, scale=1)
    stats_group.append(legend_label)

    # Calibration info
    cal_label = label.Label(terminalio.FONT, text=f"Offset: {TEMP_OFFSET:+.1f}C",
                           color=0x888888, x=5, y=160, scale=1)
    stats_group.append(cal_label)

    # Help text
    help_label = label.Label(terminalio.FONT, text="A:Mode B:C/F", color=0x666666,
                            x=5, y=225, scale=1)
    stats_group.append(help_label)

    return stats_group

def update_stats_display():
    """Update the statistics display."""
    temp_min, temp_max, temp_avg = get_stats(temp_history)
    humidity_min, humidity_max, humidity_avg = get_stats(humidity_history)
    pressure_min, pressure_max, pressure_avg = get_stats(pressure_history)

    if temp_min is not None:
        unit = "F" if use_fahrenheit else "C"
        if use_fahrenheit:
            temp_min = celsius_to_fahrenheit(temp_min)
            temp_max = celsius_to_fahrenheit(temp_max)
            temp_avg = celsius_to_fahrenheit(temp_avg)

        stats_group[1].text = f"Temp: {temp_min:.1f}/{temp_avg:.1f}/{temp_max:.1f}{unit}"
        stats_group[2].text = f"RH: {humidity_min:.0f}/{humidity_avg:.0f}/{humidity_max:.0f}%"
        stats_group[3].text = f"P: {pressure_min:.0f}/{pressure_avg:.0f}/{pressure_max:.0f}hPa"

# ============================================
# INITIALIZATION
# ============================================

# Setup all display modes
setup_main_display()
setup_trends_display()
setup_stats_display()

# Set NeoPixel to indicate startup
clue.pixel.brightness = 0.1
clue.pixel.fill((0, 0, 255))  # Blue during startup

print("=" * 50)
print("Adafruit CLUE - Calibrated Environmental Monitor")
print("=" * 50)
print(f"Temperature offset: {TEMP_OFFSET:+.1f}C")
print(f"Update interval: {UPDATE_INTERVAL}s")
print(f"Log interval: {LOG_INTERVAL}s")
print(f"History size: {HISTORY_SIZE} readings")
print("=" * 50)

# Warm-up period
print("Warming up sensors (5 seconds)...")
time.sleep(5)

clue.pixel.fill((0, 255, 0))  # Green when ready
print("Ready! Starting measurements...\n")

# ============================================
# MAIN LOOP
# ============================================

start_time = time.monotonic()

while True:
    current_time = time.monotonic()
    uptime_seconds = int(current_time - start_time)

    # Read sensors
    calibrated_temp = get_calibrated_temperature()
    humidity = clue.humidity
    pressure = clue.pressure
    altitude = clue.altitude

    # Convert temperature if needed
    display_temp = celsius_to_fahrenheit(calibrated_temp) if use_fahrenheit else calibrated_temp

    # Log data at specified interval
    if current_time - last_log_time >= LOG_INTERVAL:
        temp_history[history_index] = calibrated_temp
        humidity_history[history_index] = humidity
        pressure_history[history_index] = pressure

        history_index = (history_index + 1) % HISTORY_SIZE
        last_log_time = current_time

        # Print to serial console
        print(f"[{format_uptime(uptime_seconds)}] T: {calibrated_temp:.1f}C, RH: {humidity:.1f}%, P: {pressure:.0f}hPa, Alt: {altitude:.0f}m")

    # Update current display mode
    if display_mode == 0:
        update_main_display(display_temp, humidity, pressure, altitude)
    elif display_mode == 1:
        update_trends_display()
    elif display_mode == 2:
        update_stats_display()

    # Handle button A (cycle display modes)
    if clue.button_a:
        if not button_a_pressed:
            button_a_pressed = True
            display_mode = (display_mode + 1) % 3

            if display_mode == 0:
                display.root_group = main_group
                print("Display mode: Main")
            elif display_mode == 1:
                display.root_group = trends_group
                print("Display mode: Trends")
            elif display_mode == 2:
                display.root_group = stats_group
                print("Display mode: Statistics")

            # Brief flash to acknowledge button press
            clue.pixel.fill((255, 255, 0))
            time.sleep(0.1)
            clue.pixel.fill((0, 255, 0))
    else:
        button_a_pressed = False

    # Handle button B (toggle Celsius/Fahrenheit)
    if clue.button_b:
        if not button_b_pressed:
            button_b_pressed = True
            use_fahrenheit = not use_fahrenheit
            unit = "Fahrenheit" if use_fahrenheit else "Celsius"
            print(f"Temperature unit: {unit}")

            # Brief flash to acknowledge button press
            clue.pixel.fill((255, 0, 255))
            time.sleep(0.1)
            clue.pixel.fill((0, 255, 0))
    else:
        button_b_pressed = False

    # Sleep until next update
    time.sleep(UPDATE_INTERVAL)
