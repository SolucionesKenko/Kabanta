import sys 
import numpy as np
import os
import wfdb
import scipy.signal
import neurokit2 as nk
record = wfdb.rdrecord('Signals/00001_lr',channels=[0,1,2],sampfrom=0)
ecg12 = nk.ecg_simulate(duration=10, method="multileads")
#ecg12 = list(ecg12)

signal = record.p_signal
ecg_signal = signal.tolist()
print(ecg_signal[3])
#Cambios de Codigo Main, Separacion de StyleSheet, y agregado de Generacion de senales con neurokit





