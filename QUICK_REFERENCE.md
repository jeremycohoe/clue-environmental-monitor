# CLUE Environmental Monitor - Quick Reference Card

**Version:** 1.0 | **Date:** November 2025

---

## 🎮 Button Controls

| Button | Action | Result |
|--------|--------|--------|
| **A** | Single Press | Cycle to next mode (4 modes total) |
| **B** | Single Press | Toggle °C ⟷ °F |

---

## 📊 The 4 Display Modes

### 1️⃣ Main View (Default)
**What:** Live sensor readings
**Shows:** Temperature, Humidity, Pressure, Altitude, Uptime
**LED:** 🟢 Green (normal), 🔵 Blue (cold), 🟠 Orange (hot)

### 2️⃣ Trends
**What:** Historical analysis
**Shows:** Rising/Falling/Stable trends, sparkline graphs
**Data:** Last 2 hours (120 samples)

### 3️⃣ Statistics
**What:** Min/Avg/Max values
**Shows:** Statistical ranges for all sensors
**Format:** `min / avg / max`

### 4️⃣ Food Safety 🍔
**What:** FDA leftover monitor
**Shows:** Safe/Warning states
**LED:** ⚪ Ready, 🟢 Safe (<4°C), 🟡 Check temp

---

## 🌡️ Temperature Color Codes

| Color | Meaning | Range |
|-------|---------|-------|
| 🔵 **Blue** | Too Cold | < 20°C |
| 🟢 **Green** | Comfortable | 20-24°C |
| 🟠 **Orange** | Too Hot | > 24°C |

---

## 💧 Humidity Indicators

| Symbol | Meaning | Range |
|--------|---------|-------|
| 🟠 **Orange** | Too Dry | < 30% |
| 🟢 **Green** | Comfortable | 30-60% |
| 🔵 **Blue** | Too Humid | > 60% |

---

## 🍔 Food Safety States

| State | Display | LED | Temperature | Action |
|-------|---------|-----|-------------|--------|
| **READY** | White | ⚪ | Room temp | Place in fridge |
| **SAFE** | Green | 🟢 | ≤ 4°C | Food is safe to eat |
| **CHECK** | Yellow | 🟡 | > 4°C | Monitor closely |

**How to Use:**
1. Press Button A **three times** to enter Food Safety mode
2. Place CLUE in fridge with food container
3. Watch for green "SAFE" display (automatic)
4. Yellow warning if temp rises above 4°C
5. Returns to READY at room temperature

---

## ⚙️ Calibration Values

**Current Settings:**
- Temperature: **-3.5°C** offset
- Humidity: **+5.2%** offset
- Calibrated: **Nov 1, 2025**

**To Recalibrate:** See `CALIBRATION_GUIDE.md`

---

## 🔌 Quick Setup

1. **Plug in CLUE** via USB-C
2. **Wait 5 seconds** for sensor warmup
3. **Green LED** = Ready to use
4. **Press A** to explore modes

---

## 📈 Trend Indicators

| Text | Meaning |
|------|---------|
| **Rising +X.X** | Value increasing |
| **Falling -X.X** | Value decreasing |
| **Stable** | No significant change |
| **Insufficient data** | Less than 2 samples |

---

## 💡 Quick Tips

✅ **Best Accuracy:** Wait 10-15 minutes after power-on for sensors to stabilize
✅ **Weather Prediction:** Falling pressure = rain likely within 12-24 hours
✅ **Food Safety:** Green LED must stay lit for food to be safe
✅ **Battery Use:** Lower display brightness in `code.py` line 90 for longer runtime
✅ **Data Reset:** Unplug and replug to reset history and statistics

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Temp too high | Normal - sensor self-heating. Use calibration offset |
| Button not responding | Press firmly. LED should flash |
| Display blank | Check USB connection, try reset |
| Wrong mode showing | Press Button A to cycle |
| Food Safety not entering | Must press A exactly 3 times from Main |

---

## 📊 Data Collection

- **Update Rate:** Every 2 seconds (display refresh)
- **Log Rate:** Every 60 seconds (history storage)
- **History Size:** 120 samples = 2 hours maximum
- **Memory:** Resets on power cycle

---

## 🔋 Power Options

| Method | Duration | Notes |
|--------|----------|-------|
| USB | Unlimited | Recommended for 24/7 monitoring |
| LiPo Battery | ~8-12 hours | 350-500mAh battery recommended |
| AAA Pack | ~6-8 hours | 3x AAA in holder |

---

## 📁 Files You Need

**Essential:**
- `code.py` - Main program (all 4 modes)

**Optional:**
- `food_safety.py` - Standalone food monitor
- `calibrate_interactive.py` - Calibration tool

---

## 🌐 More Info

- **Full Documentation:** `README.md`
- **Food Safety Guide:** `FOOD_SAFETY_USAGE.md`
- **Calibration Help:** `CALIBRATION_GUIDE.md`
- **GitHub:** https://github.com/jeremycohoe/clue-environmental-monitor

---

**Print this card for quick reference! 📄**
