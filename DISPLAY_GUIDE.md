# CLUE Environmental Monitor - Display Guide

## Display Modes Overview

Your CLUE has **3 display modes** that you can cycle through by pressing **Button A**.

---

## Mode 1: MAIN VIEW (Default)

**What it shows:** Current real-time sensor readings

```
┌────────────────────────────────────────┐
│                                        │
│        CLUE Monitor                    │
│                                        │
│                                        │
│   Temp: 22.5°C                         │
│                                        │
│   RH: 45.2%                            │
│                                        │
│   P: 1013 hPa                          │
│                                        │
│   Alt: 125 m                           │
│                                        │
│                                        │
│   Uptime: 15m 30s                      │
│                                        │
│                                        │
│   A:Mode B:C/F                         │
│                                        │
└────────────────────────────────────────┘
```

**Display Elements:**
- **Title**: "CLUE Monitor" (white text, centered)
- **Temp**: Temperature reading with color coding
  - 🔵 **Blue** if < 20°C (cold)
  - 🟢 **Green** if 20-24°C (comfortable)
  - 🟠 **Orange** if > 24°C (hot)
- **RH**: Relative Humidity percentage with color coding
  - 🟠 **Orange** if < 30% (too dry)
  - 🔵 **Cyan** if 30-60% (comfortable)
  - 🔵 **Blue** if > 60% (too humid)
- **P**: Barometric Pressure in hectopascals (white)
- **Alt**: Altitude in meters (white)
- **Uptime**: How long the CLUE has been running (gray)
- **Help**: Button controls reminder (dark gray)

**Update Frequency**: Every 2 seconds

---

## Mode 2: TRENDS VIEW

**What it shows:** Historical trend analysis over time

```
┌────────────────────────────────────────┐
│                                        │
│           Trends                       │
│                                        │
│                                        │
│   Temp: Rising +0.3                    │
│                                        │
│                                        │
│   RH: Stable                           │
│                                        │
│                                        │
│   Pres: Falling -1.2                   │
│                                        │
│                                        │
│                                        │
│   45 data points                       │
│                                        │
│                                        │
│   A:Mode B:C/F                         │
│                                        │
└────────────────────────────────────────┘
```

**Display Elements:**
- **Title**: "Trends" (white text)
- **Temp trend**: Shows if temperature is rising, falling, or stable
  - Format: "Rising +0.3" (temperature change in °C or °F)
  - "Falling -0.5" (negative change)
  - "Stable" (minimal change < 0.2)
- **RH trend**: Humidity trend
  - Same format as temperature
- **Pres trend**: Pressure trend with color coding
  - 🟢 **Green** if rising (improving weather)
  - 🔴 **Red** if falling (deteriorating weather)
  - ⚪ **White** if stable
- **Data points**: Number of historical readings collected (max 120)
- **Help**: Button controls

**Trend Calculation**: Compares average of recent half vs older half of data

---

## Mode 3: STATISTICS VIEW

**What it shows:** Minimum, average, and maximum values over time

```
┌────────────────────────────────────────┐
│                                        │
│        Statistics                      │
│                                        │
│                                        │
│   Temp: 21.5/22.3/23.1C               │
│                                        │
│   RH: 42/45/48%                        │
│                                        │
│   Pres: 1012/1013/1015hPa             │
│                                        │
│   (min/avg/max)                        │
│                                        │
│                                        │
│   Offset: -1.0C                        │
│                                        │
│                                        │
│   A:Mode B:C/F                         │
│                                        │
└────────────────────────────────────────┘
```

**Display Elements:**
- **Title**: "Statistics" (white text)
- **Temp stats**: min/avg/max temperature (in current unit)
  - Format: "21.5/22.3/23.1C" or "70.7/72.1/73.6F"
- **RH stats**: min/avg/max humidity percentage
  - Format: "42/45/48%"
- **Pres stats**: min/avg/max pressure
  - Format: "1012/1013/1015hPa"
- **Legend**: Explains the format (gray text)
- **Offset**: Current calibration offset applied (gray text)
- **Help**: Button controls

**Statistics Period**: Last 2 hours (120 data points at 1-minute intervals)

---

## Button Controls

### Button A (Left Button)
**Function**: Cycle through display modes

**Sequence**:
```
Main View → Trends → Statistics → Main View (repeats)
```

**Visual Feedback**:
- NeoPixel flashes **yellow** briefly when pressed
- Display immediately switches to next mode

### Button B (Right Button)
**Function**: Toggle temperature unit

**Sequence**:
```
Celsius (°C) ⟷ Fahrenheit (°F)
```

**Visual Feedback**:
- NeoPixel flashes **purple** briefly when pressed
- Temperature values update immediately
- All temperature displays change (Main, Trends, Statistics)

---

## NeoPixel LED Status

The RGB LED on top of the CLUE shows system status:

| Color | Meaning |
|-------|---------|
| 🔵 **Blue** (dim) | Starting up / initializing |
| 🟢 **Green** (dim) | Running normally |
| 🟡 **Yellow** (flash) | Button A pressed (mode change) |
| 🟣 **Purple** (flash) | Button B pressed (unit change) |
| 🔴 **Red** | Error occurred |

**Brightness**: Set to 10% to avoid distraction

---

## Serial Console Output

If you connect to the serial console, you'll see:

```
==================================================
Adafruit CLUE - Calibrated Environmental Monitor
==================================================
Temperature offset: -1.0C
Update interval: 2s
Log interval: 60s
History size: 120 readings
==================================================
Warming up sensors (5 seconds)...
Ready! Starting measurements...

[    60s] T: 22.5C, RH: 45.1%, P: 1013hPa, Alt: 125m
[   120s] T: 22.6C, RH: 45.3%, P: 1013hPa, Alt: 125m
[   180s] T: 22.5C, RH: 45.2%, P: 1014hPa, Alt: 124m
...
```

