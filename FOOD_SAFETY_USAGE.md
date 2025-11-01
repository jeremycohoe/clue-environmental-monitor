# Food Safety Monitor - Quick Reference

## Two Ways to Use

### Option 1: Standalone Food Safety Monitor
Rename `food_safety.py` to `code.py` on your CLUE for dedicated food safety monitoring.

```bash
# On CLUE filesystem
mv code.py code_env.py  # Save environmental monitor
mv food_safety.py code.py  # Activate food safety monitor
```

### Option 2: Environmental Monitor with Food Safety Mode
Use the integrated `code.py` which includes food safety as Mode 3.

Press **Button A** three times to access Food Safety mode from the main environmental monitor.

## Food Safety States

### WHITE - READY (Initial State)
- Device at room temperature
- Ready to be placed in fridge
- Monitoring will begin when temperature drops to 4°C

### GREEN - SAFE
- Temperature below 4°C
- Food is safe to consume
- Shows time in fridge
- Shows days remaining (max 4 days)

### YELLOW - WARNING
- Temperature above 4°C but below room temp
- Counts time in danger zone
- Limit: 2 hours
- Action: Return food to fridge immediately

### RED - DISCARD
- Exceeded 2 hours in danger zone, OR
- Stored for more than 4 days
- Food is NOT safe to eat
- Must be disposed of

### BLUE - CHARGE ME
- Temperature returned to room temperature
- Device ready to be recharged and reset
- Will reset when returned to fridge (below 4°C)

## Button Controls (in Environmental Monitor)

- **Button A**: Cycle modes (Main → Trends → Stats → Food Safety → Main)
- **Button B**: Toggle Celsius/Fahrenheit (works in all modes except Food Safety)

## FDA Guidelines

- **Food Safe Temperature**: ≤ 4°C (40°F)
- **Room Temperature**: 21°C (70°F)
- **Danger Zone**: 4°C - 21°C
- **2-Hour Rule**: Food in danger zone > 2 hours must be discarded
- **Storage Limit**: Leftovers should not be stored > 3-4 days

## NeoPixel LED Indicators

- **WHITE**: Ready/Initial state
- **GREEN**: Food safe
- **YELLOW**: Warning - danger zone
- **RED**: Discard food
- **BLUE**: Charge/Reset mode

## Typical Use Case

1. **Prepare**: Charge CLUE, ensure it's at room temperature (WHITE display)
2. **Attach**: Affix to food container
3. **Refrigerate**: Place in fridge
4. **Monitor**: Display turns GREEN when temp reaches 4°C, monitoring begins
5. **Check**: Days remaining shown on display
6. **Alert**: If temperature rises (door open, power loss), YELLOW warning appears
7. **Decide**: If in danger zone > 2 hours or > 4 days stored, RED discard alert
8. **Consume**: While in GREEN zone
9. **Reset**: When food consumed, remove from fridge, returns to room temp (BLUE), then ready for next use (WHITE)

## Advanced Features (Future)

- Bluetooth naming and status reporting
- Multiple sensor monitoring via BLE
- Food type customization
- Mobile app integration
- Data logging and history

## Switching Between Modes

### Use Standalone Food Safety Monitor:
```bash
# On CLUE (mounted at /mnt/clue)
sudo mv /mnt/clue/code.py /mnt/clue/code_env.py
sudo mv /mnt/clue/food_safety.py /mnt/clue/code.py
sudo sync
```

### Return to Environmental Monitor:
```bash
# On CLUE (mounted at /mnt/clue)
sudo mv /mnt/clue/code.py /mnt/clue/food_safety.py
sudo mv /mnt/clue/code_env.py /mnt/clue/code.py
sudo sync
```

Or just use the integrated version and press Button A to switch modes!
