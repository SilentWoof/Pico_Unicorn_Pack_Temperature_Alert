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
# gc.threshold(100000)

# **--------------------------------------------------**
# Set Variables
# **--------------------------------------------------**
# Loop Counters
core0_loop_n = 0
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


# Define Thread Running Confirmation
def thread_0_running_led():
    for x in range(0, 1):
            for y in range(0, 7):
                uni.set_pixel(x, y, 50, 50, 50)
    time.sleep(0.5)
    for x in range(0, 1):
            for y in range(0, 7):
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
t_hot = 30
t_cold = 18

temperatures = []

# **--------------------------------------------------**
# Define Buzzer and Mute Button
# **--------------------------------------------------**
# set up the Siren buzzer
buzzer = machine.Pin(28, machine.Pin.OUT)
buzzer.value(0)

# Add an interrupt button to mute the buzzer
buzzer_mute = False
mute_button = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN)

def mute_handler(pin):
    global buzzer_mute
    if not buzzer_mute:
        buzzer_mute = True
 
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
    print("Buzzer Mute Status:" + str(buzzer_mute))
    print("\n")
    print("Free Memory: " + str(gc.mem_free()) + " bytes of available heap RAM")
    print("Allocared Memory: " + str(gc.mem_alloc()) + " bytes of allocated heap RAM")
    print("*--------------------------*")
    print("\n")

# **--------------------------------------------------**
# Main Program On Core 0
# **--------------------------------------------------**
while True:
    mute_button.irq(trigger=machine.Pin.IRQ_RISING, handler=mute_handler)
    
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
        if buzzer_mute == True:
            buzzer.value(0)
            matrix_red()

        else:
            buzzer.value(1)
            matrix_red()

    else:
        if temperature > t_cold and temperature < t_hot:
            buzzer.value(0)
            buzzer_mute = False
            matrix_green()
        else:
            buzzer.value(0)
            buzzer_mute = False
            matrix_blue()
    
    status_print()

    # set the delay in seconds between temperature checks
    for delay in range(1):
        thread_0_running_led()
