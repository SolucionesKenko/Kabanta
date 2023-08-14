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

        # Define deque to hold data with a maximum length of N_SAMPLES
        self.data = deque([], maxlen=self.N_SAMPLES)
        self.databuffer = deque([],maxlen=self.N_SAMPLES)
        self.time = deque([], maxlen=self.N_SAMPLES)
        
        # Initialize timestamp to the current time
        self.timestamp = time()

        self.init_timer()
    
        
    def init_timer(self):
        self.databuffer.clear()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.init_signal)
        self.timer.start()


    def init_signal(self):
        if (np.size(self.databuffer)>=50):
            self.timer.stop()
            size = np.size(self.databuffer)
            for i in range (self.N_SAMPLES-size):
                self.databuffer.append(self.databuffer[i])
                #print(f" indice {i}, tamano del variable {np.size(self.data)}")
            self.data = self.databuffer
            print("Blood Pressure Signal Created")
        else:
            self.update_plot()

    def update_plot(self):
        # Get the current time since the start of the simulation
        t = (time() - self.timestamp) % 5
        # Solve the differential equation for the current time
        P_out = odeint(self.model, self.P_in, [t, t+1])
        #print(P_out)
        # Add the new signals to the data buffers
        self.time.append(t)
        self.databuffer.append((P_out[-1][0]))
    
    # Define the model with the square wave for the aortic pressure
    def model(self, P, t):
        P_aortic = self.square_wave(t)
        Q_in = (P_aortic - P) / self.R_p
        Q_out = (P - self.P_venous) / self.R_d
        return (Q_in - Q_out) / self.C
    
    def square_wave(self, t):
        return self.P_in * (square(2 * np.pi * (self.HR / 60) * t) + 1) / 2
    



