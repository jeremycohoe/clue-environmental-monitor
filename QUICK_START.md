# Quick Start Guide - Adafruit CLUE

## What We've Done

✅ **Backed up your original files** to `backup_20251101_210948/`
✅ **Created comprehensive documentation** about CLUE capabilities
✅ **Developed calibrated temperature monitoring** with the new `code.py`
✅ **Provided calibration tools and guides**
✅ **Created example programs** for different use cases

---

## Files Created

### Main Files
- **`README.md`** - Complete documentation of CLUE capabilities and sensors
- **`CALIBRATION_GUIDE.md`** - Detailed temperature calibration instructions
- **`code.py`** - Ready to upload to CLUE (calibrated environmental monitor)
- **`calibrate_temperature.py`** - Interactive calibration helper

### Backup Files (in `backup_20251101_210948/`)
- `code.py` - Your original temperature monitor
- `temp.py` - Alternative temperature display
- `boot_out.txt` - System information

### Example Programs (in `examples/`)
- **`sensor_test.py`** - Test all sensors on the CLUE
- **`data_logger.py`** - Log data to CSV format
- **`weather_station.py`** - Full weather station with forecasting

---

## Next Steps

### 1. Upload the New Code (Recommended)

The new `code.py` includes:
- ✅ Temperature calibration (adjustable offset)
- ✅ Humidity monitoring
- ✅ Pressure and altitude
- ✅ 2-hour historical trending
- ✅ Color-coded comfort indicators
- ✅ Multiple display modes (Main, Trends, Statistics)
- ✅ Button controls (Mode switching, °C/°F toggle)

**To upload:**
```bash
# Copy the new code to CLUE
sudo cp /home/user/clue/code.py /mnt/clue/code.py
sudo sync
```

The CLUE will automatically restart and run the new program!

### 2. Calibrate the Temperature

**Quick calibration:**
1. Let the CLUE run for 10-15 minutes
2. Compare its temperature reading with a reference thermometer
3. Calculate the offset: `OFFSET = Reference_Temp - CLUE_Temp`
4. Edit `code.py` on the CLUE and change line ~30:
   ```python
   TEMP_OFFSET = -1.0  # Change to your calculated value
   ```

**Detailed calibration:**
- See `CALIBRATION_GUIDE.md` for comprehensive instructions
- Or use `calibrate_temperature.py` for interactive calibration

### 3. Using the Main Program

**Button Controls:**
- **Button A**: Cycle through display modes (Main → Trends → Statistics)
- **Button B**: Toggle between Celsius and Fahrenheit

**Display Modes:**

1. **Main View** - Current readings
   - Temperature (color-coded: blue=cold, green=comfortable, orange=hot)
   - Humidity (color-coded)
   - Pressure
   - Altitude
   - Uptime

2. **Trends View** - Historical analysis
   - Temperature trend (Rising/Falling/Stable)
   - Humidity trend
   - Pressure trend
   - Number of data points collected

3. **Statistics View** - Min/Avg/Max
   - Temperature range over 2 hours
   - Humidity range
   - Pressure range
   - Calibration offset display

**Serial Console:**
- Data is logged to serial console every minute
- Connect with: `screen /dev/ttyACM0 115200` or `picocom /dev/ttyACM0 -b 115200`

### 4. Try the Example Programs

**Sensor Test:**
```bash
# Copy sensor test to CLUE as code.py
sudo cp /home/user/clue/examples/sensor_test.py /mnt/clue/code.py
sudo sync
```
This reads ALL sensors and displays values via serial console.

**Data Logger:**
```bash
# Copy data logger to CLUE
sudo cp /home/user/clue/examples/data_logger.py /mnt/clue/code.py
sudo sync
```
Then collect data:
```bash
screen -L /dev/ttyACM0 115200  # Logs to screenlog.0
# or
picocom /dev/ttyACM0 -b 115200 | tee data_log.csv
```

**Weather Station:**
```bash
# Copy weather station to CLUE
sudo cp /home/user/clue/examples/weather_station.py /mnt/clue/code.py
sudo sync
```
Full weather display with pressure trends and forecasting!

---

