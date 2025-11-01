# Leftover Food Safety Device Application

## Overview

This document outlines how to use the Adafruit CLUE as a **Leftover Food Safety Device** for monitoring refrigerated food storage and ensuring safe consumption practices.

## Concept

**Microprocessor with Temperature and Humidity sensors, a screen for feedback, and Bluetooth for wireless communication.**

The CLUE monitors temperature in refrigerators to track food safety and alert users when leftovers should be discarded based on FDA recommendations.

## Operating States

### Initial State
- **Sensor is at room temperature* and fully charged**
- Sensor is affixed to food container and placed into a fridge
- When the sensor reaches **4° C (food safe)**, start logging data and display a **Safe** message, with Date and Time, in **GREEN**

### Safety Zones

#### GREEN Zone - Food Safe
- **Display:** GREEN screen
- **Condition:** Temperature is below 4° C
- **Action:** Food is safe to consume
- **Display Info:** "SAFE" message with timestamp

#### YELLOW Zone - Warning
- **Display:** YELLOW screen
- **Condition:** Temperature is Above 4° C but below room temperature for **Less than 2 hours**
- **Action:** Warning - monitor closely
- **Display Info:** Show the temperature and how long it stayed above 4° C before temperature dropped below 4° again and returned to GREEN
- **Duration Tracking:** If this exceeds Two (2) hours, escalate to RED zone

#### RED Zone - Discard Food
- **Display:** RED screen
- **Condition 1:** Temperature is Above 4° C but below room temperature for **More than 2 hours**
- **Condition 2:** Temperature is Below 4° C but below room temperature for **More than 4 days**
- **Action:** Recommend disposing of food on the display

### Reset Condition
When temperature reaches room temperature, reset sensors and display a **"Charge Me"** message on screen to be reused

## Implementation Requirements

### Core Features
1. **Temperature Monitoring**
   - Continuous temperature logging
   - Track time spent in each temperature zone
   - 4°C threshold detection
   - Room temperature detection (21°C defined as room temperature)

2. **Time Tracking**
   - Log when food entered refrigerator (below 4°C)
   - Track duration above 4°C (danger zone timer)
   - Track total days in refrigerator

3. **Visual Feedback**
   - GREEN background: Food safe
   - YELLOW background: Warning state
   - RED background: Discard food
   - Display relevant temperature, time, and safety information

4. **Data Logging**
   - Record temperature events
   - Log zone transitions
   - Track safety violations

### Bluetooth Features (Future)
- Name each sensor for multiple monitoring
- Read sensor status from outside the fridge
- Display list of sensors with duration and safety status
- Color-coded status for multiple sensors

### Future Enhancements
- Selection of type of food to customize food safe timelines
- Different food types have different safe storage durations
- Note: FDA recommends leftovers not be stored more than 3-4 days in general

## FDA Food Safety Guidelines

### Key Rules
- **Refrigerator Temperature:** Must be at or below 4°C (40°F)
- **Danger Zone:** 4°C - 21°C (room temperature)
- **2-Hour Rule:** Food left at room temperature for more than 2 hours should be discarded
- **Storage Duration:** Leftovers should not be stored more than 3-4 days

### Temperature Thresholds
- **Room Temperature:** 21°C (defined)
- **Food Safe Temperature:** 4°C or below
- **Danger Zone:** Above 4°C

## Hardware Considerations

### CLUE Advantages for This Application
1. **Accurate Temperature Sensor (SHT31-D)**
   - Range: -40°C to +125°C
   - Accuracy: ±0.3°C (typical)
   - Calibrated in this project to exact reference

2. **Color Display**
   - 1.3" 240×240 IPS screen
   - Perfect for color-coded safety zones
   - Visible in refrigerator light

3. **Bluetooth Connectivity**
   - nRF52840 with BLE 5.0
   - Can monitor from outside fridge
   - Support multiple sensors

4. **Battery Operation**
   - Built-in LiPo charger
   - Low power mode available
   - Can run for days on single charge

