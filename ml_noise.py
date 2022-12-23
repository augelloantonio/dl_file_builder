import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# OUR TOOLS
from ecg_processing.signal_filtering import movingAverageMean, bandpassFilt, derivateStep, movingAverageMeanPamTompkins, artifactRemoval

def normal_ecg(size):
    normal = "data/normal/"
    normal_file_list = []
    for filename in os.listdir(normal):
            normal_file_list.append(filename)
    normal_file_list.sort()

    try:
        df = pd.read_csv("good_signal_for_ml_"+str(size)+".csv")
    except:
        df = pd.DataFrame()
        df = df.reindex(columns = [i for i in range(0,size+1)]) 

    count_len = 0

    for normal_file in normal_file_list:
        
        ecg = np.genfromtxt(normal + normal_file, delimiter=',')
        main_removed_ecg = movingAverageMean(ecg, 5)
        finalEcgArtifactRemoved = artifactRemoval(main_removed_ecg)
        finalEcgArtifactRemoved = [i for i in finalEcgArtifactRemoved if i != 0.0]

        count_len = count_len + len(finalEcgArtifactRemoved)

        i = 1
        while i < len(finalEcgArtifactRemoved):
            if i % size == 0:
                this_ecg = finalEcgArtifactRemoved[i-size:i]
                # USE 0 FOR NORMAL SIGNAL, 1 FOR ARTIFACT
                this_ecg.append(0)
                # TODO - set a new csv with a list ok signal lists for every row + (time_window*fs/1000) > n > i-(time_window*fs/1000)
                df = df.append(pd.Series(this_ecg, index=df.columns[:len(this_ecg)]), ignore_index=True)
            i+=1

    print(count_len)

    df.to_csv("good_signal_for_ml_"+str(size)+".csv", index = False, header=True)


def artifact_ecg(size):
    artifact = "data/artifacts/"

    try:
        df = pd.read_csv("artifact_signal_for_ml_"+str(size)+".csv")
    except:
        df = pd.DataFrame()
        df = df.reindex(columns = [i for i in range(0,size+1)]) 

    artifact_file_list = []
    for filename in os.listdir(artifact):
            artifact_file_list.append(filename)

    artifact_file_list.sort()

    count_len = 0

    for artifact_file in artifact_file_list:
        ecg = np.genfromtxt(artifact + artifact_file, delimiter=',')
        main_removed_ecg = movingAverageMean(ecg, 5)

        count_len = count_len + len(main_removed_ecg)

        i = 1
        while i < len(main_removed_ecg):
            if i % size == 0:
                this_ecg = main_removed_ecg[i-size:i]
                # USE 0 FOR NORMAL SIGNAL, 1 FOR ARTIFACT
                this_ecg.append(1)
                # TODO - set a new csv with a list ok signal lists for every row + (time_window*fs/1000) > n > i-(time_window*fs/1000)
                df = df.append(pd.Series(this_ecg, index=df.columns[:len(this_ecg)]), ignore_index=True)
            i+=1    

    print(count_len)
    
    df.to_csv("artifact_signal_for_ml_"+str(size)+".csv"", index = False, header=True)

def main(artifacts=True, normal=True, size=250):
    if normal:
        normal_ecg(size)
    if artifacts:
        artifact_ecg(size)


main(artifacts=True, normal=True, size=250)