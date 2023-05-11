import numpy as np
import os
import wfdb
import scipy.signal

def generate_ecg_signal(duration, sampling_rate, heart_rate):
    # Parámetros para el modelo de ondas QRS basado en Gaussianas
    qrs_params = [
        (-0.025, 0.25, 0.01),
        (0.04, 0.1, 0.02),
        (-0.025, 0.25, 0.03)
    ]

    # Calcula la duración de un latido cardíaco en muestras
    samples_per_beat = int(sampling_rate * 60 / heart_rate)

    # Genera una onda QRS utilizando la suma de Gaussianas
    t = np.linspace(0, 1, samples_per_beat)
    qrs_wave = np.zeros_like(t)
    for A, a, b in qrs_params:
        qrs_wave += A * np.exp(-((t - a) * 2) / (2 * b * 2))

    # Repite la onda QRS para llenar la duración total
    num_beats = int(duration * heart_rate / 60)
    gen_ecg_signal = np.tile(qrs_wave, num_beats)

    # Corta la señal a la duración exacta en muestras
    total_samples = int(duration * sampling_rate)
    gen_ecg_signal = gen_ecg_signal[:total_samples]

    return gen_ecg_signal



def simular_ecg(fs, duracion):
    # Definir la frecuencia de muestreo y la duración de la señal
    t = np.arange(0, duracion, 1/fs)

    # Generar la señal de ECG simulada
    frecuencia_cardiaca = 60  # latidos por minuto
    amplitud_p = 2.5  # amplitud de la onda P
    amplitud_qrs = 12  # amplitud del complejo QRS
    amplitud_t = 2.5  # amplitud de la onda T

    # Derivación I
    ecg_I = amplitud_p * np.sin(2 * np.pi * frecuencia_cardiaca * t) + \
            amplitud_qrs * np.sin(2 * np.pi * 2 * frecuencia_cardiaca * t + np.pi/6) + \
            amplitud_t * np.sin(2 * np.pi * 1.2 * frecuencia_cardiaca * t + np.pi/3)

    # Derivación II
    ecg_II = amplitud_p * np.sin(2 * np.pi * frecuencia_cardiaca * t) + \
             amplitud_qrs * np.sin(2 * np.pi * 2 * frecuencia_cardiaca * t) + \
             amplitud_t * np.sin(2 * np.pi * 0.8 * frecuencia_cardiaca * t)

    # Derivación III
    ecg_III = amplitud_p * np.sin(2 * np.pi * frecuencia_cardiaca * t) + \
              amplitud_qrs * np.sin(2 * np.pi * 2 * frecuencia_cardiaca * t - np.pi/6) + \
              amplitud_t * np.sin(2 * np.pi * 0.6 * frecuencia_cardiaca * t + np.pi/6)
    
    ecg_signals = {'DI': ecg_I, 'DII': ecg_II, 'DIII': ecg_III}
    return ecg_signals


def generate_ecg_signal2(fs, dur, fc, amp):
    """
    Genera una señal de ECG en las tres derivaciones (DI, DII, DIII).

    Args:
        fs (float): Frecuencia de muestreo de la señal.
        dur (float): Duración de la señal en segundos.
        fc (float): Frecuencia cardíaca en latidos por minuto.
        amp (float): Amplitud de la señal.

    Returns:
        dict: Un diccionario que contiene tres claves, 'DI', 'DII' y 'DIII', cada una con su señal de ECG correspondiente.
    """
    # Definir vector de tiempo
    t = np.arange(0, dur, 1/fs)

    # Generar señal en cada derivación
    di = amp * np.sin(2 * np.pi * fc * t)
    dii = amp * np.sin(2 * np.pi * fc * t + np.pi/6)
    diii = amp * np.sin(2 * np.pi * fc * t - np.pi/6)

    # Crear un diccionario con las señales en cada derivación
    ecg_signals = {'DI': di, 'DII': dii, 'DIII': diii}

    return ecg_signals


# Ejemplo de uso
duration = 10  # Duración de la señal en segundos
sampling_rate = 1000  # Frecuencia de muestreo en Hz
heart_rate = 60  # Frecuencia cardíaca en latidos por minuto

# Vectores base definidos arbitrariamente
base_vectors = [
    np.array([0, 1, 0]),
    np.array([0, 0, 1]),
]

# Ejemplo de uso
duration = 10  # Duración de la señal en segundos
sampling_rate = 1000  # Frecuencia de muestreo en Hz
heart_rate = 60  # Frecuencia cardíaca en latidos por minuto

gen_ecg_signal = generate_ecg_signal(duration, sampling_rate, heart_rate)

# Generar señal de ECG con parámetros personalizados
fs = 1000 # Frecuencia de muestreo
dur = 5 # Duración de la señal en segundos
fc = 60 # Frecuencia cardíaca en latidos por minuto
amp = 1.5 # Amplitud de la señal
ecg_signals3 = generate_ecg_signal2(fs, dur, fc, amp)

fs = 100
duracion = 10
gen_ecg_signal2 = simular_ecg(fs,duracion)