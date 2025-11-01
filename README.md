# Adafruit CLUE Environmental Monitor

A comprehensive environmental monitoring system for the Adafruit CLUE nRF52840 Express with calibrated temperature sensing, historical trending, and multiple display modes.

![CLUE Badge](https://img.shields.io/badge/Adafruit-CLUE-blueviolet)
![CircuitPython](https://img.shields.io/badge/CircuitPython-9.2.4-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Real-time Monitoring**: Temperature, humidity, and pressure readings
- **Multiple Display Modes**:
  - Main View: Current readings with large text
  - Trends View: Historical data tracking
  - Statistics View: Min/avg/max values
- **Button Controls**:
  - Button A: Cycle through display modes
  - Button B: Toggle between Celsius and Fahrenheit
- **Calibrated Sensors**: Professionally calibrated for accuracy
- **Color Display**: Easy-to-read 240×240 IPS screen
- **Status Indicators**: NeoPixel LED shows sensor readings

## Applications

### Environmental Monitoring (Current Implementation)
The CLUE provides accurate environmental data for indoor climate monitoring, server rooms, greenhouses, weather stations, and general home automation.

### Food Safety Device (Design Concept)
The CLUE can be adapted as a **Leftover Food Safety Device** to monitor refrigerated food storage. See [FOOD_SAFETY_APPLICATION.md](FOOD_SAFETY_APPLICATION.md) for detailed design specifications including:
- FDA-compliant food safety monitoring
- Color-coded safety zones (GREEN/YELLOW/RED)
- 4°C threshold detection with time tracking
- Multi-day storage monitoring
- Bluetooth connectivity for remote monitoring
- Support for multiple sensors

This demonstrates the versatility of the calibrated CLUE platform for both general environmental monitoring and specialized food safety applications.

## 📸 Display Screenshots

### Mode 1: Main View - Real-time Readings
The default display showing current sensor readings with color-coded comfort indicators.

```
╔════════════════════════════════════════╗
║                                        ║
║        CLUE Monitor                    ║
║                                        ║
║                                        ║
║   Temp: 22.5°C         🟢 Comfortable  ║
║                                        ║
║   RH: 45.2%            🔵 Comfortable  ║
║                                        ║
║   P: 1013 hPa                          ║
║                                        ║
║   Alt: 125 m                           ║
║                                        ║
║                                        ║
║   Uptime: 15m 30s                      ║
║                                        ║
║                                        ║
║   A:Mode B:C/F                         ║
║                                        ║
╚════════════════════════════════════════╝
```

**Features:**
- Temperature with color coding (🔵 cold, 🟢 comfortable, 🟠 hot)
- Humidity with comfort indication
- Barometric pressure in hPa
- Calculated altitude in meters
- Running uptime counter

---

### Mode 2: Trends View - Historical Analysis
Press Button A once to see trend analysis based on 2 hours of collected data.

```
╔════════════════════════════════════════╗
║                                        ║
║           Trends                       ║
║                                        ║
║                                        ║
║   Temp: Rising +0.3                    ║
║                                        ║
║                                        ║
║   RH: Stable                           ║
║                                        ║
║                                        ║
║   Pres: Falling -1.2                   ║
║                                        ║
║                                        ║
║                                        ║
║   45 data points                       ║
║                                        ║
║                                        ║
║   A:Mode B:C/F                         ║
║                                        ║
╚════════════════════════════════════════╝
```

**Features:**
- Temperature trend (rising/falling/stable)
- Humidity trend analysis
- Pressure trend (useful for weather prediction)
- Data collection progress (max 120 points = 2 hours)

---

### Mode 3: Statistics View - Min/Avg/Max
Press Button A twice to see statistical analysis over the collection period.

```
╔════════════════════════════════════════╗
║                                        ║
║        Statistics                      ║
║                                        ║
║                                        ║
║   Temp: 21.5/22.3/23.1C                ║
║                                        ║
║   RH: 42/45/48%                        ║
║                                        ║
║   Pres: 1012/1013/1015hPa              ║
║                                        ║
║   (min/avg/max)                        ║
║                                        ║
║                                        ║
║   Offset: -1.0C                        ║
║                                        ║
║                                        ║
║   A:Mode B:C/F                         ║
║                                        ║
╚════════════════════════════════════════╝
```

**Features:**
- Minimum, average, and maximum values
- Temperature calibration offset displayed
- All values update in real-time as data is collected
- Format: min/avg/max for easy reading

---

### Button Controls Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│    [A]  ← Button A                                      │
│                                                         │
│         ┌──────────────────────────┐                    │
│         │                          │                    │
│         │   1.3" Color Display     │                    │
│         │      240 x 240           │                    │
│         │                          │                    │
│         └──────────────────────────┘                    │
│                                                         │
│    [B]  ← Button B                                      │
│                                                         │
│     (●) ← NeoPixel LED (status indicator)               │
│                                                         │
└─────────────────────────────────────────────────────────┘

Button A: Cycle through display modes
  Main → Trends → Statistics → Main (repeats)

Button B: Toggle temperature unit
  Celsius (°C) ⟷ Fahrenheit (°F)
```

## 🚀 Quick Start

### Hardware Required
- [Adafruit CLUE nRF52840 Express](https://www.adafruit.com/product/4500)
- USB-C cable
- Optional: Reference thermometer for calibration

### Installation

1. **Ensure CircuitPython is installed** on your CLUE (version 9.2.4 or later)
   - Download from [circuitpython.org](https://circuitpython.org/board/clue_nrf52840_express/)

2. **Clone this repository**
   ```bash
   git clone https://github.com/jeremycohoe/clue-environmental-monitor.git
   cd clue-environmental-monitor
   ```

3. **Copy to CLUE**
   ```bash
   # Mount your CLUE (appears as CIRCUITPY drive)
   sudo mount /dev/sdX1 /mnt/clue

   # Copy the main program
   sudo cp code.py /mnt/clue/
   sudo sync
   ```

4. **Done!** The CLUE will automatically restart and run the monitor

### Usage

#### Button Controls
- **Button A** (left): Cycle through Main → Trends → Statistics
- **Button B** (right): Toggle between °C and °F

#### Display Modes
1. **Main View**: Real-time sensor readings
2. **Trends View**: Historical trend analysis
3. **Statistics View**: Min/Avg/Max values

#### Serial Console
Connect to view detailed logging:
```bash
screen /dev/ttyACM0 115200
# or
picocom /dev/ttyACM0 -b 115200
```

## 🎯 Temperature Calibration

The CLUE's temperature sensor reads 0.5-1.5°C higher than ambient due to self-heating. Follow these steps to calibrate:

1. Let CLUE run for 10-15 minutes to stabilize
2. Compare with a reference thermometer
3. Calculate offset: `Reference_Temp - CLUE_Temp`
4. Edit `code.py` line ~30:
   ```python
   TEMP_OFFSET = -1.0  # Replace with your calculated offset
   ```

See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for detailed instructions.

## 📚 Documentation

- **[README.md](README.md)** - Complete hardware capabilities and sensor specifications
- **[QUICK_START.md](QUICK_START.md)** - Quick reference and common tasks
- **[CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md)** - Detailed temperature calibration
- **[DISPLAY_GUIDE.md](DISPLAY_GUIDE.md)** - Visual guide to all display modes
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and file structure
- **[FOOD_SAFETY_APPLICATION.md](FOOD_SAFETY_APPLICATION.md)** - FDA-compliant food safety monitoring design
- **[REFERENCE_CARD.txt](REFERENCE_CARD.txt)** - Quick reference card

## 🔧 Configuration

Edit `code.py` to customize:

```python
# Temperature calibration
TEMP_OFFSET = -1.0          # Your calibration offset (°C)

# Update intervals
UPDATE_INTERVAL = 2         # Display refresh (seconds)
LOG_INTERVAL = 60           # Data logging (seconds)

# History
HISTORY_SIZE = 120          # Data points (2 hours at 1/min)

# Comfort zones
TEMP_MIN_COMFORT = 20.0     # °C
TEMP_MAX_COMFORT = 24.0     # °C
HUMIDITY_MIN_COMFORT = 30.0 # %
HUMIDITY_MAX_COMFORT = 60.0 # %
```

## 📊 Sensors

| Sensor | Measurement | Accuracy | Notes |
|--------|------------|----------|-------|
| SHT31-D | Temperature | ±0.2°C | Apply calibration offset |
| SHT31-D | Humidity | ±2% RH | Generally accurate |
| BMP280 | Pressure | ±1 hPa | For weather trends |
| BMP280 | Altitude | ±1 m | Calculated from pressure |

Additional sensors available but not used in this project:
- LSM6DS33 (accelerometer & gyroscope)
- LIS3MDL (magnetometer)
- APDS9960 (proximity, light, color, gesture)
- PDM microphone

## 📁 Project Structure

```
clue-environmental-monitor/
├── code.py                    # Main program (upload to CLUE)
├── calibrate_temperature.py   # Interactive calibration helper
├── examples/                  # Example programs
│   ├── sensor_test.py        # Test all sensors
│   ├── data_logger.py        # CSV data logging
│   └── weather_station.py    # Weather forecasting
├── backup_20251101_210948/   # Original files backup
│   ├── code.py
│   ├── temp.py
│   └── boot_out.txt
├── README.md                  # This file (GitHub main page)
├── CALIBRATION_GUIDE.md      # Detailed calibration
├── DISPLAY_GUIDE.md          # Visual display reference
├── QUICK_START.md            # Quick start guide
├── PROJECT_SUMMARY.md        # Project overview
└── REFERENCE_CARD.txt        # Quick reference card
```

## 🎓 Example Programs

### Sensor Test
Test all CLUE sensors with detailed output:
```bash
cp examples/sensor_test.py /mnt/clue/code.py
```

### Data Logger
Log environmental data to CSV format:
```bash
cp examples/data_logger.py /mnt/clue/code.py
```

### Weather Station
Full weather station with pressure trends and forecasting:
```bash
cp examples/weather_station.py /mnt/clue/code.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Adafruit Industries](https://www.adafruit.com/) for the CLUE hardware and CircuitPython
- CircuitPython community for excellent documentation and libraries

## 📞 Support

- **Issues**: Please report bugs via [GitHub Issues](https://github.com/jeremycohoe/clue-environmental-monitor/issues)
- **Documentation**: See the `docs/` directory for comprehensive guides
- **Adafruit Forums**: [forums.adafruit.com](https://forums.adafruit.com/)

## 🔗 Links

- [Adafruit CLUE Product Page](https://www.adafruit.com/product/4500)
- [Adafruit CLUE Learn Guide](https://learn.adafruit.com/adafruit-clue)
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [CLUE Library Reference](https://circuitpython.readthedocs.io/projects/clue/)

---

**Made with ❤️ for the Adafruit CLUE community**

**Device**: Adafruit CLUE nRF52840 Express
**Firmware**: CircuitPython 9.2.4
**Created**: November 2025
