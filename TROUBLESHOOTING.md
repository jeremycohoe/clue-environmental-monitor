# Troubleshooting Guide
## CLUE Environmental Monitor

**Last Updated:** November 2, 2025

---

## 🚨 Common Issues & Solutions

### Display Issues

#### ❌ Display is Blank / Black Screen
**Symptoms:** No display output, but device powers on

**Solutions:**
1. Check USB-C connection is secure
2. Try a different USB cable (some are charge-only)
3. Check display brightness setting in `code.py` (line ~90)
   ```python
   display.brightness = 0.7  # Increase to 1.0
   ```
4. Try hard reset: Unplug, wait 10 seconds, replug
5. Check for `code.py` syntax errors via serial console

**Prevention:** Use quality USB cables with data lines

---

#### ❌ Display Frozen / Not Updating
**Symptoms:** Display shows readings but they don't change

**Solutions:**
1. Check if CLUE is running or crashed
2. Connect to serial console: `screen /dev/ttyACM0 115200`
3. Look for Python error messages
4. Check UPDATE_INTERVAL setting (should be 2 seconds)
5. Hard reset device

**Common Causes:**
- Memory allocation error
- Syntax error in code
- Infinite loop condition

---

#### ❌ Wrong Mode Showing
**Symptoms:** Can't get to desired mode, or skips modes

**Solutions:**
1. Press Button A repeatedly to cycle: Main → Trends → Stats → Food Safety
2. Check button responsiveness (should see yellow LED flash)
3. Ensure `% 4` in code (not `% 3`) - line ~516 and ~562
4. Hard reset and try again

---

### Button Issues

#### ❌ Buttons Not Responding
**Symptoms:** Pressing A or B does nothing, no LED flash

**Solutions:**
1. Press buttons firmly (they require good contact)
2. Check for yellow/magenta LED flash on press
3. Look at serial console for "Button A/B detected!" messages
4. Ensure button debouncing code is present
5. Try pressing and holding for 1 second

**Testing:**
Run `button_test.py` to verify button hardware:
```python
# Should see LED change color when buttons pressed
```

---

#### ❌ Button Presses Delayed or Missed
**Symptoms:** Have to press multiple times, laggy response

**Solutions:**
1. Check sleep loop interval (should be 0.1s checks)
2. Verify both button checks exist (main loop + sleep loop)
3. Ensure button state tracking variables work
4. Reduce UPDATE_INTERVAL if very sluggish

**Code Check:**
```python
# Should see this in code.py:
for _ in range(int(UPDATE_INTERVAL * 10)):
    time.sleep(0.1)  # Check every 0.1s
```

---

### Temperature Issues

#### ❌ Temperature Reading Too High
**Symptoms:** Shows 2-4°C higher than actual room temperature

**This is NORMAL!** The CLUE's processor generates heat.

**Solutions:**
1. **Calibrate** using `TEMP_OFFSET` in `code.py`:
   ```python
   TEMP_OFFSET = -3.5  # Adjust this value
   ```
2. Wait 10-15 minutes after power-on for stabilization
3. Compare with reference thermometer
4. See `CALIBRATION_GUIDE.md` for detailed steps

**Typical Offset Range:** -2.5°C to -4.0°C

---

#### ❌ Temperature Fluctuates Wildly
**Symptoms:** Reading jumps up/down by several degrees

**Solutions:**
1. Wait 15+ minutes for thermal stabilization
2. Ensure CLUE isn't in direct sunlight or near heat sources
3. Check if touching the board (hand heat affects reading)
4. Verify UPDATE_INTERVAL is not too short
5. Check for loose USB connection

---

#### ❌ Celsius/Fahrenheit Toggle Not Working
**Symptoms:** Button B doesn't switch units

**Solutions:**
1. Ensure you're in Main mode (not Trends/Stats/Food Safety)
2. Look for magenta LED flash on Button B press
3. Check serial console for "Temperature unit: X" message
4. Verify `use_fahrenheit` variable exists in code

---

### Humidity Issues

