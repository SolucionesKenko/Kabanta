from scipy.integrate import odeint
from scipy.signal import square
from collections import deque
from PyQt5 import QtCore
import numpy as np
from time import time

class BloodPressure():
    def __init__(self):
        self.timer = QtCore.QTimer()
        # Define the parameters for the model
        self.R_p = 0.5  # Proximal resistance
        self.R_d = 1    # Distal resistance
        self.C = 1      # Compliance
        self.P_in = 35  # Inlet pressure
        self.P_venous = 0  # Venous pressure
        self.HR = 60  # Heart rate in beats per minute

        self.N_SAMPLES = 2000

        self.p = 0

        # Define deque to hold data with a maximum length of N_SAMPLES

        
        # Initialize timestamp to the current time
        #self.timestamp = time()

        #self.init_timer()

    def update_plot(self, hr, t):
        self.HR = hr
        # Solve the differential equation for the current time
        P_out = odeint(self.model, self.P_in, [t, t+1])
        #print(P_out)
        # Add the new signals to the data buffers
        self.p = ((P_out[-1][0])-12)/48
    
    # Define the model with the square wave for the aortic pressure
    def model(self, P, t):
        P_aortic = self.square_wave(t)
        Q_in = (P_aortic - P) / self.R_p
        Q_out = (P - self.P_venous) / self.R_d
        return (Q_in - Q_out) / self.C
    
    def square_wave(self, t):
        return self.P_in * (square(2 * np.pi * (self.HR / 60) * t) + 1) / 2
    



