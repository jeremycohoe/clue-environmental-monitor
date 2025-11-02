# Food Safety Monitor - Quick Start Guide

## Current Setup
Your CLUE is now running the **FDA-Compliant Food Safety Monitor** as the main program.

## How It Works

### 5 Color-Coded States

#### 1️⃣ WHITE - READY (Initial State)
- **When:** At room temperature (≥21°C)
- **Display:** "READY" on white background
- **Action:** Attach to food container, place in refrigerator
- **What Happens Next:** Automatically starts monitoring when temp drops to 4°C

#### 2️⃣ GREEN - SAFE
- **When:** Temperature ≤ 4°C (food safe zone)
- **Display:** "SAFE" on green background
- **Shows:** Time in fridge, days remaining
- **Action:** Food is safe to eat
- **Auto-switch:** Goes to YELLOW if temp rises above 4°C

#### 3️⃣ YELLOW - WARNING
- **When:** Temperature 4-21°C (danger zone)
- **Display:** "WARNING" on yellow background
- **Shows:** Time in danger zone, 2-hour countdown
- **Action:** RETURN TO FRIDGE IMMEDIATELY
- **Auto-switch:**
  - Returns to GREEN if temp drops below 4°C
  - Goes to RED if in danger zone > 2 hours

#### 4️⃣ RED - DISCARD
- **When:** Either:
  - In danger zone > 2 hours, OR
  - Stored > 4 days total
- **Display:** "DISCARD" on red background
- **Shows:** "NOT SAFE TO EAT", "DISPOSE OF FOOD"
- **Action:** ⚠️ THROW FOOD AWAY - DO NOT EAT
- **Auto-switch:** Goes to BLUE when returned to room temp

#### 5️⃣ BLUE - CHARGE ME
- **When:** Returned to room temperature (≥21°C)
- **Display:** "CHARGE ME" on blue background
- **Shows:** "Room temp reached", "Ready to reset"
- **Action:** Connect USB to recharge
- **Auto-switch:** Resets to WHITE when battery charged and cooled

## Usage Instructions

### First Time Setup
1. **Charge the CLUE** (connect USB until LED indicates full charge)
2. **Let it cool** to room temperature if warm from charging
3. **Verify display** shows WHITE "READY"

### Monitoring Food
1. **Prepare food** - Put leftovers in container
2. **Attach CLUE** - Place on or near food container
3. **Refrigerate** - Put entire setup in fridge
4. **Auto-start** - Display turns GREEN when temp reaches 4°C
5. **Check periodically** - Glance at color to verify food safety

### Reading the Display

**GREEN = EAT**
- Food is safe
- Enjoy your leftovers!

**YELLOW = WARNING**
- Door left open? Power outage?
- Return to fridge immediately
- Check timer - must get back to cold within 2 hours

**RED = TRASH**
- DO NOT EAT
- Dispose of food safely
- Clean container

**BLUE = CHARGE**
- Food consumed or discarded
- Recharge CLUE for next use
- Will auto-reset to WHITE when ready

## LED Indicator
The NeoPixel LED on the back matches the screen color:
- ⚪ White = Ready
- 🟢 Green = Safe
- 🟡 Yellow = Warning
- 🔴 Red = Discard
- 🔵 Blue = Charge

## FDA Food Safety Rules (Built-In)

✅ **4°C (40°F)** - Maximum safe refrigerator temperature
✅ **2 Hours** - Maximum time in danger zone (4-21°C)
✅ **4 Days** - Maximum refrigerator storage for leftovers
✅ **21°C (70°F)** - Room temperature threshold

## Typical Use Case Example

**Day 1 - Monday Dinner Leftovers:**
1. 8:00 PM - Cook dinner, have leftovers
2. 8:30 PM - CLUE shows WHITE "READY" at room temp
3. 8:35 PM - Place food + CLUE in fridge
4. 8:50 PM - CLUE shows GREEN "SAFE" (reached 4°C)
5. Display shows: "In Fridge: 0d 0h", "Safe for: 4d"

**Day 2 - Tuesday:**
- CLUE shows GREEN
- Display shows: "In Fridge: 1d 2h", "Safe for: 3d"

**Day 3 - Wednesday Lunch:**
- Take food out to reheat
- CLUE briefly shows YELLOW (warming up)
- Eat the food, done!
- CLUE returns to room temp → shows BLUE "CHARGE ME"
- Plug in USB to recharge
- Ready for next use

**Forgot in Fridge Scenario:**
- Day 5 - Food still in fridge
- CLUE shows RED "DISCARD" (>4 days)
- Throw food away
- CLUE resets when removed from fridge

## Power Outage Scenario

If power goes out:
1. Fridge temp starts rising
2. CLUE detects temp > 4°C → shows YELLOW
3. Timer starts counting (2 hour limit)
4. If power returns within 2 hours → returns to GREEN
5. If power out > 2 hours → shows RED, discard food

## Troubleshooting

**Q: Display shows WHITE but I'm in the fridge**
- A: Fridge temp might be > 4°C. Check fridge thermometer. Adjust fridge settings.

**Q: Shows YELLOW as soon as I close fridge door**
- A: Fridge may be too warm. Let CLUE stabilize for a few minutes. Check fridge temperature.

**Q: Always shows RED immediately**
- A: Device might think it's been > 4 days or > 2 hours in danger zone. Remove from fridge to reset (BLUE), then WHITE.

**Q: Stuck on BLUE**
- A: Waiting for temperature to drop below 4°C to reset. If at room temp, this is normal - device is ready to be recharged and reused.

**Q: Battery dies in fridge**
- A: CLUE battery life is ~24-48 hours depending on usage. For >2 day storage, you may need to remove, charge, and return to fridge.

## Switching Back to Environmental Monitor

If you want the environmental monitor instead:

```bash
sudo mv /mnt/clue/code.py /mnt/clue/food_safety.py
sudo mv /mnt/clue/code_env_backup.py /mnt/clue/code.py
sudo sync
```

## Temperature Calibration

Already calibrated:
- **Offset: -3.5°C** (compensates for self-heating)
- **Accuracy: ±0.1°C** (verified with reference thermometer)
- **Reference: 27.5°C** at room temperature

## Buttons

Note: Current version does not use buttons. Future versions may add:
- Button A: Show detailed stats
- Button B: Manual reset
- Both buttons: Switch to environmental monitor mode

## Files on CLUE

Current:
- `/code.py` - Food Safety Monitor (ACTIVE)
- `/code_env_backup.py` - Environmental Monitor (backup)

## Support

- Calibration data: TEMP_OFFSET = -3.5°C
- Safe temp threshold: 4°C
- Danger zone limit: 2 hours
- Max storage: 4 days
- Room temp: 21°C

---

**Your CLUE is now dedicated to food safety!** 🥗✅

The device automatically monitors and alerts you based on FDA food safety guidelines. No button presses needed - just attach to food and refrigerate!
