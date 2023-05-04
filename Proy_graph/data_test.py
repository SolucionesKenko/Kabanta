import sys 
import numpy as np
import os
import wfdb
record = wfdb.rdrecord('/Users/mac/Documents/AlanBecarioSW/PruebasQt/Proy_graph/Signals/00001_lr',channels=[0,1,2],sampfrom=0)
signal = record.p_signal
ecg_signal = signal.tolist()
print(ecg_signal[3])

