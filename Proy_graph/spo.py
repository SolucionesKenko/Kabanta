import sys
from typing import Any, Union, List
from time import time
from PyQt5 import QtCore

import numpy as np
import scipy.io as sio

from collections import deque
from multiprocessing import Queue

# @brief Buffer size for the data (number of points in the plot)
N_SAMPLES = 2001
# @brief Update time of the plot, in ms
PLOT_UPDATE_TIME = 1
# @brief Point to update in each redraw
PLOT_UPDATE_POINTS = -1

class SPO():
    def __init__(self):
        # Spo2 signal initial parameters
        self.timestamp = 0.0
        self.ampR = 0.4  # amplitude for Red signal
        self.ampIR = 0.270  # amplitude for InfraRed signal
        self.minR = 0.45  # Displacement from zero for Red signal
        self.minIR = 0.45  # Displacement from zero for Red signal
        
        self.change(98)
    
    def ppg_parameters(self, minR, ampR, minIR, ampIR, t, HR):
        """
        Store the function of two signals - e.g PPG Red and Infrared channel signals
        We can also put here a sine, cosine, etc.
        """
        f = HR *( 1 / 60)
         # Spo2 Red signal function
        self.sR = minR + ampR * (0.05 * np.sin(2 * np.pi * t * 3 * f) + 0.4 * np.sin(2 * np.pi * t * f) +
                                 0.22 * np.sin(2 * np.pi * t * 2 * f + 45))
        # self.sR = minR + ampR * (0.5 * np.sin(2 * np.pi * t * f) + 0.22 * np.sin(2 * np.pi * t * 2 * f + 40))
        # Spo2 InfraRed signal function
        self.sIR = minIR + ampIR * (0.05 * np.sin(2 * np.pi * t * 3 * f) + 0.4 * np.sin(2 * np.pi * t * f) +
                                    0.22 * np.sin(2 * np.pi * t * 2 * f + 45))
        # self.sIR = minIR + ampIR * (0.5 * np.sin(2 * np.pi * t * f) + 0.22 * np.sin(2 * np.pi * t * 2 * f + 40))
        
        return self.sR, self.sIR
    
    def change(self, spoValue):
        """
        Change the value of the SpO2 when moving the slider.
        It also have the list of SpO2 values vs the R value
        """
        sp02 = list(range(50, 101))[::-1]

        R = [0.50, 0.55, 0.60, 0.64, 0.66, 0.70, 0.71, 0.72, 0.73, 0.75, 0.76, 0.77, 0.78, 0.80, 0.81, 0.82, 0.83,
             0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00,
             1.01, 1.00, 1.05, 1.11, 1.12, 1.16, 1.19, 1.25, 1.27, 1.32, 1.33, 1.35, 1.39, 1.43, 1.47, 1.52, 1.50]

        Ri = [0] * 51

        Ri[sp02.index(spoValue)] = R[sp02.index(spoValue)]

        # R-IR values & SpO2
        rR = [0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.4, 0.4,
              0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
              0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]

        IR = [1.0, 0.9, 0.7, 1.0, 0.9, 0.7, 0.7, 0.6, 0.6, 0.58, 0.57, 0.54, 0.52, 0.5, 0.5, 0.48, 0.47, 0.46, 0.45,
              0.445, 0.44, 0.43, 0.42, 0.39, 0.4, 0.39, 0.38, 0.38, 0.37, 0.35, 0.36, 0.35, 0.35, 0.34, 0.34, 0.34,
              0.33, 0.32, 0.32, 0.31, 0.3, 0.3, 0.3, 0.29, 0.29, 0.28, 0.28, 0.27, 0.27, 0.26, 0.25]

        self.ampR = rR[sp02.index(spoValue)]
        self.ampIR = IR[sp02.index(spoValue)]


    def init(self, amp_r, amp_ir, hr, spo):
        t = np.linspace(0.2, 0.8, 10)
        s_r, s_ir = self.ppg_parameters(self.minR, amp_r, self.minIR, amp_ir, t, hr)

        data = sio.loadmat('curvesHB')
        x = data['x']

        xhb_o2, hb_o2, x_oxy_hb, oxy_hb = x[0], x[1], x[2], x[3]

        spo2value = spo 
        hb_x = np.linspace((700 - spo2value), 1000, 10)
        hb_y = x[5]
    
    def update(self, hr, tppg):
        self.sR, self.sIR = self.ppg_parameters(self.minR, self.ampR, self.minIR, self.ampIR, tppg, hr)
        self.sR = self.sR * 1.5 
        self.sIR = self.sIR * 1.5 
