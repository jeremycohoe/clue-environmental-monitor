"""
Leftover Food Safety Device
FDA-compliant food safety monitoring for refrigerated leftovers

Features:
- 4°C threshold detection (food safe temperature)
- Color-coded safety zones (GREEN/YELLOW/RED)
- Time tracking in danger zone
- 4-day maximum storage monitoring
- Visual alerts and status display

Author: jeremycohoe
License: MIT
"""

import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_clue import clue

# Calibration offsets
TEMP_OFFSET = -3.5  # Calibrated temperature offset
HUMIDITY_OFFSET = 5.2  # Calibrated humidity offset

# FDA Food Safety Thresholds
FOOD_SAFE_TEMP = 4.0  # Degrees Celsius - FDA safe temperature
ROOM_TEMP = 21.0  # Degrees Celsius - defined room temperature
DANGER_ZONE_LIMIT = 7200  # 2 hours in seconds
MAX_STORAGE_DAYS = 4  # Maximum days in refrigerator

# State definitions
STATE_INITIAL = 0  # At room temperature, ready to start
STATE_SAFE = 1  # Below 4°C, food is safe
STATE_WARNING = 2  # Above 4°C but below 2 hour limit
STATE_DISCARD = 3  # Exceeded safety limits
STATE_CHARGE = 4  # Returned to room temp, needs charging

# Colors for safety zones
COLOR_GREEN = 0x00FF00
COLOR_YELLOW = 0xFFFF00
COLOR_RED = 0xFF0000
COLOR_BLUE = 0x0000FF
COLOR_WHITE = 0xFFFFFF
COLOR_BLACK = 0x000000

# Global state tracking
current_state = STATE_INITIAL
fridge_entry_time = None
danger_zone_start = None
total_danger_time = 0
previous_temp = None

def get_calibrated_temperature():
    """Get calibrated temperature reading in Celsius"""
    raw_temp = clue.temperature
    return raw_temp + TEMP_OFFSET

def get_calibrated_humidity():
    """Get calibrated humidity reading"""
    raw_humidity = clue.humidity
    return raw_humidity + HUMIDITY_OFFSET

def format_time_duration(seconds):
    """Convert seconds to human readable format"""
    if seconds < 60:
        return "{:d}s".format(int(seconds))
    elif seconds < 3600:
        mins = int(seconds / 60)
        secs = int(seconds % 60)
        return "{:d}m {:d}s".format(mins, secs)
    else:
        hours = int(seconds / 3600)
        mins = int((seconds % 3600) / 60)
        return "{:d}h {:d}m".format(hours, mins)

def format_days_hours(seconds):
    """Convert seconds to days and hours"""
    days = int(seconds / 86400)
    hours = int((seconds % 86400) / 3600)
    if days > 0:
        return "{:d}d {:d}h".format(days, hours)
    else:
        return "{:d}h".format(hours)

