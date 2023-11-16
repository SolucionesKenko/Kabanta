########################## RPi.GPIO module basics ##########################

### Documentación 
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
###
    ## https://sourceforge.net/p/raspberry-gpio-python/wiki/install/
import time
from PyQt5 import QtCore
from enum import Enum, auto, IntEnum
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError or RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges or you'r not on a Raspberry device.  You can achieve superuser privileges by using 'sudo' to run your script; ")



    
class ScriptState(Enum):
    TESTING = auto()
    NOTTESTING = auto()

class Gpios(IntEnum):   #   Estado para simular
    LED = 0                    #   Listo
    SHOCK1 = 1            #   Listo
    SHOCK2 = 2      #   Pendiente
    CHARGE = 3      #   Listo
    UPENERGY = 4        #   Listo
    DOWNENERGY = 5    #   Listo

class PinoutMode(IntEnum):
    BOARD = 10
    BMC = 11

class LEDstate(IntEnum):
    ON = 1
    OFF = 0
class GPIOHandler(QtCore.QObject):
    sig = QtCore.pyqtSignal()
    def __ini__(self):
        super().__init__()
    def button_pressed_callback(self):
        self.sig.emit()

class GPIOS():
    def __init__(self):
        self.boardPinout = [3,5,7,11,13,15]
        self.BMCPinout = [2,3,4,17,27,22]
        self.scriptState = ScriptState.NOTTESTING
        self.texto = "Hola"
        self.DownEnergy = GPIOHandler()
        self.UpEnergy = GPIOHandler()
        self.Shock = GPIOHandler()
        self.Charge = GPIOHandler()
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
        print("Your have enterd the setEventDetects")
        GPIO.add_event_detect(self.pinout[Gpios.SHOCK1], GPIO.RISING, callback =self.onShockButttonPressed1, bouncetime=200)
        GPIO.add_event_detect(self.pinout[Gpios.SHOCK2], GPIO.RISING, callback =self.onShockButttonPressed2, bouncetime=200)
        GPIO.add_event_detect(self.pinout[Gpios.CHARGE], GPIO.RISING, callback = self.onChargeButtonPressed, bouncetime=200)
        GPIO.add_event_detect(self.pinout[Gpios.UPENERGY], GPIO.RISING, callback = self.onUpEnergyButtonPressed, bouncetime=200)
        GPIO.add_event_detect(self.pinout[Gpios.DOWNENERGY], GPIO.RISING, callback = self.onDownEnergyButtonPressed, bouncetime=200)
        print(self.pinout[Gpios.SHOCK1])
        print(self.pinout[Gpios.SHOCK2])
        print(self.pinout[Gpios.CHARGE])
        print(self.pinout[Gpios.UPENERGY])     
        print(self.pinout[Gpios.DOWNENERGY])       
        print("Event callbacks created")
    
    def onDownEnergyButtonPressed(self,channel):
        print(self.texto +" onDownEnergyButtonPressed")
        self.DownEnergy.button_pressed_callback()
    def onUpEnergyButtonPressed(self,channel):
        print(self.texto +" onUpEnergyButtonChanged")
        self.UpEnergy.button_pressed_callback()
    def onShockButttonDoblePressed(self):
        print(self.texto +" onShockButttonDoblePressed")
        self.Shock.button_pressed_callback()
    def onChargeButtonPressed(self,channel):
        print(self.texto +" onChargeButtonPressed")
        self.Charge.button_pressed_callback()
    def LEDOn(self):
        print(self.texto +" LEDOn")
    def LEDOff(self):
        print(self.texto +" LEDOff")
    def LEDToggle(self):
        print(self.texto +" LEDToggle")
    
    def onShockButttonPressed1(self, channel):
        print(self.texto +" onShockButttonPressed")
        if (GPIO.input(self.pinout[Gpios.SHOCK1]) == 1) and (GPIO.input(self.pinout[Gpios.SHOCK2]) == 1):
            self.onShockButttonDoblePressed()
    def onShockButttonPressed2(self, channel):
        print(self.texto +" onShockButttonPressed")
        if (GPIO.input(self.pinout[Gpios.SHOCK1]) == 1) and (GPIO.input(self.pinout[Gpios.SHOCK2]) == 1):
            self.onShockButttonDoblePressed()

    def detectPinoutMode(self):    # detecting numbering system
        self.pinoutMode = GPIO.getmode()
        print("BOARD numbering system = 10")
        print("BMC numbering system = 11")
        print("The GPIO Pin mode is " + str(self.pinoutMode))
        print("To see details of the pinout use the command <pinout> in the terminar")

if __name__ == "__main__":
    print("testing has started")
    scriptState = ScriptState.TESTING
    test = GPIOS()
    test.init_Gpios()
    test.scriptState = scriptState
    while True:
        x =1







# to see more interacción with the gpios you can see the input documentation:
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
