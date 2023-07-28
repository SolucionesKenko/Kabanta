import pyqtgraph as pg
import numpy as np
from scipy.stats import exponnorm
from collections import deque
from PyQt5 import QtCore
from time import time


class CO2():
    def __init__(self):
        self.timer = QtCore.QTimer()
        # Define parameters for the EMG distribution
        self.K = 4  # This is lambda in the EMG equation
        self.loc = 4  # This is mu in the EMG equation
        self.scale = 0.5  # This is sigma in the EMG equation
        self.N_SAMPLES = 2000

        # Define deque to hold data with a maximum length of N_SAMPLES
        self.data = deque([], maxlen=self.N_SAMPLES)
        self.time = deque([], maxlen=self.N_SAMPLES)

        # Initialize timestamp to the current time
        self.timestamp = time()
        self.init_timer()

    def init_timer(self):
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.init_signal)
        self.timer.start()

    def init_signal(self):
        if ((time() - self.timestamp) > 5):
            self.timer.stop()
            size = np.size(self.data)
            for i in range (self.N_SAMPLES-size):
                self.data.append(self.data[i-1])
            print(" CO2 Signal Created")
        else:
            self.update_plot()

    def capno_parameters(self, t_mod):
        y = exponnorm.pdf(t_mod, self.K, self.loc, self.scale)

        # Add noise
        noise = np.random.normal(0, 0.02, len(t_mod))  # Noise with a standard deviation of 0.02
        y = y + noise
        return y

    def update_plot(self):
        # Get the current time since the start of the simulation
        self.tCapno = (time() - self.timestamp) % 5
        # Generate new capnogram signal based on the current time
        self.s = self.capno_parameters(np.array([self.tCapno]))
        # Add the new signals to the data buffers
        self.time.append(self.tCapno)
        self.data.append(self.s[0]*10)

