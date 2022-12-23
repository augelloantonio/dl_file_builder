import numpy as np

path = "data/20220329_103913.002.ecg"
ecg = np.genfromtxt(path, delimiter=',')

ecg = ecg[~np.isnan(ecg)]

with open('data/artifacts/16.ecg', 'w') as f:
    for i in ecg[2800:2950]:
        f.write(str(i)+"\n")

""" with open('data/normal/17.ecg', 'w') as f:
    for i in ecg[:2500]:
        f.write(str(i)+"\n") """