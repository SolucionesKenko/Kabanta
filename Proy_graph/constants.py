from enum import Enum, auto, IntEnum

class SignalState (Enum):
    Playing = auto()
    Pause = auto()
    Stop = auto()
    Idle = auto()

class DEFIBState(Enum):
    Off = auto()
    Select = auto()
    Charging = auto()
    Charged = auto()
    Shock = auto()

class WorkingState(Enum):
    Busy = auto()
    Idle = auto()

class ScenarioState(IntEnum):   #   Estado para simular
    Idle = 0                    #   Listo
    ParoCardiaco = 1            #   Listo
    TaquicardiaSinusal = 2      #   Pendiente
    BradicardiaSinusal = 3      #   Listo
    FlutterAuricular = 4        #   Listo
    FibrilacionAuricular = 5    #   Listo
    TaquicardiaAuricular = 6    #   Pendiente
    ArritmiaSinusal = 7         #   Listo
    FibrilacionVentricular = 8  #   Listo
    TaquicardiaVentricular = 9  #   Listo
    Asistolia = 10
    
class PageState (IntEnum):
    OFFPAGE = 0
    DEFAULTPAGE = 1
    CPRPAGE = 2
    DEFIBPAGE = 3
    PACERPAGE = 4
    LEADPAGE1 = 5 
    LEADPAGE2 = 6

HEART_RATE = "1"
TEMPERATURE = "2"
SPO = "3"
SYSPRESSURE = "4"
DIAPRESSURE = "5"
FR = "6"
CO = "7"
SCENARIO = "8"

PACEMAKER_MA = "1"
PACEMAKER_PPM = "2"
DEFIB_SELECT = "3"
DEFIB_CHARGE = "4"

NUM_CHANNELS = 6
CHANNEL_OFFSETS = [130, 110, 90, 70, 50, 30]
CHANNEL_TEXT_POSITIONS = [-0.2, -0.3, -0.3, -0.3, -0.3, -0.2]
