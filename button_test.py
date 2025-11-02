"""
Simple button test for CLUE
Tests if Button A and Button B work
"""

import time
from adafruit_clue import clue

print("Button Test Starting...")
print("Press Button A (left) or Button B (right)")
print("Press both together to exit")
print("-" * 40)

clue.pixel.brightness = 0.3

while True:
    if clue.button_a and clue.button_b:
        print("Both buttons pressed - exiting")
        clue.pixel.fill((255, 0, 0))
        break

    if clue.button_a:
        print("Button A pressed!")
        clue.pixel.fill((0, 255, 0))
        time.sleep(0.2)

    if clue.button_b:
        print("Button B pressed!")
        clue.pixel.fill((0, 0, 255))
        time.sleep(0.2)

    time.sleep(0.05)
