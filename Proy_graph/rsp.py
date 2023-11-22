import pyqtgraph as pg
import numpy as np
from scipy.stats import exponnorm
from collections import deque
from PyQt5 import QtCore
from time import time


class RSP():
    def __init__(self):
        self.timer = QtCore.QTimer()
        # Define parameters for the EMG distribution
        self.rf = 0  # This is lambda in the EMG equation, influences the skewness of the distribution, A higher value of self.K might make the onset of the plateau more abrupt
        self.amplitude = 0.4  # This is mu in the EMG equation, can shift the peak left or right, helping to position the plateau where it's most physiologically realistic
        self.baseline = 0  # This is sigma in the EMG equation
        self.rsp = 0

    def update_plot(self, rf, t):
        cycle_length = 60 / rf  # Length of one respiratory cycle in seconds
        # Convert time to radians, scaled by the respiratory cycle
        radian_time = (t % cycle_length) / cycle_length * 2 * np.pi
        # Sinusoidal waveform for respiration
        self.rsp = self.amplitude * np.sin(radian_time) + self.baseline
        
        
