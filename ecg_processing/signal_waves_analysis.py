import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import neurokit2 as nk

def amplitude_t(signal, r_peaks, t_index):
    t_amplitude = []
    i=0
    while i<len(r_peaks):
        # Be sure t distance from r peaks is < 360 msec
        if t_index[i] - r_peaks[i] >= 360:
            t_amplitude.append(0)
        else:
            try:
                t_amplitude.append(signal[t_index[i]])
            except:
                t_amplitude.append(0)
        i+=1
    return t_amplitude

def amplitude_p(signal, r_peaks, p_peak):
    p_amplitude = []
    i=0
    while i<len(r_peaks):
        if p_peak[i] - r_peaks[i] >= 200:
            p_amplitude.append(0)
        else:
            try:
                p_amplitude.append(signal[p_peak[i]])
            except:
                p_amplitude.append(0)
        i+=1
    return p_amplitude


def amplitude_q(signal, r_peaks, q_peak):
    q_amplitude = []
    i=0
    while i<len(r_peaks):
        try:
            q_amplitude.append(signal[q_peak[i]])
        except:
            q_amplitude.append(0)
        i+=1
    return q_amplitude

def amplitude_s(signal, r_peaks, s_peak):
    s_amplitude = []
    i=0
    while i<len(r_peaks):
        try:
            s_amplitude.append(signal[s_peak[i]])
        except:
            s_amplitude.append(0)
        i+=1
    return s_amplitude


def p_duration_calculate(r_peaks, waves_list, fs):
    p_duration = []
    i=0
    p_peak = waves_list['ECG_P_Peaks']
    p_onset = waves_list['ECG_P_Onsets']
    p_offset = waves_list['ECG_P_Offsets']

    while i<len(r_peaks):
        if p_peak[i] - r_peaks[i] >= 200:
            try:
                p_duration.append(((p_offset[i]-p_onset[i])/fs)*1000)
            except:
                p_duration.append(0)
        i+=1
    return p_duration

def t_duration_calculate(r_peaks, waves_list, fs):
    t_duration = []
    i=0
    t_peak = waves_list['ECG_T_Peaks']
    t_onset = waves_list['ECG_T_Onsets']
    t_offset = waves_list['ECG_T_Offsets']

    while i<len(r_peaks):
        if t_peak[i] - r_peaks[i] >= 360:
            try:
                t_duration.append(((t_offset[i]-t_onset[i])/fs)*1000)
            except:
                t_duration.append(0)
        i+=1
    return t_duration

def qrs_duration_calculate(r_peaks, waves_list, fs):
    qrs_duration = []
    i=0
    q_peak = waves_list['ECG_Q_Peaks']
    s_peak = waves_list['ECG_S_Peaks']

    while i<len(r_peaks):
        try:
            print(r_peaks[i])
            qrs_duration.append(((s_peak[i]-q_peak[i])/fs)*1000)
            print(q_peak[i])
            print(s_peak[i])
            print(((s_peak[i]-q_peak[i])/fs)*1000)
        except:
            qrs_duration.append(0)
        i+=1
    return qrs_duration