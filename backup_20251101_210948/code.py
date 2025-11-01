import time
import board
import displayio
import terminalio
from adafruit_clue import clue
from adafruit_display_text import label

# Constants
LOG_INTERVAL = 60  # Log data every 60 seconds (1 minute)
HISTORY_SIZE = 120  # Store last 120 readings (2 hours)

# Store historical data
temp_history = [None] * HISTORY_SIZE
humidity_history = [None] * HISTORY_SIZE
uptime_seconds = 0

# Setup display
display = board.DISPLAY
screen = displayio.Group()
display.root_group = screen  # Correct for CircuitPython 8+

# Add a spacer line to prevent cut-off
spacer_label = label.Label(terminalio.FONT, text=" ", color=0xFFFFFF, x=5, y=0, scale=2)
screen.append(spacer_label)

# Temperature label
temp_label = label.Label(terminalio.FONT, text="Temp: --°C", color=0xFFFFFF, x=5, y=25, scale=2)
screen.append(temp_label)

# Humidity label
humidity_label = label.Label(terminalio.FONT, text="Humidity: --%", color=0xFFFFFF, x=5, y=55, scale=2)
screen.append(humidity_label)

# Uptime label
uptime_label = label.Label(terminalio.FONT, text="Uptime: -- min", color=0xFFFFFF, x=5, y=85, scale=2)
screen.append(uptime_label)

# Trend label
trend_label = label.Label(terminalio.FONT, text="Trend: --", color=0xFFFFFF, x=5, y=115, scale=2)
screen.append(trend_label)

def calculate_trend(data):
    """Determine if values are increasing, decreasing, or stable."""
    valid_data = [d for d in data if d is not None]
    if len(valid_data) < 2:
        return "No trend"

    if valid_data[-1] > valid_data[0]:
        return "Increasing 🔼"
    elif valid_data[-1] < valid_data[0]:
        return "Decreasing 🔽"
    else:
        return "Stable ➖"

# Main loop
index = 0
while True:
    temperature = clue.temperature  # Get temperature in Celsius
    humidity = clue.humidity  # Get humidity in %

    temp_history[index] = round(temperature, 1)
    humidity_history[index] = round(humidity, 1)
    uptime_minutes = uptime_seconds // 60

    # Update display text
    temp_label.text = f"Temp: {temperature:.1f}°C"
    humidity_label.text = f"Humidity: {humidity:.1f}%"
    uptime_label.text = f"Uptime: {uptime_minutes} min"
    
    # Show trend analysis
    temp_trend = calculate_trend(temp_history)
    trend_label.text = f"Trend: {temp_trend}"

    # Increment uptime and index
    uptime_seconds += LOG_INTERVAL
    index = (index + 1) % HISTORY_SIZE  # Circular buffer

    time.sleep(LOG_INTERVAL)  # Wait before next reading