def create_display_group(bg_color):
    """Create a new display group with background color"""
    group = displayio.Group()

    # Create background
    color_bitmap = displayio.Bitmap(240, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = bg_color
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    group.append(bg_sprite)

    return group

def update_display_safe(temp, days_in_fridge):
    """Update display for SAFE state (GREEN)"""
    group = create_display_group(COLOR_GREEN)

    # Title
    title = label.Label(terminalio.FONT, text="FOOD SAFETY", color=COLOR_BLACK)
    title.x = 60
    title.y = 15
    group.append(title)

    # Status
    status = label.Label(terminalio.FONT, text="SAFE", color=COLOR_BLACK, scale=3)
    status.x = 60
    status.y = 50
    group.append(status)

    checkmark = label.Label(terminalio.FONT, text="OK", color=COLOR_BLACK, scale=2)
    checkmark.x = 170
    checkmark.y = 50
    group.append(checkmark)

    # Temperature
    temp_text = "Temp: {:.1f}{}C".format(temp, chr(176))
    temp_label = label.Label(terminalio.FONT, text=temp_text, color=COLOR_BLACK, scale=2)
    temp_label.x = 20
    temp_label.y = 100
    group.append(temp_label)

    # Time in fridge
    if days_in_fridge is not None:
        time_text = "In Fridge:"
        time_label = label.Label(terminalio.FONT, text=time_text, color=COLOR_BLACK)
        time_label.x = 60
        time_label.y = 140
        group.append(time_label)

        days_text = format_days_hours(days_in_fridge)
        days_label = label.Label(terminalio.FONT, text=days_text, color=COLOR_BLACK, scale=2)
        days_label.x = 70
        days_label.y = 160
        group.append(days_label)

        # Days remaining
        days_elapsed = int(days_in_fridge / 86400)
        days_left = MAX_STORAGE_DAYS - days_elapsed
        if days_left >= 0:
            left_text = "Safe for: {}d".format(days_left)
        else:
            left_text = "OVER 4 DAYS!"

        left_label = label.Label(terminalio.FONT, text=left_text, color=COLOR_BLACK)
        left_label.x = 60
        left_label.y = 200
        group.append(left_label)

    clue.display.root_group = group

def update_display_warning(temp, danger_time):
    """Update display for WARNING state (YELLOW)"""
    group = create_display_group(COLOR_YELLOW)

    # Title
    title = label.Label(terminalio.FONT, text="FOOD SAFETY", color=COLOR_BLACK)
    title.x = 60
    title.y = 15
    group.append(title)

    # Status
    status = label.Label(terminalio.FONT, text="WARNING", color=COLOR_BLACK, scale=2)
    status.x = 30
    status.y = 50
    group.append(status)

    warning_symbol = label.Label(terminalio.FONT, text="!", color=COLOR_BLACK, scale=3)
    warning_symbol.x = 210
    warning_symbol.y = 50
    group.append(warning_symbol)

    # Temperature
    temp_text = "Temp: {:.1f}{}C".format(temp, chr(176))
    temp_label = label.Label(terminalio.FONT, text=temp_text, color=COLOR_BLACK, scale=2)
    temp_label.x = 20
    temp_label.y = 100
    group.append(temp_label)

    # Time in danger zone
    time_text = "Above 4{}C:".format(chr(176))
    time_label = label.Label(terminalio.FONT, text=time_text, color=COLOR_BLACK)
    time_label.x = 60
    time_label.y = 140
    group.append(time_label)

    danger_text = format_time_duration(danger_time)
    danger_label = label.Label(terminalio.FONT, text=danger_text, color=COLOR_BLACK, scale=2)
    danger_label.x = 70
    danger_label.y = 160
    group.append(danger_label)

    # Limit warning
    remaining = DANGER_ZONE_LIMIT - danger_time
    limit_text = "Limit: 2 hours"
    if remaining < 600:  # Less than 10 minutes
        limit_text = "TIME CRITICAL!"

    limit_label = label.Label(terminalio.FONT, text=limit_text, color=COLOR_BLACK, scale=1)
    limit_label.x = 40
    limit_label.y = 200
    group.append(limit_label)

    # Action
    action = label.Label(terminalio.FONT, text="Return to fridge", color=COLOR_BLACK)
    action.x = 40
    action.y = 220
    group.append(action)

    clue.display.root_group = group

def update_display_discard(temp, reason):
    """Update display for DISCARD state (RED)"""
    group = create_display_group(COLOR_RED)

    # Title
    title = label.Label(terminalio.FONT, text="FOOD SAFETY", color=COLOR_WHITE)
    title.x = 60
    title.y = 15
    group.append(title)

    # Status
    status = label.Label(terminalio.FONT, text="DISCARD", color=COLOR_WHITE, scale=2)
    status.x = 30
    status.y = 50
    group.append(status)

    x_symbol = label.Label(terminalio.FONT, text="X", color=COLOR_WHITE, scale=3)
    x_symbol.x = 200
    x_symbol.y = 50
    group.append(x_symbol)

    # Temperature
    temp_text = "Temp: {:.1f}{}C".format(temp, chr(176))
    temp_label = label.Label(terminalio.FONT, text=temp_text, color=COLOR_WHITE, scale=2)
    temp_label.x = 20
    temp_label.y = 100
    group.append(temp_label)

    # Reason
    reason_label = label.Label(terminalio.FONT, text=reason, color=COLOR_WHITE)
    reason_label.x = 10
    reason_label.y = 140
    group.append(reason_label)

    # Warning messages
    warning1 = label.Label(terminalio.FONT, text="NOT SAFE TO EAT", color=COLOR_WHITE, scale=2)
    warning1.x = 10
    warning1.y = 170
    group.append(warning1)

    warning2 = label.Label(terminalio.FONT, text="DISPOSE OF FOOD", color=COLOR_WHITE, scale=1)
    warning2.x = 20
    warning2.y = 210
    group.append(warning2)

    clue.display.root_group = group

def update_display_charge(temp):
    """Update display for CHARGE state (BLUE)"""
    group = create_display_group(COLOR_BLUE)

    # Title
    title = label.Label(terminalio.FONT, text="FOOD SAFETY", color=COLOR_WHITE)
    title.x = 60
    title.y = 15
    group.append(title)

    # Status
    status = label.Label(terminalio.FONT, text="CHARGE ME", color=COLOR_WHITE, scale=2)
    status.x = 20
    status.y = 50
    group.append(status)

    # Temperature
    temp_text = "Temp: {:.1f}{}C".format(temp, chr(176))
    temp_label = label.Label(terminalio.FONT, text=temp_text, color=COLOR_WHITE, scale=2)
    temp_label.x = 20
    temp_label.y = 100
    group.append(temp_label)

    room_temp_label = label.Label(terminalio.FONT, text="(Room Temperature)", color=COLOR_WHITE)
    room_temp_label.x = 30
    room_temp_label.y = 130
    group.append(room_temp_label)

    # Instructions
    instr1 = label.Label(terminalio.FONT, text="Ready to reset", color=COLOR_WHITE)
    instr1.x = 50
    instr1.y = 170
    group.append(instr1)

    instr2 = label.Label(terminalio.FONT, text="Connect USB", color=COLOR_WHITE)
    instr2.x = 60
    instr2.y = 190
    group.append(instr2)

    instr3 = label.Label(terminalio.FONT, text="to charge", color=COLOR_WHITE)
    instr3.x = 70
    instr3.y = 210
    group.append(instr3)

    clue.display.root_group = group

def update_display_initial(temp):
    """Update display for INITIAL state (waiting to enter fridge)"""
    group = create_display_group(COLOR_WHITE)

    # Title
    title = label.Label(terminalio.FONT, text="FOOD SAFETY", color=COLOR_BLACK)
    title.x = 60
    title.y = 15
    group.append(title)

    # Status
    status = label.Label(terminalio.FONT, text="READY", color=COLOR_BLACK, scale=3)
    status.x = 40
    status.y = 60
    group.append(status)

    # Temperature
    temp_text = "Temp: {:.1f}{}C".format(temp, chr(176))
    temp_label = label.Label(terminalio.FONT, text=temp_text, color=COLOR_BLACK, scale=2)
    temp_label.x = 20
    temp_label.y = 120
    group.append(temp_label)

    # Instructions
    instr1 = label.Label(terminalio.FONT, text="Place in fridge", color=COLOR_BLACK)
    instr1.x = 50
    instr1.y = 170
    group.append(instr1)

    instr2 = label.Label(terminalio.FONT, text="Monitoring starts", color=COLOR_BLACK)
    instr2.x = 40
    instr2.y = 190
    group.append(instr2)

    instr3 = label.Label(terminalio.FONT, text="at 4{}C".format(chr(176)), color=COLOR_BLACK)
    instr3.x = 80
    instr3.y = 210
    group.append(instr3)

    clue.display.root_group = group

def update_state(temp):
    """Update state machine based on temperature and time"""
    global current_state, fridge_entry_time, danger_zone_start, total_danger_time

    current_time = time.monotonic()

    if current_state == STATE_INITIAL:
        # Waiting to enter fridge
        if temp <= FOOD_SAFE_TEMP:
            current_state = STATE_SAFE
            fridge_entry_time = current_time
            danger_zone_start = None
            total_danger_time = 0
            print("Entered fridge - monitoring started")
        update_display_initial(temp)

    elif current_state == STATE_SAFE:
        # Food is safe in fridge
        time_in_fridge = current_time - fridge_entry_time
        days_in_fridge_seconds = int(time_in_fridge)

        # Check if exceeded maximum storage
        if time_in_fridge > (MAX_STORAGE_DAYS * 86400):
            current_state = STATE_DISCARD
            reason = "Stored > 4 days"
            update_display_discard(temp, reason)
            print("DISCARD: Exceeded 4 day storage limit")

        # Check if temperature rose above safe
        elif temp > FOOD_SAFE_TEMP:
            current_state = STATE_WARNING
            danger_zone_start = current_time
            print("WARNING: Temperature above 4C")
            update_display_warning(temp, 0)

        # Check if returned to room temperature
        elif temp >= ROOM_TEMP:
            current_state = STATE_CHARGE
            print("Returned to room temperature - charge mode")
            update_display_charge(temp)

        else:
            update_display_safe(temp, days_in_fridge_seconds)

    elif current_state == STATE_WARNING:
        # Temperature above safe but monitoring
        danger_time = current_time - danger_zone_start + total_danger_time

        # Check if exceeded 2 hour limit
        if danger_time >= DANGER_ZONE_LIMIT:
            current_state = STATE_DISCARD
            reason_text = "Above 4{}C > 2hrs".format(chr(176))
            update_display_discard(temp, reason_text)
            print("DISCARD: Exceeded 2 hour danger zone")

        # Check if returned to safe temperature
        elif temp <= FOOD_SAFE_TEMP:
            total_danger_time = danger_time
            danger_zone_start = None
            current_state = STATE_SAFE
            print("Returned to safe temperature")
            time_in_fridge = current_time - fridge_entry_time
            update_display_safe(temp, int(time_in_fridge))

        # Check if returned to room temperature
        elif temp >= ROOM_TEMP:
            current_state = STATE_CHARGE
            print("Returned to room temperature - charge mode")
            update_display_charge(temp)

        else:
            update_display_warning(temp, danger_time)

    elif current_state == STATE_DISCARD:
        # Food must be discarded
        if temp >= ROOM_TEMP:
            current_state = STATE_CHARGE
            print("Returned to room temperature - charge mode")
            update_display_charge(temp)
        else:
            # Stay in discard state
            reason_text = "UNSAFE"
            update_display_discard(temp, reason_text)

    elif current_state == STATE_CHARGE:
        # Waiting to be recharged and reset
        if temp <= FOOD_SAFE_TEMP:
            # Reset to initial state
            current_state = STATE_INITIAL
            fridge_entry_time = None
            danger_zone_start = None
            total_danger_time = 0
            print("Reset - ready for new monitoring")
            update_display_initial(temp)
        else:
            update_display_charge(temp)

# Main loop
print("Food Safety Monitor Starting...")
print("FDA Compliant Leftover Monitoring")
print("Safe Temp: <= 4C, Danger Zone Limit: 2 hours")
print("Max Storage: 4 days")
print("-" * 40)

# Initial display
temp = get_calibrated_temperature()
update_display_initial(temp)

while True:
    try:
        # Get current temperature
        temp = get_calibrated_temperature()

        # Update state machine
        update_state(temp)

        # Update NeoPixel based on state
        if current_state == STATE_SAFE:
            clue.pixel.fill(COLOR_GREEN)
        elif current_state == STATE_WARNING:
            clue.pixel.fill(COLOR_YELLOW)
        elif current_state == STATE_DISCARD:
            clue.pixel.fill(COLOR_RED)
        elif current_state == STATE_CHARGE:
            clue.pixel.fill(COLOR_BLUE)
        else:
            clue.pixel.fill(COLOR_WHITE)

        # Wait before next update
        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)
