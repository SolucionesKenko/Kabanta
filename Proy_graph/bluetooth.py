from PyQt5 import QtBluetooth

LocalDevice = QtBluetooth.QBluetoothLocalDevice()
HostDiscoverable = LocalDevice.hostMode
if LocalDevice.isValid():
    print("Pokemon")
    LocalDevice.powerOn()

    DeviceName = LocalDevice.name()
    print("device name",DeviceName)
    DeviceAddress = LocalDevice.address()
    print("Device address",DeviceAddress)
    remots = LocalDevice.connectedDevices()
    print("Device remotes", remots)
    
