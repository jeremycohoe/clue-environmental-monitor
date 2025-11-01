# Temperature Calibration Guide for Adafruit CLUE

## Quick Start Calibration

### What You Need
1. Adafruit CLUE (connected and running)
2. Reference thermometer (digital thermometer, weather station, or smartphone with temperature sensor)
3. 30 minutes of time
4. Stable environment (no drafts, direct sunlight, or heat sources)

---

## Step-by-Step Calibration Process

### Step 1: Prepare the Environment

1. **Choose a stable location**:
   - Indoor room with stable temperature
   - Away from windows, heaters, or air vents
   - No direct sunlight
   - Minimal air movement

2. **Position the devices**:
   - Place CLUE and reference thermometer side-by-side
   - Keep them at the same height (on a table/desk)
   - Ensure both have similar airflow conditions
   - Keep them at least 30cm (1 foot) apart to avoid heat interference

### Step 2: Warm-Up Period

1. **Connect the CLUE** via USB and let it run
2. **Wait 10-15 minutes** for the board to reach thermal equilibrium
   - The processor generates heat, warming the sensor
   - Temperature will stabilize after this period
3. **Monitor the readings** - they should stop increasing after stabilization

### Step 3: Take Measurements

**Using the calibration script (recommended)**:

1. Copy `calibrate_temperature.py` to your CLUE as `code.py`
2. Connect to the serial console to see readings
3. The script will:
   - Display current CLUE temperature
   - Prompt you to enter reference temperature
   - Calculate and display the offset
   - Show corrected readings

**Manual method**:

1. **Record multiple readings** over 30 minutes:
   ```
   Time    CLUE Reading    Reference Reading    Difference
   0 min   23.2°C         21.8°C               +1.4°C
   10 min  23.5°C         21.9°C               +1.6°C
   20 min  23.4°C         22.0°C               +1.4°C
   30 min  23.5°C         22.0°C               +1.5°C
   ```

2. **Calculate the average difference**:
   ```
   Average CLUE: 23.4°C
   Average Reference: 21.9°C
   Offset = 21.9 - 23.4 = -1.5°C
   ```

### Step 4: Apply the Calibration

1. **Open `code.py`** on your CLUE
2. **Find the line** near the top:
   ```python
   TEMP_OFFSET = -1.0
   ```
3. **Replace** with your calculated offset:
   ```python
   TEMP_OFFSET = -1.5  # Your calculated value
   ```
4. **Save the file** - CLUE will automatically restart
5. **Verify** - readings should now match your reference thermometer

---

## Validation and Fine-Tuning

### Initial Validation

After applying the offset:
1. Wait another 10 minutes for stabilization
2. Compare readings again
3. If difference is > 0.3°C, adjust the offset further

### Test in Different Conditions

For best accuracy, test in multiple scenarios:

**Different temperatures**:
- Cool room (18-20°C)
- Comfortable room (20-24°C)
- Warm room (24-28°C)

**Different orientations**:
- Flat on table (display up)
- Standing vertical
- Display facing down

**Different power modes**:
- USB powered
- Battery powered (if applicable)

### Creating a Calibration Table

If readings vary by orientation or temperature range, create a lookup table:

```python
# In code.py
def get_calibration_offset(raw_temp):
    """Get offset based on temperature range."""
    if raw_temp < 22:
        return -0.8  # Less self-heating when cold
    elif raw_temp < 25:
        return -1.2  # Typical room temperature
    else:
        return -1.5  # More self-heating when warm
```

---

## Common Calibration Values

Based on typical usage patterns:

| Scenario | Expected Offset | Notes |
|----------|----------------|-------|
| USB powered, active display | -1.0 to -1.5°C | Most common |
| USB powered, minimal updates | -0.8 to -1.2°C | Lower CPU usage |
| Battery powered | -0.5 to -0.8°C | Less heat generation |
| Enclosed case | -1.5 to -2.0°C | Reduced airflow |
| External sensor (future mod) | 0°C | Direct ambient reading |

---

## Advanced Calibration Techniques

### Two-Point Calibration

For maximum accuracy across temperature ranges:

1. **Calibrate at two temperatures**:
   - Cold point: ~15-18°C (refrigerator)
   - Hot point: ~30-35°C (warm room)