## Understanding the CLUE Sensors

### Temperature & Humidity (SHT31-D)
- **Accuracy**: ±0.2°C, ±2% RH
- **Issue**: Self-heating (~0.5-1.5°C higher than ambient)
- **Solution**: Apply calibration offset (typically -0.8 to -1.5°C)

### Pressure (BMP280)
- **Range**: 300-1100 hPa
- **Uses**: Weather prediction, altitude measurement
- **Accuracy**: ±1 hPa

### Motion (LSM6DS33)
- 3-axis accelerometer (gravity, movement)
- 3-axis gyroscope (rotation rate)
- Useful for orientation, tap detection, motion sensing

### Magnetometer (LIS3MDL)
- 3-axis magnetic field sensor
- Compass functionality
- Metal detection

### Light & Proximity (APDS9960)
- Color sensing (RGB)
- Proximity detection (~20cm range)
- Gesture detection (up/down/left/right)
- Ambient light level

### Audio
- PDM microphone for sound level
- Built-in buzzer for tones

---

## Common Tasks

### Change Temperature Unit
Press **Button B** to toggle between Celsius and Fahrenheit

### View Historical Trends
Press **Button A** until "Trends" appears at the top

### See Min/Max Values
Press **Button A** until "Statistics" appears

### Adjust Calibration Offset
1. Edit `/mnt/clue/code.py`
2. Find line: `TEMP_OFFSET = -1.0`
3. Change to your value (e.g., `TEMP_OFFSET = -1.2`)
4. Save and CLUE will restart

### Change Update Speed
Edit `code.py`:
```python
UPDATE_INTERVAL = 2  # Display updates (2 seconds)
LOG_INTERVAL = 60    # Data logging (60 seconds)
```

### Monitor via Serial
```bash
# Linux
screen /dev/ttyACM0 115200
# or
picocom /dev/ttyACM0 -b 115200

# To exit screen: Ctrl+A, then K, then Y
# To exit picocom: Ctrl+A, then Ctrl+X
```

---

## Troubleshooting

### CLUE Not Appearing
- Try unplugging and replugging USB
- Check if it's mounted: `ls -la /mnt/clue/`
- If not mounted: `sudo mount /dev/sdb1 /mnt/clue`

### Temperature Seems Wrong
1. Let it stabilize for 10-15 minutes
2. Compare with a reference thermometer
3. Adjust `TEMP_OFFSET` in code.py
4. See CALIBRATION_GUIDE.md for detailed help

### Display Not Updating
- Check if CLUE is responding (LED should blink)
- Press RESET button on CLUE
- Check serial console for errors

### Can't Edit Files
Files are read-only when mounted. To edit:
```bash
# Copy to local, edit, copy back
sudo cp /mnt/clue/code.py ~/clue/code_edit.py
nano ~/clue/code_edit.py
sudo cp ~/clue/code_edit.py /mnt/clue/code.py
sudo sync
```

### Reset to Factory Settings
Double-press the RESET button to enter bootloader mode, then reinstall CircuitPython

---

## Technical Specifications

- **Processor**: nRF52840 ARM Cortex-M4F @ 64 MHz
- **Memory**: 2 MB Flash, 256 KB RAM
- **Display**: 1.3" 240x240 IPS TFT
- **Connectivity**: BLE 5.0, USB-C, I2C, SPI, UART
- **Power**: USB or battery (via JST connector)
- **CircuitPython**: Version 9.2.4

---

## Resources

- **Full Documentation**: See `README.md`
- **Calibration Guide**: See `CALIBRATION_GUIDE.md`
- **Example Code**: See `examples/` directory
- **Adafruit Learn**: https://learn.adafruit.com/adafruit-clue
- **CircuitPython Docs**: https://docs.circuitpython.org/

---

## Current Recommended Action

**Upload the new calibrated code:**
```bash
sudo cp /home/user/clue/code.py /mnt/clue/code.py
sudo sync
```

Then watch the CLUE display! Press Button A to cycle through modes.

For serial output:
```bash
screen /dev/ttyACM0 115200
```

Enjoy your fully-featured CLUE environmental monitor! 🎉
