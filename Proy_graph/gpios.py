########################## RPi.GPIO module basics ##########################

### Documentación 
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
###
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/install/
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

### specify Raspberry Pi Pin numbering
GPIO.setmode(GPIO.BOARD)            # BOARD numbering system
    # or
#GPIO.setmode(GPIO.BCM)         # BCM numbering system
# detecting numbering system
mode = GPIO.getmode()
print("The GPIO Pin mode is " + str(mode))
print("To see details of the pinout use the command <pinout> in the terminar")

### Setup up a channel
if mode == 10:
    channel1 = 3
    channel2 = 5
elif mode == 11:
    channel1 = 2
    channel2 = 3
# To configure a channel as an input output:
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

GPIO.setup(channel1, GPIO.IN)        # input
GPIO.setup(channel2, GPIO.OUT)       # output


#Setup a multichannel 
chan_list = [11,12]    # add as many channels as you want!
# ~ GPIO.setup(chan_list, GPIO.OUT)
# ~ GPIO.setup(chan_list, GPIO.IN)

# Read the value of a GPIO pin:
#GPIO.input(channel)

# Output Value of a GPIO pin:
state = True                        # State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.output(channel2, state)

# Output a multichannel 
# ~ chan_list = [11,12]                             # also works with tuples
# ~ GPIO.output(chan_list, GPIO.LOW)                # sets all to GPIO.LOW
# ~ GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
for i in range(10):
    print(GPIO.input(channel1))
    time.sleep(2)
    if state == True:
        state= False
        GPIO.output(channel2,state)
    else:
        state = True
        GPIO.output(channel2,state)
    
#### To clean up at the end of your script:
GPIO.cleanup() # Only clean up GPIO channels that your script has used. Note that GPIO.cleanup() 
                # also clears the pin numbering system in use.


    
# Possible to clean up  individual channels, a list or a tuple of channels:
# ~ GPIO.cleanup(channel)
# ~ GPIO.cleanup( (channel1, channel2) )
# ~ GPIO.cleanup( [channel1, channel2] )

# to see more interacción with the gpios you can see the input documentation:
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
