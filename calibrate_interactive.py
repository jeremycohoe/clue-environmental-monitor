"""
Interactive Temperature Calibration for CLUE
==============================================

This script reads the RAW temperature from the sensor and helps you
calculate the exact offset needed.
"""

import time
import board
import displayio
import terminalio
from adafruit_clue import clue
from adafruit_display_text import label

# Setup display
display = board.DISPLAY
display.brightness = 0.8
screen = displayio.Group()
display.root_group = screen

# Title
title = label.Label(terminalio.FONT, text="Calibration", color=0xFFFF00,
                   x=30, y=10, scale=2)
screen.append(title)

# Raw temp label
raw_label = label.Label(terminalio.FONT, text="Raw: --.-C", color=0xFF0000,
                       x=10, y=60, scale=2)
screen.append(raw_label)

# Target label
target_label = label.Label(terminalio.FONT, text="Target: 27.5C", color=0x00FF00,
                          x=10, y=100, scale=2)
screen.append(target_label)

# Offset label
offset_label = label.Label(terminalio.FONT, text="Offset: --.-C", color=0x00FFFF,
                          x=10, y=140, scale=2)
screen.append(offset_label)

# Instructions
inst_label = label.Label(terminalio.FONT, text="Reading sensor...", color=0xFFFFFF,
                        x=10, y=200, scale=1)
screen.append(inst_label)

# Set NeoPixel
clue.pixel.brightness = 0.2
clue.pixel.fill((255, 165, 0))

print("=" * 60)
print("CLUE TEMPERATURE CALIBRATION")
print("=" * 60)
print()
print("Your reference thermometer shows: 27.5°C")
print("Reading CLUE raw sensor value...")
print()
print("Waiting 5 seconds for sensor to stabilize...")
time.sleep(5)

# Target reference temperature
TARGET_TEMP = 27.5

# Take multiple readings and average them
readings = []
print("Taking 10 readings over 20 seconds...")
for i in range(10):
    raw_temp = clue.temperature
    readings.append(raw_temp)

    # Update display
    raw_label.text = f"Raw: {raw_temp:.1f}C"
    offset = TARGET_TEMP - raw_temp
    offset_label.text = f"Offset: {offset:.1f}C"

    print(f"Reading {i+1}/10: {raw_temp:.1f}C  (Offset would be: {offset:.1f}C)")

    # Flash LED
    if i % 2 == 0:
        clue.pixel.fill((0, 255, 0))
    else:
        clue.pixel.fill((0, 100, 0))

    time.sleep(2)

# Calculate average
avg_raw = sum(readings) / len(readings)
calculated_offset = TARGET_TEMP - avg_raw

print()
print("=" * 60)
print("CALIBRATION RESULTS")
print("=" * 60)
print(f"Average RAW reading:  {avg_raw:.2f}°C")
print(f"Target temperature:   {TARGET_TEMP:.2f}°C")
print(f"Calculated offset:    {calculated_offset:.2f}°C")
print("=" * 60)
print()
print("UPDATE YOUR CODE:")
print(f"Set TEMP_OFFSET = {calculated_offset:.1f}")
print()
print("=" * 60)

# Update display with final results
raw_label.text = f"Raw: {avg_raw:.1f}C"
offset_label.text = f"Set: {calculated_offset:.1f}C"
inst_label.text = f"TEMP_OFFSET = {calculated_offset:.1f}"
clue.pixel.fill((0, 0, 255))

# Keep displaying results
while True:
    time.sleep(1)
