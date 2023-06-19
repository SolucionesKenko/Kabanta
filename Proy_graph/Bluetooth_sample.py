"""from PyQt5 import QtCore, QtBluetooth# QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QObject, pyqtSlot


#QtCore.pyqtSlot
class MyClass(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def startDeviceDiscovery(self):
        # Create a discovery agent and connect to its signals
        discoveryAgent = QtBluetooth.QBluetoothDeviceDiscoveryAgent(self)
        discoveryAgent.deviceDiscovered.connect(self.deviceDiscovered)

        # Start a discovery
        discoveryAgent.start()

    QtCore.pyqtSlot(QtBluetooth.QBluetoothDeviceInfo)
    def deviceDiscovered(self, device):
        print("Found new device:", device.name(), '(', device.address().toString(), ')')
        #print(device.address())"""
import PyQt5
from PyQt5 import QtCore
from PyQt5 import QtBluetooth


class DeviceFinder(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.m_devices = []

        self.deviceDiscoveryAgent = QtBluetooth.QBluetoothDeviceDiscoveryAgent(self)
        self.deviceDiscoveryAgent.setLowEnergyDiscoveryTimeout(1000)
        self.deviceDiscoveryAgent.deviceDiscovered.connect(self.add_device)
        self.deviceDiscoveryAgent.error.connect(self.scan_error)
        self.deviceDiscoveryAgent.finished.connect(self.scan_finished)
        self.deviceDiscoveryAgent.canceled.connect(self.scan_finished)

        self.deviceDiscoveryAgent.start(QtBluetooth.QBluetoothDeviceDiscoveryAgent.DiscoveryMethod(2))

    def add_device(self, device):
        # If device is LowEnergy-device, add it to the list
        if device.coreConfigurations() and QtBluetooth.QBluetoothDeviceInfo.LowEnergyCoreConfiguration:
            self.m_devices.append( QtBluetooth.QBluetoothDeviceInfo(device) )
            print("Low Energy device found. Scanning more...")

    def scan_finished(self):
        print("scan finished")
        for i in self.m_devices:
            #QtBluetooth.QBluetoothDeviceInfo.
            print('UUID: {UUID}, Name: {name}, rssi: {rssi}, Address: {address}'.format(UUID=i.deviceUuid().toString(),
                                                                    name=i.name(),
                                                                    rssi=i.rssi(), 
                                                                    address = i.address().toString()))
        self.quit()

    def scan_error(self):
        print("scan error")

    def quit(self):
        print("Bye!")
        QtCore.QCoreApplication.instance().quit()




