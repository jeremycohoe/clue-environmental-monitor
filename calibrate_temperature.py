"""
Temperature Calibration Helper for Adafruit CLUE
=================================================

This interactive script helps you calibrate your CLUE's temperature sensor.

Instructions:
1. Place CLUE and a reference thermometer side-by-side
2. Wait 10-15 minutes for thermal stabilization
3. Run this script
4. Enter the reference temperature when prompted
5. The script will calculate and display the calibration offset

Note: This requires serial console connection (screen, picocom, or Mu editor)
"""

import time
import board
import displayio
import terminalio
from adafruit_clue import clue
from adafruit_display_text import label
import supervisor

print("=" * 60)
print("ADAFRUIT CLUE - TEMPERATURE CALIBRATION HELPER")
print("=" * 60)
print()

# Setup display
display = board.DISPLAY
display.brightness = 0.7
screen = displayio.Group()
display.root_group = screen

# Title
title = label.Label(terminalio.FONT, text="Calibration", color=0xFFFF00,
                   x=50, y=10, scale=2)
screen.append(title)

# Status message
status_label = label.Label(terminalio.FONT, text="Stabilizing...", color=0xFFFFFF,
                          x=40, y=60, scale=2)
screen.append(status_label)

# Temperature display
temp_label = label.Label(terminalio.FONT, text="--.-C", color=0x00FFFF,
                        x=50, y=120, scale=3)
screen.append(temp_label)

# Instruction
instruction_label = label.Label(terminalio.FONT, text="See serial console",
                                color=0x888888, x=30, y=200, scale=1)
screen.append(instruction_label)

# Set NeoPixel to orange during calibration
clue.pixel.brightness = 0.2
clue.pixel.fill((255, 100, 0))

print("Step 1: Stabilization Period")
print("-" * 60)
print("Letting the sensor stabilize for 15 seconds...")
print("(In real calibration, wait 10-15 minutes)")
print()

# Take some initial readings
readings = []
for i in range(15):
    temp = clue.temperature
    readings.append(temp)
    temp_label.text = f"{temp:.1f}C"

    if i < 5:
        status_label.text = "Warming up..."
    elif i < 10:
        status_label.text = "Stabilizing..."
    else:
        status_label.text = "Almost ready..."

    print(f"  Reading {i+1}/15: {temp:.1f}°C")
    time.sleep(1)

print()
print("Stabilization complete!")
print()

# Calculate current average
clue_temp = sum(readings[-5:]) / 5  # Average of last 5 readings

print("=" * 60)
print("Step 2: Reference Measurement")
print("-" * 60)
print()
print(f"CLUE Temperature: {clue_temp:.2f}°C")
print()
print("Now, please:")
print("1. Read your reference thermometer")
print("2. Wait for this temperature to stabilize")
print("3. Note the reference temperature")
print()

status_label.text = "Ready!"
temp_label.text = f"{clue_temp:.1f}C"
temp_label.color = 0x00FF00
clue.pixel.fill((0, 255, 0))

# Continuously display current temperature
print("Current CLUE readings (updates every 5 seconds):")
print("-" * 60)

measurement_count = 0
sum_measurements = 0

try:
    while True:
        current_temp = clue.temperature
        temp_label.text = f"{current_temp:.1f}C"

        measurement_count += 1
        sum_measurements += current_temp
        avg_temp = sum_measurements / measurement_count

        print(f"[{measurement_count:3d}] Current: {current_temp:.2f}°C  |  "
              f"Average: {avg_temp:.2f}°C")

        # Update display
        status_label.text = f"Avg: {avg_temp:.1f}C"

        # Check if user input is available (won't work in CircuitPython serial console)
        # This is more for documentation - actual offset calculation needs to be done manually

        time.sleep(5)

        # Provide periodic instructions
        if measurement_count % 6 == 0:  # Every 30 seconds
            print()
            print("To calculate calibration offset:")
            print(f"  OFFSET = (Your Reference Temperature) - {avg_temp:.2f}")
            print(f"  Example: If reference shows 22.0°C: OFFSET = 22.0 - {avg_temp:.2f} = {22.0 - avg_temp:.2f}°C")
            print()
            print("Then edit code.py and set:")
            print(f"  TEMP_OFFSET = {22.0 - avg_temp:.2f}  # Replace 22.0 with your actual reference")
            print()
            print("-" * 60)

except KeyboardInterrupt:
    print()
    print("=" * 60)
    print("Calibration Helper Stopped")
    print("=" * 60)
    print()
    print(f"Final average CLUE temperature: {avg_temp:.2f}°C")
    print()
    print("To complete calibration:")
    print("1. Note your reference thermometer reading")
    print(f"2. Calculate: OFFSET = (Reference Temp) - {avg_temp:.2f}")
    print("3. Edit code.py and update TEMP_OFFSET with your calculated value")
    print()
    status_label.text = "Stopped"
    temp_label.color = 0xFF0000
    clue.pixel.fill((255, 0, 0))

print()
print("Calibration examples:")
print("-" * 60)
print(f"If reference = 20.0°C: OFFSET = 20.0 - {avg_temp:.2f} = {20.0 - avg_temp:+.2f}°C")
print(f"If reference = 21.0°C: OFFSET = 21.0 - {avg_temp:.2f} = {21.0 - avg_temp:+.2f}°C")
print(f"If reference = 22.0°C: OFFSET = 22.0 - {avg_temp:.2f} = {22.0 - avg_temp:+.2f}°C")
print(f"If reference = 23.0°C: OFFSET = 23.0 - {avg_temp:.2f} = {23.0 - avg_temp:+.2f}°C")
print()
