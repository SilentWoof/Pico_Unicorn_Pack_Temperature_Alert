import machine
from machine import Pin, PWM
import time
import picounicorn as uni
import _thread
import gc

# **--------------------------------------------------**
# Configure Garbage Collection
# **--------------------------------------------------**
# Enable automatic garbage collection in Out Of Memory condition
gc.enable()

# Trigger carbage collection after 100000 bytes
# of heap memory have been allocated
gc.threshold(100000)

# **--------------------------------------------------**
# Set Variables
# **--------------------------------------------------**
# Loop Counters
core0_loop_n = 0
global core1_loop_n
core1_loop_n = 0
alert_loop_n = 0

# **--------------------------------------------------**
# Configure Unicorn Matrix Alerts
# **--------------------------------------------------**
uni.init()

# set the width and height for the led matrix
uni_width = uni.get_width()
uni_height = uni.get_height()

# define led matrix colors for temperature states
def matrix_red():
    for x in range(1, 16):
            for y in range(uni_height):
                uni.set_pixel(x, y, 255, 0, 0)

def matrix_green():
    for x in range(1, 16):
            for y in range(uni_height):
                uni.set_pixel(x, y, 0, 50, 0)

def matrix_blue():
    for x in range(1, 16):
            for y in range(uni_height):
                uni.set_pixel(x, y, 0, 0, 50)

def matrix_black():
    for x in range(1, 16):
            for y in range(uni_height):
                uni.set_pixel(x, y, 0, 0, 0)

# Define Thread Running Confirmation
def thread_0_running_led():
    for x in range(0, 1):
            for y in range(0, 2):
                uni.set_pixel(x, y, 50, 50, 50)
    time.sleep(0.5)
    for x in range(0, 1):
            for y in range(0, 2):
                uni.set_pixel(x, y, 0, 0, 0)
    time.sleep(0.5)
        
def thread_1_running_led():
    for x in range(0, 1):
            for y in range(5, 7):
                uni.set_pixel(x, y, 50, 50, 50)
    time.sleep(0.5)
    for x in range(0, 1):
            for y in range(5, 7):
                uni.set_pixel(x, y, 0, 0, 0)
    time.sleep(0.5)

# Define taking temperature notification
def taking_temp_note():
    for x in range(0, 1):
            for y in range(2, 5):
                uni.set_pixel(x, y, 255, 0, 255)
    time.sleep(0.2)
    for x in range(0, 1):
            for y in range(2, 5):
                uni.set_pixel(x, y, 0, 0, 0)
    time.sleep(0.2)

# **--------------------------------------------------**
# Configure Pico's Onboard temperature sensor
# **--------------------------------------------------**
# reads from Pico's temp sensor and converts it into a more manageable number
sensor_temp = machine.ADC(4) 
conversion_factor = 3.3 / (65535)

# add a variable to manually adjust the accuracy of the sensor
t_adjust = 3.1  

# variables to set the upper and lower temperature limits
t_hot = 23
t_cold = 18

temperatures = []

# **--------------------------------------------------**
# Define Buzzer and Mute Button
# **--------------------------------------------------**
# set up the piezzo buzzer
buzzer = PWM(Pin(0))
buzzer.freq(500)

# Add a button to mute the buzzer
button = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)

global buzzer_mute
buzzer_mute = False

# **--------------------------------------------------**
# Define Console Print Info for Debugging
# **--------------------------------------------------**
def status_print():
    print("*--------------------------*")
    print("Core 0 Loop #" + str(core0_loop_n))
    print("Core 1 Loop #" + str(core1_loop_n))
    print("*--------------------------*")
    print("Sensor reading: " + str(reading))
    print("Temperature: " + str(temperature))
    print("Decimal temperature: " + str(temp_float))
    print("\n")
    print("Alert Count: " + str(alert_loop_n) + " Loops In Total")
    print("Temp Alert Status: " + str(temp_alert))
    print("Buzzer Mute Status:" + str(buzzer_mute))
    print("\n")
    print("Free Memory: " + str(gc.mem_free()) + " bytes of available heap RAM")
    print("Allocared Memory: " + str(gc.mem_alloc()) + " bytes of allocated heap RAM")
    print("*--------------------------*")
    print("\n")

# **--------------------------------------------------**
# Define Alert Thread on Core 1
# **--------------------------------------------------**
global temp_alert
temp_alert = False

# Define a function for the alert thread on core 1
def alert_thread():
    global temp_alert
    global buzzer_mute
    global core1_loop_n
    while True:
        # Start counting the loops
        core1_loop_n += 1

        # Watch for mute button press
        if button.value() == 1:
            time.sleep(0.01)
            buzzer_mute = True

        # Visual and Audiable alert for over temperature
        if temp_alert == True and buzzer_mute == False:
            matrix_red()
            buzzer.duty_u16(1000)
            time.sleep(0.2)
            matrix_black()
            buzzer.duty_u16(0)
            time.sleep(0.2)
        
        # Visual Only Alert (Buzzer Mute is Active)
        elif temp_alert == True and buzzer_mute == True:
            matrix_red()
            time.sleep(0.2)
            matrix_black()
            time.sleep(0.2)

        else:
            # Toggle LED to Show Thread is running
            thread_1_running_led()

_thread.start_new_thread(alert_thread, ())

# **--------------------------------------------------**
# Main Program On Core 0
# **--------------------------------------------------**
while True:
    # start counting the loops
    core0_loop_n += 1

    # taking teperature notification
    taking_temp_note()

    # the following two lines convert the value from the temp sensor into celsius
    reading = (sensor_temp.read_u16() * conversion_factor)
    temp_float = round((27 - (reading - 0.706) / 0.001721) + t_adjust, 1)
    temperature = int(temp_float)
    
    # set the temperature alert
    if temperature >= t_hot:
        temp_alert = True
        alert_loop_n += 1

    else:
        if temperature > t_cold and temperature < t_hot:
            temp_alert = False
            buzzer_mute = False
            matrix_green()
        else:
            temp_alert = False
            buzzer_mute = False
            matrix_blue()
    
    status_print()

    # set the delay in seconds between temperature checks
    for delay in range(30):
        thread_0_running_led()
