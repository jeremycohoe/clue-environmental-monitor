"""
Simple Sensor Test - Read all CLUE sensors
===========================================

This script reads and displays all available sensors on the CLUE.
Useful for verifying sensors are working and exploring capabilities.

Output is sent to serial console.
"""

import time
import board
from adafruit_clue import clue

print("=" * 70)
print("ADAFRUIT CLUE - COMPLETE SENSOR TEST")
print("=" * 70)
print()

# Set NeoPixel to indicate running
clue.pixel.brightness = 0.1
clue.pixel.fill((0, 255, 0))

print("Reading all sensors every 2 seconds...")
print("Press Ctrl+C to stop")
print()

count = 0

try:
    while True:
        count += 1
        print(f"\n{'='*70}")
        print(f"Reading #{count} - {time.monotonic():.1f}s since boot")
        print(f"{'='*70}")

        # Environmental Sensors
        print("\n[ENVIRONMENTAL SENSORS]")
        print(f"  Temperature:  {clue.temperature:.2f} °C")
        print(f"  Humidity:     {clue.humidity:.1f} %")
        print(f"  Pressure:     {clue.pressure:.2f} hPa")
        print(f"  Altitude:     {clue.altitude:.1f} m")

        # Motion Sensors
        print("\n[MOTION SENSORS]")
        accel_x, accel_y, accel_z = clue.acceleration
        print(f"  Acceleration: X={accel_x:6.2f}, Y={accel_y:6.2f}, Z={accel_z:6.2f} m/s²")

        gyro_x, gyro_y, gyro_z = clue.gyro
        print(f"  Gyroscope:    X={gyro_x:6.2f}, Y={gyro_y:6.2f}, Z={gyro_z:6.2f} dps")

        mag_x, mag_y, mag_z = clue.magnetic
        print(f"  Magnetometer: X={mag_x:6.2f}, Y={mag_y:6.2f}, Z={mag_z:6.2f} µT")

        # Light & Proximity Sensors
        print("\n[LIGHT & PROXIMITY SENSORS]")
        print(f"  Proximity:    {clue.proximity}")

        try:
            r, g, b, c = clue.color
            print(f"  Color (RGBC): R={r:5d}, G={g:5d}, B={b:5d}, Clear={c:5d}")
        except:
            print(f"  Color:        (Not available)")

        # Gesture (if available)
        try:
            gesture = clue.gesture
            if gesture:
                print(f"  Gesture:      {gesture}")
        except:
            pass

        # Audio
        print("\n[AUDIO]")
        print(f"  Sound Level:  {clue.sound_level}")

        # Buttons
        print("\n[BUTTONS]")
        print(f"  Button A:     {'PRESSED' if clue.button_a else 'Released'}")
        print(f"  Button B:     {'PRESSED' if clue.button_b else 'Released'}")

        # Touch (capacitive touch on some pins)
        print("\n[TOUCH PADS]")
        print(f"  Touch 0:      {'TOUCHED' if clue.touch_0 else 'Not touched'}")
        print(f"  Touch 1:      {'TOUCHED' if clue.touch_1 else 'Not touched'}")
        print(f"  Touch 2:      {'TOUCHED' if clue.touch_2 else 'Not touched'}")

        # White LEDs (if available)
        print("\n[STATUS]")
        print(f"  White LED:    {clue.white_leds}")

        # Calculate some derived values
        print("\n[DERIVED VALUES]")

        # Total acceleration (magnitude)
        import math
        total_accel = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
        print(f"  Accel Mag:    {total_accel:.2f} m/s²")

        # Compass heading (simplified)
        heading = math.atan2(mag_y, mag_x) * 180 / math.pi
        if heading < 0:
            heading += 360
        print(f"  Heading:      {heading:.1f}° (approximate)")

        # Sea level pressure (estimated from altitude)
        sea_level_pressure = clue.pressure / ((1 - (clue.altitude / 44330)) ** 5.255)
        print(f"  Sea Level P:  {sea_level_pressure:.2f} hPa (estimated)")

        # Blink NeoPixel
        if count % 2 == 0:
            clue.pixel.fill((0, 255, 0))
        else:
            clue.pixel.fill((0, 100, 0))

        time.sleep(2)

except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("Sensor test stopped")
    print("=" * 70)
    clue.pixel.fill((255, 0, 0))
