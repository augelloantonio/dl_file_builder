import numpy as np
from ecg_processing.utils import floatListDiff

def calculateNNI(rpeaks):
    rr_diff = floatListDiff(rpeaks)
    nni_div = np.divide(rr_diff, 250)
    nni = np.multiply(nni_div, 1000)

    i = 0
    nniFiltered = []
    while i < nni.size: 
        if nni[i] not in range(1, 5000):
            i += 1
        else:
            nniFiltered.append(nni[i])
            i += 1
    return nni

def calculateBpm(nni):
    bpm = 0
    r = []
    if len(nni) > 2:
        for i in range(0, len(nni)):
            r.append(60000 / nni[i])

        bpm = np.mean(r)
    return bpm, r

def calculateRmssd(nni):
    if len(nni)>2:
        nni = np.array([i for i in nni if i in range(200, 2000)])
        diff_nni_rmssd = floatListDiff(nni)
        diff_nni_pow_rmssd = np.power(diff_nni_rmssd, 2)
        diff_nni = np.divide(diff_nni_pow_rmssd, (nni.size - 2))
        diff_nni_somm_rmssd = np.mean(diff_nni)
        rmssd = np.sqrt(diff_nni_somm_rmssd)
    else:
        rmssd = 0

    return rmssd

""" def calculateCorrectRmssdFromNNI(nni):

    rmssd = 0.0
    correctNNI = []
    for i in nni:
        if i >= 200 and i<= 1800:
            correctNNI.add(i)
    
    diff_nni_rmssd = FloatListDiff(correctNNI)
    diff_nni_pow_rmssd = SlicePow(diff_nni_rmssd, 2)
    diff_nni_somm_rmssd = SliceMean(diff_nni_pow_rmssd)

    rmssd = Math.Sqrt(diff_nni_somm_rmssd)
    
    return rmssd """

def calculateRmssd2(nni):
    nni = np.where(nni < 2000, nni, nni>200)
    diff_nni_rmssd = np.diff(nni)
    diff_nni_pow_rmssd = np.power(diff_nni_rmssd, 2)
    sum_nni = np.sum(diff_nni_pow_rmssd)
    diff_nni = np.divide(sum_nni, (nni.size - 1))
    #diff_nni_somm_rmssd = np.mean(diff_nni)

    rmssd = np.sqrt(diff_nni)
    
    if not np.isnan(rmssd):
        print(rmssd)

    return rmssd