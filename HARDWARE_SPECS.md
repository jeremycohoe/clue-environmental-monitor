# Adafruit CLUE nRF52840 Express - Complete Guide

## Device Information
- **Model**: Adafruit CLUE nRF52840 Express
- **CircuitPython Version**: 9.2.4 (2025-01-28)
- **Board ID**: clue_nrf52840_express
- **UID**: B6060B5384F2F8C4
- **Backup Date**: 2025-11-01

## Table of Contents
1. [Hardware Capabilities](#hardware-capabilities)
2. [Sensor Specifications](#sensor-specifications)
3. [Getting Started](#getting-started)
4. [Temperature Calibration](#temperature-calibration)
5. [Example Projects](#example-projects)
6. [Best Practices](#best-practices)

---

## Hardware Capabilities

The Adafruit CLUE is a powerful, all-in-one development board with an impressive array of sensors:

### Display
- **1.3" 240x240 Color IPS TFT** - ST7789 chipset
- 16-bit color display
- Wide viewing angles
- Built-in backlight

### Sensors

#### Environmental Sensors
1. **SHT31-D Temperature & Humidity Sensor**
   - Temperature range: -40°C to +125°C (±0.2°C accuracy)
   - Humidity range: 0-100% RH (±2% accuracy)
   - Self-heating effect: ~0.5-1°C due to board heat

2. **BMP280 Barometric Pressure Sensor**
   - Pressure range: 300-1100 hPa
   - Altitude calculation capability
   - Temperature sensor (can be used for calibration reference)

#### Motion & Orientation Sensors
3. **LSM6DS33 Accelerometer + Gyroscope**
   - 3-axis accelerometer: ±2/±4/±8/±16 g
   - 3-axis gyroscope: ±125/±245/±500/±1000/±2000 dps
   - Gesture detection, tap/double-tap, freefall detection

4. **LIS3MDL Magnetometer**
   - 3-axis magnetic field sensor
   - Compass functionality
   - ±4/±8/±12/±16 gauss ranges

5. **APDS9960 Proximity, Light, Color, and Gesture Sensor**
   - Ambient light sensing (RGB)
   - Proximity detection (up to ~20cm)
   - Gesture detection (up/down/left/right)
   - Color sensing

#### Audio
6. **PDM Microphone**
   - Built-in microphone for audio input
   - Sound level detection
   - Voice/audio recording capabilities

7. **Buzzer**
   - Built-in speaker for tones and simple audio output

### Input/Output
- **2 Programmable Buttons** (A and B)
- **RGB NeoPixel LED**
- **White LED** (on GPIO 17)
- **I2C, SPI, UART** interfaces available on edge connectors
- **6 GPIO pins** with analog input capability
- **USB-C connector** for power and data

### Processing & Connectivity
- **nRF52840** - ARM Cortex-M4F processor @ 64 MHz
- **2 MB Flash** storage
- **256 KB RAM**
- **Bluetooth Low Energy (BLE)** 5.0
- **NFC** tag support

---

## Sensor Specifications

### Temperature & Humidity (SHT31-D)

**Access via**: `clue.temperature` and `clue.humidity`

**Specifications**:
- Temperature accuracy: ±0.2°C (0°C to 90°C)
- Humidity accuracy: ±2% RH (10% to 90% RH)
- Response time: <8 seconds (τ63%)
- Repeatability: ±0.1°C, ±0.1% RH

**Known Issues**:
- **Self-heating**: The sensor reads 0.5-1.5°C higher than ambient due to heat from the processor and other components
- **Calibration needed**: For accurate room temperature readings, apply a temperature offset
- Position-dependent: Reading varies based on board orientation and airflow

**Best Use Cases**:
- Relative temperature monitoring (trends over time)
- Humidity monitoring (less affected by self-heating)
- Environmental data logging
- HVAC monitoring

### Pressure & Altitude (BMP280)

**Access via**: `clue.pressure` and `clue.altitude`

**Specifications**:
- Pressure range: 300-1100 hPa
- Relative accuracy: ±0.12 hPa (±1m altitude)
- Absolute accuracy: ±1 hPa
- Temperature coefficient: ±1.5 Pa/K

**Best Use Cases**:
- Weather monitoring
- Altitude/elevation tracking
- Indoor/outdoor detection
- Vertical position tracking (stairs, floors)

### Accelerometer & Gyroscope (LSM6DS33)

**Access via**: `clue.acceleration` and `clue.gyro`

**Best Use Cases**:
- Motion detection
- Orientation sensing
- Step counting
- Gesture recognition
- Tap detection
- Gaming controllers
- Stabilization

### Magnetometer (LIS3MDL)

**Access via**: `clue.magnetic`

**Best Use Cases**:
- Compass/heading detection
- Metal detection
- Position tracking
- Navigation systems

### Proximity & Light (APDS9960)

**Access via**: `clue.proximity`, `clue.color`, `clue.gesture`

**Best Use Cases**:
- Touchless interfaces
- Gesture control
- Color sensing/matching
- Ambient light adjustment
- Presence detection

### Microphone (PDM)

**Best Use Cases**:
- Sound level monitoring
- Voice activation
- Audio recording
- Noise detection
- Clap detection

---

## Getting Started

### 1. Connecting to Your Computer

The CLUE appears as two devices when connected via USB:
1. **Mass Storage Device**: `CIRCUITPY` drive (2MB)
2. **Serial Console**: `/dev/ttyACM0` (on Linux) or `COM` port (Windows)

### 2. File Structure

```
CIRCUITPY/
├── code.py          # Main program (auto-runs on boot)
├── boot.py          # Boot configuration (optional)
├── lib/             # Libraries folder
│   ├── adafruit_clue.py
│   ├── adafruit_display_text/
│   └── ... (other libraries)
└── boot_out.txt     # System info (read-only)
```

### 3. Basic Program Template

```python
import board
from adafruit_clue import clue

# Simple sensor reading
while True:
    print(f"Temperature: {clue.temperature:.1f}°C")
    print(f"Humidity: {clue.humidity:.1f}%")
    print(f"Pressure: {clue.pressure:.1f} hPa")
```

### 4. Accessing the Serial Console

**Linux/Mac**:
```bash
screen /dev/ttyACM0 115200
# or
picocom /dev/ttyACM0 -b 115200
```

**Windows**: Use PuTTY or the Mu Editor

---

## Temperature Calibration

### Why Calibrate?

The SHT31-D sensor on the CLUE experiences self-heating from the nRF52840 processor and other components. This causes readings to be **0.5-1.5°C higher** than actual room temperature.

### Calibration Methods

#### Method 1: Reference Thermometer Comparison (Recommended)

1. **Get a reference thermometer**:
   - Use a calibrated digital thermometer
   - Or compare with multiple known-good thermometers
   - Medical thermometers work well for room temperature

2. **Stabilization period**:
   - Let the CLUE run for 10-15 minutes in the target environment
   - Place both thermometers in the same location
   - Avoid direct sunlight, drafts, or heat sources
   - Keep them at the same height

3. **Take multiple readings**:
   - Record 5-10 readings from each device over 30 minutes
   - Calculate the average difference
   - This is your **calibration offset**

4. **Apply the offset** in your code:
   ```python
   TEMP_OFFSET = -1.2  # Adjust based on your calibration
   actual_temp = clue.temperature + TEMP_OFFSET
   ```

#### Method 2: BMP280 Cross-Reference

The BMP280 pressure sensor also measures temperature and may be less affected by self-heating:

```python
import board
import adafruit_bmp280

i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

sht_temp = clue.temperature
bmp_temp = bmp280.temperature

# The difference can help estimate self-heating
offset_estimate = bmp_temp - sht_temp
```

#### Method 3: Time-Based Calibration

Temperature readings change as the board warms up:

```python
import time

# Take reading immediately after power-on
time.sleep(2)
cold_temp = clue.temperature

# Take reading after 10 minutes
time.sleep(600)
warm_temp = clue.temperature

# Estimate self-heating effect
self_heating = warm_temp - cold_temp
print(f"Self-heating effect: {self_heating:.1f}°C")
```

### Recommended Offset Values

Based on typical usage:
- **Static/stationary use**: -0.8 to -1.2°C
- **Active use** (display updating frequently): -1.0 to -1.5°C
- **Battery powered** (lower current): -0.5 to -0.8°C
- **With external sensors**: Custom calibration recommended

### Humidity Note

Humidity readings are generally accurate and don't require calibration. However, temperature affects relative humidity calculations, so use the calibrated temperature when needed.

---

## Example Projects

### 1. Environmental Monitor (with Calibration)
Location: `/examples/environmental_monitor.py`

### 2. Weather Station
Location: `/examples/weather_station.py`

### 3. Gesture-Controlled Display
Location: `/examples/gesture_display.py`

### 4. Data Logger
Location: `/examples/data_logger.py`

### 5. Compass
Location: `/examples/compass.py`

---

## Best Practices

### Power Management
- USB power provides stable readings
- Battery power may affect sensor accuracy
- Deep sleep modes available for battery projects

### Sensor Accuracy
- Allow 10-15 minute warm-up period
- Keep away from heat sources
- Consider airflow and orientation
- Calibrate for your specific use case

### Display Usage
- Lower brightness saves power
- Update frequency affects CPU heat (and temperature readings)
- Use `displayio` for efficient graphics

### Data Logging
- CIRCUITPY drive is limited to ~2MB
- Consider external storage (SD card via SPI)
- Serial output for real-time logging
- BLE for wireless data transmission

### Code Organization
- Use `code.py` as the main entry point
- Keep libraries in the `lib/` folder
- Comment your calibration values
- Version control your projects

### Troubleshooting
- If the CLUE stops responding, press **RESET** button
- Double-press RESET to enter bootloader mode (for firmware updates)
- Check `boot_out.txt` for system information
- Use serial console for debugging

---

## Additional Resources

- [Adafruit CLUE Overview](https://learn.adafruit.com/adafruit-clue)
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [CLUE Library Reference](https://circuitpython.readthedocs.io/projects/clue/)
- [Sensor Datasheets](https://learn.adafruit.com/adafruit-clue/downloads)

---

## Backup Information

**Original files backed up to**: `backup_20251101_210948/`
- `code.py` - Temperature/humidity monitor with trends
- `temp.py` - Alternative temperature display
- `boot_out.txt` - System information

**Backup created**: November 1, 2025
