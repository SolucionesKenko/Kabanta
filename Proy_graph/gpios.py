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



    
class ScriptState(Enum):
    TESTING = auto()
    NOTTESTING = auto()

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

class GPIOS():
    def __init__(self):
        self.boardPinout = [3,5,7,11,13,15]
        self.BMCPinout = [2,3,4,17,17,22]
        self.scriptState = ScriptState.NOTTESTING
        
        ### specify Raspberry Pi Pin numbering
        GPIO.setmode(GPIO.BOARD)            # BOARD numbering system
        #GPIO.setmode(GPIO.BCM)             # BCM numbering system
    
    def __del__(self):
        self.clearGPIOS()

    def clearGPIOS(self):
        #### To clean up at the end of your script:
        # Only clean up GPIO channels that your script has used. Note that GPIO.cleanup() 
        # also clears the pin numbering system in use.
        GPIO.cleanup()

    def init_Gpios(self):
        self.pinoutMode = GPIO.getmode()
        ### Setup up GPIO pin
        if self.pinoutMode == PinoutMode.BOARD:
            self.pinout = self.boardPinout
        elif self.pinoutMode == PinoutMode.BMC:
            self.pinout = self.BMCPinout
        else:
            print("Error setting Raspberry GPIO mode")
        
        # Configure GPIO pins
        # To configure a channel as an input output:
        ## https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
        GPIO.setup(self.pinout[Gpios.LED], GPIO.OUT)        # input
        GPIO.setup(self.pinout[Gpios.SHOCK1:], GPIO.IN)       # output

        # Default LED State
        GPIO.output(self.pinout[Gpios.LED], LEDstate.OFF)
        self.setEventDetects()

    def setEventDetects(self):
        GPIO.add_event_detect(self.pinout[Gpios.SHOCK1:],GPIO.RISING,bouncetime=200)
        if __name__ == "__main__":
            GPIO.add_event_callback(self.pinout[Gpios.SHOCK1], self.onShockButttonPressed())
            GPIO.add_event_callback(self.pinout[Gpios.SHOCK2], self.onShockButttonPressed())
            GPIO.add_event_callback(self.pinout[Gpios.CHARGE], self.onChargeButtonPressed())
            GPIO.add_event_callback(self.pinout[Gpios.UPENERGY], self.onDownEnergyButtonPressed())
    
    if __name__ == "__main__":
        def onDownEnergyButtonPressed(self):
            print(self.texto +" onDownEnergyButtonPressed")
        def onUpEnergyButtonPressed(self):
            print(self.texto +" onUpEnergyButtonChanged")
        def onShockButttonPressed(self):
            print(self.texto +" onShockButttonPressed")
        def onChargeButtonPressed(self):
            print(self.texto +" onChargeButtonPressed")
        def LEDOn(self):
            print(self.texto +" LEDOn")
        def LEDOff(self):
            print(self.texto +" LEDOff")
        def LEDToggle(self):
            print(self.texto +" LEDToggle")
        def onShockButttonPressed(self):
            print(self.texto +" onUpEnergyButtonPressed")
            if (GPIO.input(self.pinout[Gpios.SHOCK1]) == 1) and (GPIO.input(self.pinout[Gpios.SHOCK2]) == 1):
                self.onShockButttonPressed()

    def detectPinoutMode(self):    # detecting numbering system
        self.pinoutMode = GPIO.getmode()
        print("BOARD numbering system = 10")
        print("BMC numbering system = 11")
        print("The GPIO Pin mode is " + str(self.pinoutMode))
        print("To see details of the pinout use the command <pinout> in the terminar")

if __name__ == "__main__":
    scriptState = ScriptState.TESTING
    test = GPIOS()
    test.scriptState = scriptState
    while True:
        time.sleep(1)






# to see more interacción with the gpios you can see the input documentation:
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