#### ❌ Humidity Reading Seems Wrong
**Symptoms:** Reading doesn't match reference hygrometer

**Solutions:**
1. Adjust `HUMIDITY_OFFSET` in `code.py`:
   ```python
   HUMIDITY_OFFSET = 5.2  # Adjust this value
   ```
2. Wait 20-30 minutes for humidity sensor to stabilize
3. Compare with calibrated hygrometer
4. Ensure sensor isn't obstructed

**Note:** CLUE humidity sensor accuracy is ±3-5% typically

---

### Food Safety Mode Issues

#### ❌ Can't Enter Food Safety Mode
**Symptoms:** Pressing Button A only cycles through 3 modes

**Solutions:**
1. Verify you have the latest code with 4 modes
2. Check code has `% 4` not `% 3` in button handling
3. Ensure `update_food_safety_display()` function exists
4. Look for "Display mode: Food Safety" in serial console
5. Re-copy latest `code.py` to device

**Verification:**
```bash
grep "% 4" /mnt/clue/code.py
# Should show two matches
```

---

#### ❌ Food Safety State Stuck on READY
**Symptoms:** Won't enter SAFE mode even when cold

**Solutions:**
1. Check actual temperature is below 4°C
2. Verify `FOOD_SAFE_TEMP = 4.0` in code
3. Ensure fridge is actually cold enough
4. Wait 2-3 minutes in fridge for state transition
5. Check serial console for state change messages

---

#### ❌ Food Safety LED Wrong Color
**Symptoms:** LED doesn't match expected state color

**Solutions:**
1. Verify state logic in `update_food_safety_display()`
2. Check LED brightness isn't too dim to see
3. Ensure color values are correct:
   - READY: (255, 255, 255) - White
   - SAFE: (0, 255, 0) - Green
   - CHECK: (255, 255, 0) - Yellow

---

### Memory / Performance Issues

#### ❌ Memory Allocation Errors
**Symptoms:** Error messages mentioning "memory allocation failed"

**Solutions:**
1. This is WHY food safety reuses main_group
2. Don't create new display objects in loops
3. Reduce HISTORY_SIZE if needed
4. Remove chr(176) degree symbols
5. Simplify string formatting

**Code Review:**
- ✅ Use simplified 3-state food safety (current code)
- ❌ Don't use standalone 5-state integrated (too much memory)

---

#### ❌ Device Crashes / Restarts
**Symptoms:** Random resets, blank screen, restarts

**Solutions:**
1. Check for syntax errors via serial console
2. Look for memory allocation failures
3. Reduce feature complexity
4. Check USB power supply (needs 500mA minimum)
5. Look for infinite loops or exceptions

**Debug:**
```python
# Add to main loop:
except Exception as e:
    print(f"ERROR: {e}")
    # Already in code
```

---

### Data / Trends Issues

#### ❌ Trends Show "Insufficient Data"
**Symptoms:** Can't see trend analysis

**This is NORMAL when first started!**

**Solutions:**
1. Wait at least 2 minutes after power-on
2. Trends require minimum 2 data samples
3. Full trends need 120 samples = 2 hours
4. Data is lost on power cycle (by design)

---

#### ❌ Statistics Look Wrong
**Symptoms:** Min/Max don't seem accurate

**Solutions:**
1. Remember stats reset on power cycle
2. Stats only cover data since last restart
3. Wait for full 2-hour collection period
4. Verify LOG_INTERVAL is set to 60 seconds
5. Check serial console for logged data points

---

### USB / Connection Issues

#### ❌ Can't Mount CLUE Drive
**Symptoms:** Device not showing up as CIRCUITPY

**Solutions:**
1. Try different USB port
2. Use USB 2.0 port (some USB 3.0 ports have issues)
3. Try different USB cable
4. Check if CLUE is in bootloader mode (should see CLUEBOOT)
5. Reinstall CircuitPython if needed

**Linux Specific:**
```bash
# Find device:
lsblk | grep sd

# Mount manually:
sudo mount /dev/sdX1 /mnt/clue
```

---