5. **Real-Time Clock**
   - Track exact timestamps
   - Calculate duration in each zone

6. **Data Storage**
   - 2MB filesystem for logging
   - Can store weeks of temperature data

## Implementation Strategy

### Phase 1: Basic Food Safety Monitor
- Implement temperature monitoring with 4°C threshold
- Add color-coded display (GREEN/YELLOW/RED)
- Track time in danger zone
- Display current status and time elapsed

### Phase 2: Enhanced Time Tracking
- Add real-time clock integration
- Track exact timestamps of zone transitions
- Calculate total refrigeration days
- Implement 4-day maximum storage alert

### Phase 3: Bluetooth Integration
- Add BLE advertisement with status
- Implement sensor naming
- Create mobile app or web interface
- Support multiple sensor monitoring

### Phase 4: Food Type Customization
- Add food type selection menu
- Customize safe storage durations
- Different thresholds for different foods
- FDA guidelines database

## Code Modifications Needed

### From Current Environmental Monitor
The existing `code.py` already has:
- ✅ Calibrated temperature sensor (-3.5°C offset)
- ✅ Color display capabilities
- ✅ Button inputs for user interaction
- ✅ Data tracking and statistics

### New Features to Add
- ⚠️ Time tracking with RTC or elapsed time
- ⚠️ Temperature zone state machine
- ⚠️ Background color change based on safety zone
- ⚠️ Timer displays for danger zone duration
- ⚠️ 4-day refrigeration counter
- ⚠️ Reset/charge mode
- ⚠️ BLE advertising (future)

## Display Mockups

### GREEN Zone Display
```
╔════════════════════════════╗
║  FOOD SAFETY MONITOR       ║  (GREEN BACKGROUND)
║                            ║
║         SAFE ✓             ║
║                            ║
║    Temperature: 3.2°C      ║
║                            ║
║    In Fridge: 2 days       ║
║    Since: Nov 1, 09:30     ║
║                            ║
║  [Days Left: 1-2 days]     ║
╚════════════════════════════╝
```

### YELLOW Zone Display
```
╔════════════════════════════╗
║  FOOD SAFETY MONITOR       ║  (YELLOW BACKGROUND)
║                            ║
║       WARNING ⚠            ║
║                            ║
║    Temperature: 8.5°C      ║
║                            ║
║  Above 4°C for: 45 min     ║
║  Limit: 2 hours            ║
║                            ║
║  [Return to fridge NOW]    ║
╚════════════════════════════╝
```

### RED Zone Display
```
╔════════════════════════════╗
║  FOOD SAFETY MONITOR       ║  (RED BACKGROUND)
║                            ║
║      DISCARD FOOD ✗        ║
║                            ║
║    Temperature: 12.1°C     ║
║                            ║
║  Above 4°C for: 2h 15min   ║
║                            ║
║  [NOT SAFE TO EAT]         ║
║  [DISPOSE OF FOOD]         ║
╚════════════════════════════╝
```

### Charge Me Display
```
╔════════════════════════════╗
║  FOOD SAFETY MONITOR       ║  (BLUE BACKGROUND)
║                            ║
║       CHARGE ME            ║
║                            ║
║    Temperature: 21.0°C     ║
║    (Room Temperature)      ║
║                            ║
║  Ready to reset and        ║
║  monitor new food item     ║
║                            ║
║  [Connect USB to charge]   ║
╚════════════════════════════╝
```

## Reference Settings

- **Room Temperature Definition:** 21°C
- **Food Safe Threshold:** 4°C
- **Danger Zone Timer:** 2 hours
- **Maximum Refrigeration:** 4 days
- **Reset Temperature:** Room temperature (21°C)

## Next Steps

Would you like me to:
1. **Implement Phase 1** - Create a basic food safety monitor version of the code?
2. **Keep current environmental monitor** - Add this as an alternate application mode?
3. **Create separate food_safety.py** - Dedicated program for food safety monitoring?

The current environmental monitor can be extended to include food safety features, or we can create a dedicated food safety version while keeping the general environmental monitor as-is.