**Log Format**:
- **Timestamp**: `[XXXs]` - seconds since startup
- **T**: Temperature in Celsius (with calibration applied)
- **RH**: Relative Humidity percentage
- **P**: Pressure in hectopascals
- **Alt**: Altitude in meters

**Frequency**: One line every 60 seconds

---

## Display Characteristics

**Screen Specifications**:
- Size: 1.3 inches diagonal
- Resolution: 240 × 240 pixels
- Type: IPS TFT (good viewing angles)
- Brightness: 70% (adjustable in code)

**Text Sizes**:
- **Title**: Scale 2 (larger)
- **Main readings**: Scale 2 (larger)
- **Secondary info**: Scale 1 (smaller)
- **Help text**: Scale 1 (smaller, dark gray)

**Font**: Terminal font (monospace, built-in)

---

## Color Coding Reference

### Temperature Colors

| Condition | Color | Range |
|-----------|-------|-------|
| Too Cold | 🔵 Blue (`0x0088FF`) | < 20°C (< 68°F) |
| Comfortable | 🟢 Green (`0x00FF00`) | 20-24°C (68-75°F) |
| Too Hot | 🟠 Orange (`0xFF4400`) | > 24°C (> 75°F) |

### Humidity Colors

| Condition | Color | Range |
|-----------|-------|-------|
| Too Dry | 🟠 Orange (`0xFF8800`) | < 30% RH |
| Comfortable | 🔵 Cyan (`0x00CCFF`) | 30-60% RH |
| Too Humid | 🔵 Blue (`0x0088FF`) | > 60% RH |

### Trend Colors

| Trend | Color | Indication |
|-------|-------|------------|
| Rising | 🟢 Green | Increasing values |
| Falling | 🔴 Red | Decreasing values |
| Stable | ⚪ White | Minimal change |

---

## Data Collection & Storage

**Historical Data**:
- **Storage**: 120 data points in RAM (circular buffer)
- **Interval**: 1 reading per minute
- **Duration**: 2 hours of history
- **Update**: Oldest data automatically replaced when buffer is full

**What's Logged**:
- Temperature (calibrated)
- Humidity
- Pressure

**What's Calculated from History**:
- Trends (rising/falling/stable)
- Min/Avg/Max statistics
- Trend magnitude (amount of change)

---

## Display Timing

| Action | Timing |
|--------|--------|
| Display update | Every 2 seconds |
| Data logging | Every 60 seconds |
| Sensor reading | Every 2 seconds |
| Warm-up period | 5 seconds on startup |
| Button response | Immediate |

---

## Example Display Progression

**After Startup (0-5 seconds)**:
```
CLUE Monitor
Temp: --.-C
RH: --.-%
P: ---- hPa
Alt: ---- m
```

**After First Reading (~2 seconds)**:
```
CLUE Monitor
Temp: 23.2C         [Orange - slightly warm]
RH: 52.5%           [Cyan - comfortable]
P: 1013 hPa
Alt: 125 m
Uptime: 2s
```

**After 1 Hour of Collection**:
- Press Button A to see **Trends**:
```
Trends
Temp: Rising +0.2
RH: Falling -1.5
Pres: Stable
60 data points
```

- Press Button A again to see **Statistics**:
```
Statistics
Temp: 22.8/23.1/23.5C
RH: 51/52/54%
Pres: 1012/1013/1014hPa
(min/avg/max)
Offset: -1.0C
```

---

## Troubleshooting Display Issues

| Issue | Solution |
|-------|----------|
| Display blank | Press RESET button on CLUE |
| Values show `--` | Wait 2-5 seconds for first reading |
| Trends show "Insufficient data" | Wait 1-2 minutes for data collection |
| Statistics show nothing | Need at least 2 data points (2 minutes) |
| Button not responding | Press firmly, not too fast |
| Wrong temperature unit | Press Button B to toggle |

---

## Customization Options

If you want to modify the display, here are the key settings in `code.py`:

```python
# Line ~30-50 - Configuration
TEMP_OFFSET = -1.0          # Calibration offset
UPDATE_INTERVAL = 2         # Display refresh (seconds)
LOG_INTERVAL = 60           # Data logging (seconds)
HISTORY_SIZE = 120          # Data points to keep

# Comfort thresholds
TEMP_MIN_COMFORT = 20.0     # Cold threshold (°C)
TEMP_MAX_COMFORT = 24.0     # Hot threshold (°C)
HUMIDITY_MIN_COMFORT = 30.0 # Dry threshold (%)
HUMIDITY_MAX_COMFORT = 60.0 # Humid threshold (%)

# Display brightness
display.brightness = 0.7    # 0.0 to 1.0
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  CLUE ENVIRONMENTAL MONITOR             │
├─────────────────────────────────────────┤
│                                         │
│  Button A: Change Display Mode          │
│    Main → Trends → Stats → Main        │
│                                         │
│  Button B: Toggle °C / °F               │
│                                         │
│  LED Colors:                            │
│    🟢 Green = Running OK                │
│    🟡 Yellow Flash = Mode changed       │
│    🟣 Purple Flash = Unit changed       │
│                                         │
│  Display Updates: Every 2 seconds       │
│  Data Logged: Every 60 seconds          │
│  History: 2 hours (120 points)          │
│                                         │
│  Temperature: Color-coded comfort       │
│  Humidity: Color-coded comfort          │
│  Pressure: In hPa                       │
│  Altitude: In meters                    │
│                                         │
└─────────────────────────────────────────┘
```

---

**Created**: November 1, 2025
**Device**: Adafruit CLUE nRF52840 Express
**Firmware**: CircuitPython 9.2.4
