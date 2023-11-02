########################## RPi.GPIO module basics ##########################

### Documentación 
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
###
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/install/
import time
from enum import Enum, auto, IntEnum
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError or RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges or you'r not on a Raspberry device.  You can achieve superuser privileges by using 'sudo' to run your script; ")

class Gpios(IntEnum):   #   Estado para simular
    LED = 1                    #   Listo
    SHOCK1 = 2            #   Listo
    SHOCK2 = 3      #   Pendiente
    CHARGE = 4      #   Listo
    UPENERGY = 5        #   Listo
    DOWNENERGY = 6    #   Listo

class PinoutMode(IntEnum):
    BOARD = 10
    BMC = 11

class LEDstate(IntEnum):
    ON = 1
    OFF = 0

boardPinout = [3,5,7,11,13,15]
BMCPinout = [2,3,4,17,17,22]

def init_Gpios():
    ### specify Raspberry Pi Pin numbering
    GPIO.setmode(GPIO.BOARD)            # BOARD numbering system
    #GPIO.setmode(GPIO.BCM)             # BCM numbering system
    pinoutMode = GPIO.getmode()
    ### Setup up GPIO pin
    if pinoutMode == PinoutMode.BOARD:
        pinout = boardPinout
    elif pinoutMode == PinoutMode.BMC:
        pinout = BMCPinout
    else:
        print("Error setting Raspberry GPIO mode")
    
    # Configure GPIO pins
    # To configure a channel as an input output:
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    GPIO.setup(pinout[Gpios.LED], GPIO.OUT)        # input
    GPIO.setup(pinout[Gpios.SHOCK1:], GPIO.IN)       # output

    # Default LED State
    GPIO.output(pinout[Gpios.LED], LEDstate.OFF)

def clearGPIOS():
    #### To clean up at the end of your script:
    # Only clean up GPIO channels that your script has used. Note that GPIO.cleanup() 
    # also clears the pin numbering system in use.
    GPIO.cleanup()
    
def detectPinoutMode():    # detecting numbering system
    pinoutMode = GPIO.getmode()
    print("BOARD numbering system = 10")
    print("BMC numbering system = 11")
    print("The GPIO Pin mode is " + str(pinoutMode))
    print("To see details of the pinout use the command <pinout> in the terminar")


# to see more interacción with the gpios you can see the input documentation:
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
