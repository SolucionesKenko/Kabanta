import serial
import serial.tools.list_ports as portList

def addPorts(ui, sPorts):
    for p in sPorts:
        print(p[0])
        ui.port_comboBox.addItem(p[0])
    print("New ports added")

def generate_crc32_table(_poly, custom_crc_table):
    for i in range(256):
        c = i << 24
        for j in range(8):
            c = (c << 1) ^ _poly if (c & 0x80000000) else c << 1
        custom_crc_table[i] = c & 0xffffffff

def onScanReturnButtonClicked(ui, sPorts):
    print("Scan On")
    sPorts.clear()
    sPorts = list(portList.comports())
    ui.port_comboBox.clear()
    addPorts(ui, sPorts)

def onConnectConfirmButtonClicked(ui, sPorts, s, sConnected, sCoder, worker, state, testWorker):
    s = serial.Serial(
        ui.port_comboBox.currentText(), baudrate=115200, timeout=500)

    sConnected = s.is_open
    if(sConnected):
        print("Conectado")
        state = (State.IdleConnected)
        worker = WorkerThread(s, sCoder)
        worker.exiting = False
        state = State.IdleConnected
        worker.signal.sig.connect(testWorker)
        worker.start()