2. **Calculate linear correction**:
   ```python
   # Measured points
   clue_cold = 16.5
   ref_cold = 15.0
   clue_hot = 32.0
   ref_hot = 30.0

   # Calculate slope and offset
   slope = (ref_hot - ref_cold) / (clue_hot - clue_cold)
   offset = ref_cold - (slope * clue_cold)

   # Apply correction
   def calibrated_temp(raw):
       return (slope * raw) + offset
   ```

### Using BMP280 as Reference

The CLUE also has a BMP280 pressure sensor with temperature measurement:

```python
import board
import adafruit_bmp280

i2c = board.I2C()
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Compare both sensors
sht_temp = clue.temperature
bmp_temp = bmp.temperature

# BMP280 may have different self-heating characteristics
# Use the difference to estimate correction
```

### Environmental Correction

Account for measurement conditions:

```python
# Adjust based on humidity (affects heat dissipation)
def humidity_correction(temp_offset, humidity):
    """Adjust offset based on humidity level."""
    if humidity > 70:
        return temp_offset - 0.2  # High humidity = more heat retention
    elif humidity < 30:
        return temp_offset + 0.1  # Low humidity = better cooling
    return temp_offset
```

---

## Troubleshooting Calibration Issues

### Problem: Readings Still Don't Match

**Possible causes**:
1. **Different measurement conditions**
   - Solution: Ensure both sensors are in identical conditions

2. **Reference thermometer inaccuracy**
   - Solution: Use multiple reference thermometers or a known-accurate device

3. **Thermal mass differences**
   - Solution: Wait longer for equilibrium (20-30 minutes)

4. **Air movement**
   - Solution: Reduce drafts, close windows/doors

### Problem: Offset Changes Over Time

**Possible causes**:
1. **Varying CPU load**
   - Solution: Maintain consistent update intervals

2. **Ambient temperature changes**
   - Solution: Use temperature-dependent offset (see Advanced section)

3. **Power source changes**
   - Solution: Calibrate for each power mode separately

### Problem: Different Readings by Orientation

**Solution**:
- Calibrate in your most common orientation
- Or create orientation-specific offsets using the accelerometer

```python
from adafruit_clue import clue

def get_orientation_offset():
    """Determine offset based on board orientation."""
    x, y, z = clue.acceleration

    if z > 9:  # Display facing up
        return -1.2
    elif z < -9:  # Display facing down
        return -0.8
    else:  # Vertical
        return -1.0
```

---

## Validation Tests

### Quick Validation (5 minutes)

1. Read CLUE temperature
2. Read reference temperature
3. Difference should be < 0.5°C

### Standard Validation (30 minutes)

1. Take readings every 5 minutes
2. Calculate average difference
3. Should be < 0.3°C average error

### Comprehensive Validation (24 hours)

1. Log readings hourly
2. Compare daily min/max/average
3. Track correlation coefficient (should be > 0.95)

---

## Documenting Your Calibration

Keep a record of your calibration:

```python
"""
CLUE Temperature Calibration Record
====================================
Device UID: B6060B5384F2F8C4
Calibration Date: 2025-11-01

Reference Device: Acurite Digital Thermometer (Model XYZ)
Reference Accuracy: ±0.3°C

Test Conditions:
- Location: Living room, center of room
- Time: 14:00-14:30
- Weather: Clear, stable
- HVAC: Off

Measurements:
- CLUE average: 23.4°C
- Reference average: 22.2°C
- Calculated offset: -1.2°C

Validation:
- Test date: 2025-11-01 15:00
- Average error after calibration: 0.2°C
- Status: PASSED

Notes:
- Slight variation when display updates frequently
- Consider reducing update rate for stable readings
"""
```

---

## Next Steps

After successful calibration:

1. **Test the main monitoring program**: Run `code.py` with your offset
2. **Verify accuracy**: Compare readings over several hours
3. **Document results**: Note any remaining discrepancies
4. **Re-calibrate periodically**: Every 3-6 months or after firmware updates

---

## Quick Reference Commands

### Check current temperature (serial console):
```python
from adafruit_clue import clue
print(f"Raw: {clue.temperature:.1f}°C")
```

### Apply offset manually:
```python
OFFSET = -1.2  # Your value
calibrated = clue.temperature + OFFSET
print(f"Calibrated: {calibrated:.1f}°C")
```

### Compare with BMP280:
```python
import adafruit_bmp280
i2c = board.I2C()
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
print(f"SHT31: {clue.temperature:.1f}°C")
print(f"BMP280: {bmp.temperature:.1f}°C")
```