#### ❌ Device Keeps Remounting / Changing Drive Letter
**Symptoms:** /dev/sdf becomes /dev/sdg, etc.

**This is NORMAL on Linux!** CLUE resets when files are written.

**Solutions:**
1. Check device letter before each copy: `lsblk`
2. Use provided mount script
3. Always `sync` after copying files
4. Unmount before unplugging

---

#### ❌ Files Not Updating on Device
**Symptoms:** Copied code.py but changes don't appear

**Solutions:**
1. Run `sync` after copying
2. Check file timestamp: `ls -lh /mnt/clue/code.py`
3. Remount device after writing
4. Delete old file first, then copy new one
5. Hard reset CLUE after file changes

---

### Serial Console Issues

#### ❌ Can't Connect to Serial Console
**Symptoms:** screen/picocom shows "device busy" or timeout

**Solutions:**
1. Check device path: `ls /dev/ttyACM*`
2. Ensure no other program is using serial port
3. Add user to dialout group:
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and back in
   ```
4. Try different terminal program

**Working Commands:**
```bash
screen /dev/ttyACM0 115200
# or
picocom /dev/ttyACM0 -b 115200
# or
sudo cat /dev/ttyACM0
```

---

## 🔍 Diagnostic Tools

### Check Current Configuration
```bash
# View current settings:
grep "TEMP_OFFSET\|HUMIDITY_OFFSET" /mnt/clue/code.py
```

### Verify Button Code
```bash
# Should show 2 matches (both main and sleep loop):
grep "% 4" /mnt/clue/code.py
```

### Check File Version
```bash
# Check line count (should be ~582 after optimization):
wc -l /mnt/clue/code.py

# Check last modified:
ls -lh /mnt/clue/code.py
```

### Monitor Live Output
```bash
# See real-time sensor readings and debug messages:
screen /dev/ttyACM0 115200

# Exit screen: Ctrl-A then K
```

---

## 📋 Pre-Flight Checklist

Before asking for help, verify:

- [ ] CircuitPython 9.2.4+ installed
- [ ] Latest `code.py` copied to device
- [ ] File synced: `sync` command run
- [ ] Device has waited 5+ seconds after power-on
- [ ] Buttons physically click when pressed
- [ ] USB cable supports data (not charge-only)
- [ ] Serial console checked for error messages
- [ ] Device not in direct sunlight or near heat source

---

## 🆘 Getting Help

If issues persist after trying solutions above:

1. **Check Serial Output:**
   ```bash
   screen /dev/ttyACM0 115200
   ```
   Look for Python error messages or tracebacks

2. **Note Exact Error:**
   - What were you doing when it failed?
   - Any error messages shown?
   - What mode was active?

3. **Provide Details:**
   - CircuitPython version
   - Which mode showing issue
   - Steps to reproduce
   - Serial console output

4. **File an Issue:**
   - GitHub: https://github.com/jeremycohoe/clue-environmental-monitor/issues
   - Include all diagnostic info above

---

## 🔄 Factory Reset Procedure

If all else fails, completely reset:

1. **Backup your calibration values**
   ```bash
   grep "TEMP_OFFSET\|HUMIDITY_OFFSET" code.py > my_calibration.txt
   ```

2. **Erase and reinstall CircuitPython**
   - Download from circuitpython.org
   - Enter bootloader: double-click reset button
   - Copy UF2 file to CLUEBOOT drive

3. **Recopy code.py**
   ```bash
   sudo cp code.py /mnt/clue/
   sudo sync
   ```

4. **Restore calibration values** from backup

---

## 📊 Known Limitations

**By Design:**
- Temperature reads 2-4°C high (CPU heat) - use calibration
- History resets on power cycle (no persistent storage)
- Food safety simplified to 3 states (memory constraints)
- Trends require 2+ minutes of data collection
- Humidity accuracy ±3-5% typical for sensor

**Hardware:**
- CLUE has only 256KB RAM (limited memory)
- Buttons require firm press (hardware design)
- USB drive letter changes on Linux (device reset behavior)

---

**Still stuck? Check the GitHub issues page or file a new one!**
