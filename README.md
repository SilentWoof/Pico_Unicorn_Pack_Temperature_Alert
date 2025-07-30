# 🌡️ Pico Unicorn Pack Temperature Alert

A fun and functional Raspberry Pi Pico project using the Pimoroni Unicorn Pack to monitor temperature and provide visual and audible alerts when thresholds are crossed. Comes with threaded alerts, GC optimization, buzzer mute button, and colorful LED notifications.

## 🚀 Features

- Uses Pico’s onboard temperature sensor
- Visual alerts via Unicorn Pack LED matrix
- Audible alerts using piezo buzzer
- Mute button to disable sound
- Multithreaded alert system using `_thread`
- Manual temperature offset calibration
- Garbage Collection tuning for reliability

## 🛠️ Hardware Required

- Raspberry Pi Pico
- Pimoroni Unicorn Pack
- Piezo buzzer (connected to GPIO 0)
- Push button (connected to GPIO 28)

## 🔧 Setup Instructions

1. Clone this repo to your Pico device
2. Ensure required libraries (`picounicorn`) are available
3. Connect buzzer and mute button to correct GPIO pins
4. Flash the `.py` file and reset Pico

## 🌈 LED Alert Colors

| Color        | Meaning           |
|-------------|-------------------|
| 🔴 Red       | Temperature too hot |
| 🟢 Green     | Temperature normal |
| 🔵 Blue      | Temperature too cold |
| ⚫ Black     | Matrix cleared / standby |

## 📢 Usage Notes

- Upper temp limit: `23°C`
- Lower temp limit: `18°C`
- `t_adjust = 3.1` — tweak this for sensor accuracy
- Alerts blink and beep when hot unless muted

## 🧠 Threads

- **Core 0**: Reads temperature, updates status
- **Core 1**: Handles buzzer alerts and mute button logic

## 🧼 Memory Management

Garbage collection auto-enabled:
```python
gc.enable()
gc.threshold(100000)
```
Ensures reliability during long runtimes.

## 🧵 Thread Visual Indicators

- **Core 0** shows blinking LED in matrix corner  
- **Core 1** blinks alternate corner to indicate activity

---

Made by [SilentWoof](https://github.com/SilentWoof)  
For more info, check out the original code file [here](https://github.com/SilentWoof/Pico_Unicorn_Pack_Temperature_Alert).

