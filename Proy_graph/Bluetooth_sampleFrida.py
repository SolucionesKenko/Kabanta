from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothSocket

# Creamos una aplicación Qt
app = QApplication([])
QCoreApplication.setAttribute(QCoreApplication.AA_EnableHighDpiScaling)

# Creamos un agente de descubrimiento de dispositivos Bluetooth
discovery_agent = QBluetoothDeviceDiscoveryAgent()
discovery_agent.setLowEnergyDiscoveryTimeout(5000)  # Establecemos un tiempo de descubrimiento de 5 segundos

# Conectamos la señal deviceDiscovered al método que se ejecutará cuando se descubra un dispositivo
discovery_agent.deviceDiscovered.connect(lambda device: print("Dispositivo encontrado:", device.name(), device.address()))

# Comenzamos el proceso de descubrimiento de dispositivos
discovery_agent.start()

# Creamos un socket Bluetooth
socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)

# Conectamos el socket al dispositivo Bluetooth (debes proporcionar la dirección del dispositivo)
socket.connectToService(device_address, QBluetoothUuid.SerialPort)

# Enviamos datos al dispositivo conectado
socket.write(b'Hola, dispositivo!')

# Leemos datos desde el dispositivo conectado
data = socket.readAll()
print("Datos recibidos:", data)

# Cerramos el socket y detenemos el descubrimiento de dispositivos
socket.close()
discovery_agent.stop()

# Ejecutamos el bucle de eventos de la aplicación Qt
app.exec_()

"""from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothSocket, QBluetoothServiceInfo

def connect_to_device(device):
    # Creamos un socket Bluetooth
    socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)

    # Conectamos el socket al dispositivo Bluetooth
    socket.connectToService(device.address(), QBluetoothUuid.SerialPort)

    if socket.isOpen():
        print("Conectado al dispositivo:", device.name())
        # Enviamos datos al dispositivo conectado
        socket.write(b'Hola, dispositivo!')

        # Leemos datos desde el dispositivo conectado
        data = socket.readAll()
        print("Datos recibidos:", data)

        # Cerramos el socket
        socket.close()
    else:
        QMessageBox.warning(None, "Error", "No se pudo conectar al dispositivo")

def discover_devices():
    # Creamos un agente de descubrimiento de dispositivos Bluetooth
    discovery_agent = QBluetoothDeviceDiscoveryAgent()
    discovery_agent.setLowEnergyDiscoveryTimeout(5000)  # Establecemos un tiempo de descubrimiento de 5 segundos

    # Iniciamos el proceso de descubrimiento de dispositivos
    discovery_agent.start()

    # Esperamos a que el proceso de descubrimiento termine
    discovery_agent.finished.connect(lambda: show_devices(discovery_agent.discoveredDevices()))

def show_devices(devices):
    # Creamos una lista de dispositivos disponibles
    device_list = QListWidget()
    device_list.setWindowTitle("Seleccionar dispositivo")

    # Agregamos los dispositivos a la lista
    for device in devices:
        item = QListWidgetItem(device.name())
        item.setData(0, device)
        device_list.addItem(item)

    # Conectamos la señal itemDoubleClicked al método que se ejecutará cuando se seleccione un dispositivo
    device_list.itemDoubleClicked.connect(lambda item: connect_to_device(item.data(0)))

    device_list.show()

# Creamos una aplicación Qt
app = QApplication([])
QCoreApplication.setAttribute(QCoreApplication.AA_EnableHighDpiScaling)

# Realizamos el descubrimiento de dispositivos
discover_devices()

# Ejecutamos el bucle de eventos de la aplicación Qt
app.exec_()"""