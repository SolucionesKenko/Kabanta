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
        self.K = 8  # This is lambda in the EMG equation, influences the skewness of the distribution, A higher value of self.K might make the onset of the plateau more abrupt
        self.loc = .5  # This is mu in the EMG equation, can shift the peak left or right, helping to position the plateau where it's most physiologically realistic
        self.scale = 1  # This is sigma in the EMG equation
        self.co = 0

    def capno_parameters(self, rf, t):
        # Adjust time 't' based on respiratory frequency
        cycle_length = 60 / rf # Length of one respiratory cycle in seconds
        t_mod = t % cycle_length  # Modulate time with respiratory cycle
        y = exponnorm.pdf(t_mod, self.K, self.loc, self.scale)
        # Add noise
        noise = np.random.normal(0, 0.005)  # Noise with a standard deviation of 0.02
        y = y * 3 + noise
        return y

    def update_plot(self, rf, t):
        cycle_length = 60 / rf  # Length of one respiratory cycle in seconds
        phase_length = cycle_length / 3  # Length of one phase in the cycle
        inhalation_length = cycle_length / 3  # Length of inhalation phase
        exhalation_length = 2 * inhalation_length  # Length of exhalation phase
        # Determine the current phase in the cycle
        current_phase_time = t % cycle_length
        if current_phase_time <= inhalation_length:
            # Inhalation phase - return baseline value
            self.co =  0 + np.random.normal(0, 0.005)  # Set an appropriate baseline value
        else:
            # Exhalation phase - return the CO2 waveform
            # Adjust the time for the EMG function
            adjusted_time = (current_phase_time - inhalation_length) % exhalation_length
            self.co = self.capno_parameters(rf, adjusted_time)
        

