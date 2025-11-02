# Adafruit CLUE Environmental Monitor

A comprehensive environmental monitoring system for the Adafruit CLUE nRF52840 Express with calibrated sensors, historical trending, and **4 interactive display modes** including an FDA-compliant food safety monitor.

![CLUE Badge](https://img.shields.io/badge/Adafruit-CLUE-blueviolet)
![CircuitPython](https://img.shields.io/badge/CircuitPython-9.2.4-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Features

- **4 Display Modes** - Cycle with Button A:
  - **Mode 1:** Main View - Live sensor readings with color-coded comfort zones
  - **Mode 2:** Trends - Historical data analysis with sparkline graphs
  - **Mode 3:** Statistics - Min/Avg/Max values from 2 hours of data
  - **Mode 4:** Food Safety - FDA-compliant leftover monitoring
- **Dual Temperature Units** - Toggle °C/°F with Button B
- **Calibrated Sensors** - Professional calibration (-3.5°C, +5.2% RH)
- **Visual Feedback** - NeoPixel LED indicates status (Green=OK, Yellow=Warning, etc.)
- **Memory Optimized** - Efficient code runs smoothly on 256KB RAM

## 🚀 Quick Start

1. **Power On** - Connect CLUE via USB or battery
2. **Cycle Modes** - Press **Button A** to switch between 4 displays
3. **Toggle Units** - Press **Button B** for Celsius ⟷ Fahrenheit
4. **Food Safety** - Press **Button A** three times to enter Mode 4

## 📊 The Four Display Modes

### Mode 1: Main View - Real-Time Monitoring
**Default display** showing current environmental conditions with color-coded comfort indicators.

```
┌─────────────────────────────────────┐
│                                     │
│       CLUE Monitor                  │
│                                     │
│  Temp: 22.5 C    🟢 Comfortable     │
│                                     │
│  RH: 45.2%       🟢 Comfortable     │
│                                     │
│  P: 1013 hPa                        │
│                                     │
│  Alt: 125 m                         │
│                                     │
│  Uptime: 15m 30s                    │
│                                     │
│  A:Mode B:C/F                       │
│                                     │
└─────────────────────────────────────┘
```

**What You See:**
- 🌡️ **Temperature** - Color coded: Blue (cold), Green (comfort), Orange (hot)
- 💧 **Humidity** - Comfort range 30-60%
- 📊 **Pressure** - Barometric pressure in hPa
- 🏔️ **Altitude** - Calculated from pressure
- ⏱️ **Uptime** - Time since device started

**LED Indicator:** Green = All readings in comfort zone

---

### Mode 2: Trends - Historical Analysis
**Press Button A once** to see trend analysis based on the last 2 hours of data (120 samples).

```
┌─────────────────────────────────────┐
│                                     │
│          Trends                     │
│                                     │
│  Temp: Rising +0.3                  │
│  .-:=+*#@@@  ← ASCII sparkline      │
│                                     │
│  RH: Stable                         │
│  ===++=+==+                         │
│                                     │
│  Pres: Falling -2.1                 │
│  @##*+==:--.                        │
│                                     │
│  2hr history (120 pts)              │
│                                     │
└─────────────────────────────────────┘
```

**What You See:**
- 📈 **Trend Direction** - Rising, Falling, or Stable for each sensor
- 📉 **ASCII Sparklines** - Visual mini-charts using characters ` .-:=+*#@`
  - ` ` (space) and `.` = Lowest values
  - `-` `:` `=` = Low to medium values
  - `+` `*` `#` `@` = Medium to highest values
- 🔢 **Change Values** - Numerical difference from older to recent average

**What You See:**
- � **Trend Direction** - Rising, Falling, or Stable for each sensor
- 📉 **Sparkline Graphs** - Visual mini-charts showing data progression
- 🔢 **Change Values** - Numerical difference from older to recent average

**Use Cases:**
- Weather prediction (falling pressure = rain coming)
- HVAC monitoring (temperature trending)
- Leak detection (humidity trending up)

---

### Mode 3: Statistics - Min/Avg/Max
**Press Button A twice** to see statistical summary of collected data.

```
┌─────────────────────────────────────┐
│                                     │
│        Statistics                   │
│                                     │
│  Temp: 20.1/22.5/24.3 C             │
│        Min / Avg / Max              │
│                                     │
│  RH: 38/45/52%                      │
│                                     │
│  P: 1010/1013/1016 hPa              │
│                                     │
│  Trend: 2hr window                  │
│  Samples: 120                       │
│                                     │
└─────────────────────────────────────┘
```

**What You See:**
- 📊 **Min/Avg/Max** - Statistical range for each sensor
- � **Sample Count** - Number of data points collected
- ⏰ **Time Window** - Duration of statistics (2 hours max)

**Use Cases:**
- Daily temperature range tracking
- Indoor climate stability assessment
- Data logging and record keeping

---

### Mode 4: Food Safety Monitor 🍔
**Press Button A three times** to enter FDA-compliant leftover food safety monitoring mode.

```
┌─────────────────────────────────────┐
│                                     │
│      FOOD SAFETY                    │
│                                     │
│         SAFE                        │
│                                     │
│    Temp: 3.2 C                      │
│                                     │
│    Food is safe                     │
│                                     │
│    OK to eat                        │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Color-Coded States:**

| State | Display | LED Color | Meaning |
|-------|---------|-----------|---------|
| **READY** | White | ⚪ White | Waiting - place food in fridge |
| **SAFE** | Green | 🟢 Green | Temperature ≤ 4°C, food is safe |
| **CHECK TEMP** | Yellow | 🟡 Yellow | Above 4°C, monitor closely |

**How It Works:**
1. **Start:** Display shows "READY" (white) at room temperature
2. **Fridge:** Place in fridge - automatically enters SAFE mode when temp reaches 4°C
3. **Monitor:** Green LED and display confirm food safety
4. **Alert:** Yellow warning if temperature rises above safe threshold
5. **Reset:** Returns to READY when back at room temperature (≥21°C)

**FDA Guidelines Implemented:**
- ✅ 4°C (40°F) safe refrigerator temperature
- ✅ Visual alerts for temperature violations
- ✅ Automatic state tracking

**Pro Tip:** For the full 5-state version with 2-hour danger zone tracking and 4-day storage limits, use the standalone `food_safety.py` application.

---

## 🎮 Button Controls

| Button | Function | Description |
|--------|----------|-------------|
| **A (Left)** | Cycle Modes | Main → Trends → Stats → Food Safety → Main... |
| **B (Right)** | Toggle Units | Switch between Celsius (°C) and Fahrenheit (°F) |

**LED Flash Feedback:**
- Yellow flash = Mode changed (Button A)
- Magenta flash = Units changed (Button B)
- Steady green = Normal operation

---

## 📦 What's Included

### Core Files
- **`code.py`** - Main 4-mode environmental monitor (THIS IS WHAT YOU RUN)
- **`food_safety.py`** - Standalone FDA food safety monitor (5-state full version)
- **`CODE_REVIEW.md`** - Code optimization analysis and improvements

### Documentation
- **`README.md`** - Complete project documentation (you are here!)
- **`QUICK_REFERENCE.md`** - One-page quick reference card
- **`TROUBLESHOOTING.md`** - Common issues and solutions
- **`FOOD_SAFETY_APPLICATION.md`** - FDA food safety design specifications
- **`FOOD_SAFETY_USAGE.md`** - How to use the food safety monitor
- **`FOOD_SAFETY_QUICKSTART.md`** - Quick start for food safety mode
- **`IMPLEMENTATION_SUMMARY.md`** - Technical implementation details
- **`DISPLAY_GUIDE.md`** - Visual guide to all display modes
- **`PROJECT_SUMMARY.md`** - Project overview

### Utilities
- **`calibrate_interactive.py`** - Interactive calibration tool
- **`button_test.py`** - Test button responsiveness

---

## 🚀 Quick Start

### Step 1: Install CircuitPython
1. Download CircuitPython 9.2.4+ from [circuitpython.org](https://circuitpython.org/board/clue_nrf52840_express/)
2. Double-click CLUE's reset button → CLUEBOOT drive appears
3. Drag `.uf2` file to CLUEBOOT drive
4. Wait for restart → CIRCUITPY drive appears

### Step 2: Upload Code
```bash
# Linux/Mac
sudo mount /dev/sdX1 /mnt/clue
sudo cp code.py /mnt/clue/
sudo sync

# Windows
# Just copy code.py to CIRCUITPY drive
```

### Step 3: Use It!
- **Green LED** = Ready
- **Press Button A** = Cycle modes (Main → Trends → Stats → Food Safety)
- **Press Button B** = Toggle °C/°F

**That's it!** 🎉

---

## 📚 Documentation Quick Links

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [README.md](README.md) | Complete reference | Understanding all features |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | One-page cheat sheet | Daily use, printed reference |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Fix problems | Something not working |
| [FOOD_SAFETY_USAGE.md](FOOD_SAFETY_USAGE.md) | Food monitor guide | Using Mode 4 (Food Safety) |
| [CODE_REVIEW.md](CODE_REVIEW.md) | Code analysis | Developers, optimization info |

---

## 🔧 Configuration

Edit the top of `code.py` to customize:

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

## 📊 Technical Specifications

### Hardware: Adafruit CLUE nRF52840 Express

| Component | Specification |
|-----------|--------------|
| **Processor** | Nordic nRF52840 (ARM Cortex-M4, 64 MHz) |
| **Memory** | 256 KB RAM, 1 MB Flash, 2 MB SPI Flash |
| **Display** | 1.3" IPS TFT, 240×240 pixels, 65K colors |
| **Sensors** | Temperature, Humidity, Pressure, Motion, Light, Gesture |
| **Power** | USB-C or 3.7V LiPo battery |
| **Dimensions** | 2.0" × 2.4" × 0.5" |

### Sensors Used in This Project

| Sensor | Type | Measurement | Accuracy | Range |
|--------|------|-------------|----------|-------|
| **SHT31-D** | Temp/Humid | Temperature | ±0.2°C | -40°C to 125°C |
| **SHT31-D** | Temp/Humid | Humidity | ±2% RH | 0-100% RH |
| **BMP280** | Pressure | Barometric | ±1 hPa | 300-1100 hPa |
| **BMP280** | Altitude | Calculated | ±1 m | 0-9000 m |

**Note:** CLUE has additional sensors (accelerometer, magnetometer, light, gesture, microphone) not used in this environmental monitor.

---

## 📁 Complete Project Structure

```
clue-environmental-monitor/
│
├── 📄 code.py                           # Main program (4 modes)
├── 📄 food_safety.py                    # Standalone food safety (5 states)
├── 📄 button_test.py                    # Button testing utility
├── 📄 calibrate_interactive.py          # Calibration helper
│
├── 📚 Documentation/
│   ├── README.md                        # This file (complete reference)
│   ├── QUICK_REFERENCE.md               # One-page cheat sheet 📋
│   ├── TROUBLESHOOTING.md               # Problem solving guide 🔧
│   ├── CODE_REVIEW.md                   # Code analysis & optimization
│   ├── FOOD_SAFETY_APPLICATION.md       # FDA food safety design
│   ├── FOOD_SAFETY_USAGE.md             # Food safety user guide
│   ├── FOOD_SAFETY_QUICKSTART.md        # Food safety quick start
│   ├── IMPLEMENTATION_SUMMARY.md        # Technical details
│   ├── DISPLAY_GUIDE.md                 # Display modes visual guide
│   └── PROJECT_SUMMARY.md               # Project overview
│
└── 📁 backup_*/                         # Automatic backups
```

---

## 🎓 Use Cases

### 🏠 Home Climate Monitoring
- Track indoor temperature and humidity for comfort
- Monitor HVAC system effectiveness
- Detect humidity issues (mold prevention)
- 24/7 environmental logging

### �️ Weather Tracking
- Barometric pressure trends predict weather changes
- Falling pressure = rain likely within 12-24 hours
- Rising pressure = improving weather conditions
- Track daily temperature ranges

### 🍔 Food Safety (Mode 4)
- Monitor refrigerator temperature compliance
- Track leftover food safety (FDA guidelines)
- Prevent foodborne illness
- Visual alerts for temperature violations

### 🌱 Greenhouse Monitoring
- Optimal growing conditions tracking
- Humidity control for plants
- Temperature stability verification
- Climate data collection

### 💻 Server Room / Data Center
- Temperature monitoring for equipment
- Humidity control (prevent static damage)
- Altitude/pressure for cooling calculations
- 24/7 unattended monitoring

### 🏢 Office / Workspace
- Comfort zone compliance (OSHA guidelines)
- Air quality assessment
- HVAC efficiency tracking
- Employee comfort optimization

---

## 🔋 Power Options & Battery Life

| Power Source | Duration | Notes |
|--------------|----------|-------|
| **USB-C** | Unlimited | Recommended for 24/7 monitoring |
| **LiPo Battery (500mAh)** | ~10-12 hours | With display.brightness = 0.7 |
| **LiPo Battery (500mAh)** | ~18-24 hours | With display.brightness = 0.3 |
| **3×AAA Battery Pack** | ~8-10 hours | Using AAA holder accessory |

**Power Optimization Tips:**
- Lower `display.brightness` to 0.3-0.5 for battery use
- Increase `UPDATE_INTERVAL` to 5-10 seconds
- Use standalone food safety mode (no trends/stats = less CPU)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with clear comments
4. **Test thoroughly** on actual CLUE hardware
5. **Commit** (`git commit -m 'Add amazing feature'`)
6. **Push** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

**Areas for Contribution:**
- Additional display modes
- Data export features (CSV, JSON)
- BLE connectivity for remote monitoring
- More sensor integration (light, gesture, motion)
- Improved calibration tools
- Translation/localization

---

## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Jeremy Cohoe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **[Adafruit Industries](https://www.adafruit.com/)** - For the amazing CLUE hardware and CircuitPython ecosystem
- **CircuitPython Community** - For excellent documentation and support
- **FDA Food Safety Guidelines** - For food storage safety standards
- **Contributors** - Everyone who has helped improve this project

---

## 📞 Support & Contact

### Get Help
- 📖 **Read the Docs**: Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 🔧 **Troubleshooting**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💬 **GitHub Issues**: [Report bugs or request features](https://github.com/jeremycohoe/clue-environmental-monitor/issues)
- 🌐 **Adafruit Forums**: [forums.adafruit.com](https://forums.adafruit.com/viewforum.php?f=60)

### Useful Links
- [Adafruit CLUE Product Page](https://www.adafruit.com/product/4500)
- [CLUE Learn Guide](https://learn.adafruit.com/adafruit-clue)
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [CLUE Library Reference](https://circuitpython.readthedocs.io/projects/clue/)
- [This Project on GitHub](https://github.com/jeremycohoe/clue-environmental-monitor)

---

## 🌟 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/jeremycohoe/clue-environmental-monitor)
![GitHub issues](https://img.shields.io/github/issues/jeremycohoe/clue-environmental-monitor)
![GitHub stars](https://img.shields.io/github/stars/jeremycohoe/clue-environmental-monitor)

**Current Version:** 1.0 (Optimized)
**Last Updated:** November 2, 2025
**Status:** ✅ Production Ready

**Recent Updates:**
- ✅ November 2, 2025: Code optimization, removed duplication, added Mode 4 (Food Safety)
- ✅ November 1, 2025: Calibration completed, button responsiveness improved
- ✅ October 2025: Initial release with 3 display modes

---

## 🎯 Roadmap

### ✅ Completed
- [x] 4 interactive display modes
- [x] Calibrated temperature and humidity
- [x] Responsive button controls
- [x] Food safety monitoring (Mode 4)
- [x] Comprehensive documentation
- [x] Code optimization and cleanup

### 🚧 In Progress
- [ ] BLE data streaming to phone/computer
- [ ] CSV data export to flash storage
- [ ] Web dashboard (if WiFi added)

### 💭 Future Ideas
- [ ] Alarm system with buzzer
- [ ] Graph plotting on display
- [ ] Multiple sensor integration
- [ ] Time-series data analysis
- [ ] Machine learning trend prediction
- [ ] MQTT integration for IoT

---

<div align="center">

**Made with ❤️ for the Adafruit CLUE Community**

🌡️ 💧 📊 🍔

**[⬆ Back to Top](#adafruit-clue-environmental-monitor)**

</div>

---

**Device**: Adafruit CLUE nRF52840 Express
**Firmware**: CircuitPython 9.2.4+
**Created**: November 2025
**Author**: Jeremy Cohoe
**Repository**: [github.com/jeremycohoe/clue-environmental-monitor](https://github.com/jeremycohoe/clue-environmental-monitor)
