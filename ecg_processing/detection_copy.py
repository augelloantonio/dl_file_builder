import numpy as np
import datetime
from ecg_processing.utils import mean
from ecg_processing.signal_analysis import calculateBpm, calculateNNI
from ecg_processing.signal_peak_detector import ACSPeakDetector

def tsipourasBeatsClassification(nni, rpeaks, pulse):

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.5
    pulse = 0

    is_ventriculat_rythm = True
    counter_afib = 0

    x = 0
    i = 0
    while i < len(nni)-3:
        nni_section = nni[i:i+3]
        nni_1 = nni_section[0]
        nni_2 = nni_section[1]
        nni_3 = nni_section[2]

        ecgAnomaliesList.append("N")
        
        # CAT 5 - VF/VT
        if nni_2 < 600 and nni_3 < nni_2:
            i = i+1
            pulse = 1
            ecgAnomaliesList[-1] = "vf/vt"
            while is_ventriculat_rythm:
                if (nni_1 + nni_2 + nni_3 < 1800) or (nni_1 < 800 and nni_2 < 800 and nni_3 < 800):
                    counter_afib = counter_afib +1
                    # print("AFiB")
                    ecgAnomaliesList[-1] = "vf/vt"
                    i = i+1
                    pulse = pulse + 1

                    # print(counter_afib)

                else:       
                    is_ventriculat_rythm = False
                    if (pulse < 4):
                        ecgAnomaliesList[-1] = "N"
                        i = i-pulse
                        pulse = counter_afib

        
        # CAT 3 & CAT 2
        if nni_2 < nni_1*a and nni_1 < b*nni_3:
            if nni_2+nni_3 < 2*nni_1:
                ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CAT 2
            else:
                ecgAnomaliesList[-1] = "ventricular premature beats" # CAT 3
        else:
            print([nni_1, nni_2, nni_3])          
        # CAT 4
        if nni_2 > c*nni_1:
            ecgAnomaliesList[-1] = "escape beat" # CAT 4
        
        i+=1 
    return ecgAnomaliesList


def beatsClassification(nni, rpeaks, pulse):

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.5
    pulse = 0
    
    beat_list_peaks = []    
    nni_list = []

    for i in nni:
        nni_list.append(i)
    nni_list.append(0)
    nni_list.append(0)
    
    for i in range(0, len(nni_list)-2):

        ecgAnomaliesList.append("N")
        
        # CAT 5 - VF/VT
        if nni_list[i+1] < 600 and nni_list[i+2] < nni_list[i+1] < 800:
            if (nni_list[i] + nni_list[i+1] + nni_list[i+2] < 1800) or (nni_list[i] < 800 and nni_list[i+1] < 800 and nni_list[i+2] < 800):
                pulse += 1
                    
            if (pulse > 4):
                ecgAnomaliesList[-1] = "vf/vt"
                beat_list_peaks.append(rpeaks[i % 3])
                i = i-pulse
        
        if ecgAnomaliesList[i-1] == "N":
            # CAT 3 & CAT 2
            if nni_list[i+1] < nni_list[i]*a and nni_list[i] < b*nni_list[i+2]:
                if nni_list[i+1]+nni_list[i+2] < 2*nni_list[i]:
                    # print("ATRIAL 1")
                    # print([nni_list[i], nni_list[i+1], nni_list[i+2]])
                    ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CAT 2
                    beat_list_peaks.append(rpeaks[i % 3])
                else:
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CAT 3
                    beat_list_peaks.append(rpeaks[i % 3])

        if ecgAnomaliesList[i-1] == "N":
            # CAT 4
            if nni_list[i+1] > c*nni_list[i]:
                ecgAnomaliesList[-1] = "escape beat"
                beat_list_peaks.append(rpeaks[i % 3])
        
    return ecgAnomaliesList


def beatsClassification2(nni, rpeaks, pulse, normal_rythm):
    ecgAnomaliesList = []
    a = 0.5
    b = 0.5
    c = 2.0
    pulse = 0

    beat_list_peaks = []    

    for i in range(0,len(nni)%2):
        nni.append(0)
        
    for i in range(0, len(nni)-2):
        ecgAnomaliesList.append("N")
        
        # CAT 5 - VF/VT
        if nni[i+1] < 600 and nni[i+2] < nni[i+1] < 800:
            if (nni[i] + nni[i+1] + nni[i+2] < 1800) or (nni[i] < 800 and nni[i+1] < 800 and nni[i+2] < 800):
                pulse += 1
                #if not normal_rythm:
                    #pulse += 1
                    
            if (pulse > 4):
                ecgAnomaliesList[-1] = "vf/vt"
                beat_list_peaks.append(rpeaks[i % 3])
                i = i-pulse
        
        if ecgAnomaliesList[i-1] == "N":
            # CAT 3 & CAT 2
            if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
                if nni[i+1]+nni[i+2] < 2*nni[i]:
                    ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CAT 2
                    beat_list_peaks.append(rpeaks[i % 3])
                else:
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CAT 3
                    beat_list_peaks.append(rpeaks[i % 3])
      
        if ecgAnomaliesList[i-1] == "N":
            # CAT 4
            if nni[i+1] > c*nni[i]:
                ecgAnomaliesList[-1] = "escape beat"
                beat_list_peaks.append(rpeaks[i % 3])
    
    return ecgAnomaliesList, pulse


def beatsClassification3(nni, rpeaks, pulse, normal_rythm):

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.2
    pulse = 0

    beat_list_peaks = []  

    """ for i in range(0, len(nni)%2):
        nni.append(0)  """
                
    for i in range(0, len(nni)-2):
        
        ecgAnomaliesList.append("N")

        # CAT 5 - VF/VT
        if nni[i+1] < 600 and 1800*nni[i+1] < nni[i]:
            if (nni[i] + nni[i+1] + nni[i+2] < 1800) or (nni[i] < 800 and nni[i+1] < 800 and nni[i+2] < 800):
                pulse += 1
                #if not normal_rythm:
                    #pulse += 1
                    
            if (pulse > 4):
                ecgAnomaliesList[-1] = "vf/vt"
                beat_list_peaks.append(rpeaks[i % 3])
                i = i-pulse 
        
        if ecgAnomaliesList[i] == "N":
            # CAT 3 & CAT 2
            if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
                if nni[i+1]+nni[i+2] < 2*nni[i]:
                    ecgAnomaliesList[i] = "atrial/nodal/supraventricular beat" # CAT 2
                    beat_list_peaks.append(rpeaks[i+2])
                else:
                    ecgAnomaliesList[i] = "ventricular premature beats" # CAT 3
                    beat_list_peaks.append(rpeaks[i+2])
      
        if ecgAnomaliesList[i-1] == "N":
            # CAT 4
            if nni[i+1] > c*nni[i]:
                ecgAnomaliesList[-1] = "escape beat"
                beat_list_peaks.append(rpeaks[i])
    
    return ecgAnomaliesList, pulse

def beatsClassification4(signal, nni, rpeaks, pulse, normal_rythm):

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.5
    pulse = 0

    beat_list_peaks = []  

    counter_afib = 0

    ecgANTotal = []
    counter_anomalies_loop = 0

    """ for i in range(0, len(nni)%2):
        nni.append(0)  """
    for i in range(0, len(nni)):
        ecgAnomaliesList.append("N")
        ecgANList = ["N", "N", "N"]
        
        is_ventriculat_rythm = True

        nni = [int(x) for x in nni]
    
        if i < len(nni)-2:
            
            # print([nni[i], nni[i+1], nni[i+2]])

            """ C1 """
            if (nni[i+1] < 600) and (1.8*nni[i+1] < nni[i]): #c1
                while is_ventriculat_rythm:

                    # print("HERE AFIB")
                    # print(pulse)
                    ecgAnomaliesList[-1] = "vt/vf" # CATEGORY 3
                    ecgANList[1] = "vt/vf" # CATEGORY 3
                    beat_list_peaks.append(rpeaks[i+2])
                    i = i+1
                    pulse = 1

                    
                    """ C2 """ 
                    counter_afib = counter_afib+1
                    # ("counter_afib")
                    # print(counter_afib)
                    if (nni[i] < 800 and nni[i+1] < 800 and nni[i+2]<800) or ((nni[i] + nni[i+1] + nni[i+2])< 1800): #c2
                        counter_afib = counter_afib +1
                        pulse =  pulse + 1
                        ecgAnomaliesList[-1] = "vt/vf" # CATEGORY 3
                        ecgANList[1] = "vt/vf" # CATEGORY 3
                        beat_list_peaks.append(rpeaks[i+2])
                        i = i+1
                        #if not normal_rythm:
                            #pulse += 1
                    else:
                        if pulse < 4:
                            is_ventriculat_rythm=False
                            pulse = counter_afib
                            ecgAnomaliesList[-1] = "N" # CATEGORY 1
                            ecgANList[1] = "N" # CATEGORY 1
                            beat_list_peaks.append(rpeaks[i % 3])
                            i = i-pulse
                            ecgANTotal[counter_afib] = "N"
                        else:
                            for x in range (i, pulse):
                                ecgAnomaliesList[x] = "vt/vt" # CATEGORY 5

            """ C3 or C4 or C5 """    
            if nni[i+1]*1.15 < nni[i] and nni[i+1]*1.15 < nni[i+2]: #C3
                ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                beat_list_peaks.append(rpeaks[i+2])
                if (nni[i+1]*1.9 < nni[i+2]):
                    # print("HERE PVC C3")
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                    beat_list_peaks.append(rpeaks[i+2])
                """ else:
                    print("ATRIAL C3")
                    print([nni[i], nni[i+1], nni[i+2]])
                    print(rpeaks[i+2]) """

            if abs(nni[i]-nni[i+1])<300 and nni[i]<800 or nni[i+1]<800 and nni[i+2]>1.2*mean(nni[i], nni[i+1]): #C4
                ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                beat_list_peaks.append(rpeaks[i+2])
                if (nni[i+1]*1.9 < nni[i+2]):
                    # print("HERE PVC C4")
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                    beat_list_peaks.append(rpeaks[i+2])
                """ else:
                    print("ATRIAL C4")
                    print([nni[i], nni[i+1], nni[i+2]]) """

            if abs(nni[i+1]-nni[i+2])<300 and nni[i+1]<800 or nni[i+2]<800 and nni[i]>1.2*mean(nni[i+1], nni[i+2]): #C5 
                ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                beat_list_peaks.append(rpeaks[i+2])
                if (nni[i+1]*1.9 < nni[i+2]):
                    # print("HERE PVC C5")
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                    beat_list_peaks.append(rpeaks[i+2])
                """ else:
                    print("ATRIAL C5")
                    print([nni[i], nni[i+1], nni[i+2]])
                    print(rpeaks[i+2]) """

            """ # We nknow that pvcs are mostrly negative in morphology and the signal peak extracted is < 0 
            # so we check if the current peak is < -1.0 mV to avoid errors
            if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
                #if signal[rpeaks[i+2]][0] < -0.5:
                ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                beat_list_peaks.append(rpeaks[i+2])
                if (abs(nni[i+2]-nni[i])*10)<nni[i+1]:
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                    beat_list_peaks.append(rpeaks[i+2])  """

            # CAT 3 & CAT 2 as Tsipouras
            #if ecgANList[1] == "atrial/nodal/supraventricular beat" or ecgANList[1] == "N":
            if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
                    if nni[i+1]+nni[i+2] < 2*nni[i]:
                        ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CAT 2
                        ecgANList[1] = "atrial/nodal/supraventricular beat"
                        if signal[rpeaks[i+2]][0] < -0.5:
                            ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                            beat_list_peaks.append(rpeaks[i+2])
                    else :
                        # print("HERE PVC")
                        # print(nni[i+1]+nni[i+2])
                        # print(2*nni[i])
                        ecgAnomaliesList[-1] = "ventricular premature beats" # CAT 3
                        ecgANList[1] = "ventricular premature beats" # CATEGORY 3

            """ # C6  
            if nni[i+1] in range(2200, 3000) and (abs(nni[i]-nni[i+1])<200 or abs(nni[i+1]-nni[i+2])<200):
                ecgAnomaliesList[-1] = "escape beat" # CATEGORY 4
                ecgANList[1] = "escape beat" # CATEGORY 4
                beat_list_peaks.append(rpeaks[i]) """
            
            """
            NEW IF |NNI3-NNI1|>NNI2 -> PVC
            """                
            if ecgANList[1] != "N":
                if signal[rpeaks[i+2]][0] < -1.0:
                    ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3
            
            if ecgANList[1] != "N":
                if nni[i+1] > c*nni[i] and (nni[i+1]*1.9 > nni[i+2]):
                    ecgANList[1] = "escape sabeat" # CAT 4 
    
        if counter_anomalies_loop == 0:
            ecgANTotal.append(ecgANList[1])
            counter_anomalies_loop += 1
        else:
            ecgANTotal.append(ecgANList[1])

    return ecgANTotal, pulse  

def beatsClassification4_new(signal, nni, rpeaks, pulse, normal_rythm):

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.5
    pulse = 0

    beat_list_peaks = []  

    """ for i in range(0, len(nni)%2):
        nni.append(0)  """
                
    for i in range(0, len(nni)):
        
        ecgAnomaliesList.append("N")

        if i< len(nni)-2:
        # CAT 5 - VF/VT
            if nni[i+1] < 600 and 1800*nni[i+1] < nni[i]: #c1
                ecgAnomaliesList[i] = "ventricular premature beats" # CAT 3
                beat_list_peaks.append(rpeaks[i+2])
                if nni[i] < 700 and nni[i+1] < 700 and nni[i+2]<700 or (nni[i] + nni[i+1] + nni[i+2])< 1700: #c2
                    pulse += 1
                    #if not normal_rythm:
                        #pulse += 1
                        
                if (pulse > 4):
                    ecgAnomaliesList[-1] = "vf/vt"
                    beat_list_peaks.append(rpeaks[i % 3])
                    i = i-pulse
            
            if ecgAnomaliesList[i] == "N":
                print(rpeaks[i+2])
                if nni[i+1]*1150 < nni[i] and nni[i+1]*1150 < nni[i+2] or abs(nni[i]-nni[i+1])<300 and nni[i]<800 and nni[i+1]<800 and nni[i+2]>1200*mean(nni[i], nni[i+1]) or abs(nni[i+1]-nni[i+2])<300 and nni[i+1]<800 and nni[i+2]<800 and nni[i]>1200*mean(nni[i+1], nni[i+2]):
                    if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
                        if nni[i+1]+nni[i+2] < 2*nni[i]:
                            ecgAnomaliesList[i] = "atrial/nodal/supraventricular beat" # CAT 2
                            beat_list_peaks.append(rpeaks[i+2])
                            
                    if signal[rpeaks[i+2]].all() < -0.5:
                        ecgAnomaliesList[i] = "ventricular premature beats" # CAT 3
                        beat_list_peaks.append(rpeaks[i+2])

            if ecgAnomaliesList[i] == "N":
                print(rpeaks[i+2])
                if 2200 < nni[i] < 300 and (abs(nni[i]-nni[i+1])<200 or abs(nni[i+1]-nni[i+2])<200):
                    ecgAnomaliesList[i] = "escape beat" # CAT 2
                
    return ecgAnomaliesList, pulse

def detect_arrythmia(nni, normal_rythm):
    """
    If the difference between the max and the min nni
    is > 400 then there is an arrhythmia
    # Calculate Arrhythmia - Study:
    https://litfl.com/sinus-arrhythmia-ecg-library/#:~:text=The%20P%2DP%20interval%20varies%20widely,a%20variability%20of%20over%20400ms.
    """

    max_nni = np.max(nni)
    min_nni = np.min(nni)
    diff_nni = max_nni - min_nni

    beat_rythm = 'Normal'

    if diff_nni > 400:
        normal_rythm = False
        beat_rythm = 'Arrhythmia'

    return normal_rythm, beat_rythm


def detect_fibrillation(signal, sampling_rate, pulse, normal_rythm, beat_rythm, fibrillation_beat=False, nni=[]):
    """
    Detect Fibrillation rythm - to use in a loop while iterating over the signal data
    ** Arguments:
    - signal: ecg to process
    - sampling_rate: sampling frequency of the sample
    - pulse: beat as fibrillation detected
    - fibrillation_beat: define if the beat is fibrillation
    - normal_rythm: define the type of the rythm
    - beat_rythm: define the interval rythm
    """
    if nni is None:
        nni = calculateNNI(signal)

    x = 0

    # Check if the interval has a normal rythm
    normal_rythm, beat_rythm = detect_arrythmia(nni, normal_rythm)

    # Afib is an arithmic rythm

    if not normal_rythm:
        while x < len(nni):
            x += 1
            if x < len(nni)-2:
                # Detect VF if nni[i] < 600 msec
                if nni[x] < 600 and nni[x+1] < nni[x+2]:
                    pulse = sum_el(pulse)
                    fibrillation_beat = True

                    # if pulse is > 4 then it can be considered as category 5
                    if pulse > 4:
                        beat_rythm = 'Atrial Fibrillation'

    return pulse, fibrillation_beat, normal_rythm, beat_rythm


def detect_bradycardia(signal, sampling_rate, sinus_rythm, beat_rythm, bpm=None):
    """
    Set ad default < 50bpm
    **ARGS
    - signal: the ecg signal interval to process
    - sampling_rate: the sampling frequency
    - sinus_rythm: if the rhytm is sinus of not
    - beat_rythm: the beat rythm
    RETURN
    - beat_rythm: the beat rythm
    """

    if bpm == None:
        bpm = calculateBpm(signal)

    # Check for Bradycardia
    if bpm < 50:
        if not sinus_rythm:
            beat_rythm = 'Bradycardia'
            return beat_rythm
        else:
            beat_rythm = 'Sinus Bradycardia'
            """
            If the rythm is bradycardic and the P wave absent we could face a
            Third-degree, or complete, Seno-Atrial block
            """
            return beat_rythm
    else:
        return beat_rythm


def detect_tachycardia(signal, sampling_rate, beat_rythm, bpm=None):
    """
    Define in Bradycardic Rythm
    Set ad default < 50bpm
    **ARGS
    - signal: the ecg signal interval to process
    - sampling_rate: the sampling frequency
    - beat_rythm: the beat rythm
    RETURN
    - beat_rythm: the beat rythm
    """
    if bpm == None:
        bpm = get_mean_hr(signal, sampling_rate)

    if bpm > 90 and beat_rythm == 'Normal':
        beat_rythm = 'Sinus Tachycardia'
        return beat_rythm
    else:
        return beat_rythm


def detect_afib(nni, fs):
    ssdThreshold = 120
    prev_sdrr_true = False
    i=1
    while i < len(signal):
        if i % fs*120==0:
            peaks,thrheshold_list = ACSPeakDetector3(signal[i-fs*120:i], 250)
            nni = calculateNNI(peaks)
            bpm = calculateBpm(nni)
   
            rrsd = np.std(nni)
            if bpm > 100:
                if rrsd > ssdThreshold:
                    print("AFIB DETECTED")
            else:
                if rrsd > ssdThreshold and prev_sdrr_true == False:
                    prev_sdrr_true = True
                if rrsd > ssdThreshold and prev_sdrr_true == True:
                    if bpm > 100 and rrsd>ssdThreshold:
                        print("AFIB DETECTED")
                    else:
                        print("POTENTIAL AFIB DETECTED")

        i+=1

def countAnomalies(beatClassificationList, peaks):
        
    count_n = 0
    count_pvc = 0
    count_escape_beats = 0
    count_fib = 0
    count_extrabeat = 0

    dict_cat = {}

    for index, val in enumerate(beatClassificationList):
        if index<=len(peaks):
            if val == "N":
                count_n += 1
            if val == "escape beat":
                count_escape_beats += 1
            if val == "ventricular premature beats":
                count_pvc += 1
            if val == "vf/vt":
                count_fib += 1
            if val == "atrial/nodal/supraventricular beat":
                count_extrabeat += 1

    dict_cat = {"cat_1":count_n,"cat_2":count_extrabeat,"cat_3":count_pvc,"cat_4":count_escape_beats,"cat_5":count_fib}

    return dict_cat

def countAnomalies2(beatClassificationList, peaks):
    count_n = 0
    count_pvc = 0
    count_escape_beats = 0
    count_fib = 0
    count_extrabeat = 0
    count_anomalies = 0
    count_tot_anomalies = 0
    
    anomalies_list_timing = {}
    anomalies_indexing = {}

    anomalies_indexing[0]={"cat":"cat_1", "index":0}
    anomalies_indexing[1]={"cat":"cat_1", "index":0}

    for index, val in enumerate(beatClassificationList):
        if index < len(beatClassificationList)-1:
            if val == "N":
                count_n += 1
                time = str(datetime.timedelta(seconds=peaks[index+2]/250))
                anomalies_indexing[index+2]={"cat":"cat_1", "index":peaks[index+2]}
                anomalies_list_timing[index+2] = {"event":"escape beat", "time":time}
            if val == "escape beat":
                anomalies_indexing[index+2]={"cat":"cat_4", "index":peaks[index+2]}
                count_tot_anomalies +=1
                count_escape_beats += 1
                count_anomalies +=1
                time = str(datetime.timedelta(seconds=peaks[index+2]/250))
                anomalies_list_timing[index+2] = {"event":"escape beat", "time":time}
            if val == "ventricular premature beats":
                count_pvc += 1
                count_anomalies +=1
                time = str(datetime.timedelta(seconds=peaks[index+2]/250))
                anomalies_list_timing[index+2] = {"event":"ventricular premature beats", "time":time}
                anomalies_indexing[index+2]={"cat":"cat_3", "index":peaks[index+2]}
                count_tot_anomalies +=1
            if val == "vf/vt":
                count_fib += 1
            if val == "atrial/nodal/supraventricular beat":
                # print("ATRIAL")
                # print(index)
                # print(peaks[index+2])
                count_extrabeat += 1
                count_anomalies +=1
                time = str(datetime.timedelta(seconds=peaks[index+2]/250))
                anomalies_list_timing[index+2] = {"event":"atrial/nodal/supraventricular beat", "time":time}
                anomalies_indexing[index+2]={"cat":"cat_2", "index":peaks[index+2]}
                count_tot_anomalies +=1

                """ print("HERE")
                print(print(peaks[index+2])) """

    categories = {}
    categories[0] = {"cat_1":count_n, "cat_2":count_extrabeat, "cat_3":count_pvc, "cat_4":count_escape_beats, "cat_5":count_fib}

    return categories, anomalies_list_timing, anomalies_indexing

def new_detect(nni, fs):

    beat_classified = []

    i = 0
    while i < len(nni)-3:
        beat_is = ""
        nni_section = nni[i:i+3]
        nni_1 = nni_section[0]
        nni_2 = nni_section[1]
        nni_3 = nni_section[2]

        nni1_classificaficated = ""
        nni2_classificaficated = "N"
        nni3_classificaficated = ""

        if nni_2 < 600 and 1.8*nni_2<nni_1:
            beat_is = "C1"
        
            if (nni_1 <700 and nni_2 < 700 and nni_3 < 700) or ((nni_1 + nni_2 + nni_3) < 1700):
                beat_is = "C2"

        if nni_1 > 1.15*nni_2 and nni_3>1.15*nni_2:
            beat_is = "ventricular premature beats"
            
        if nni_2*1.15 < nni_1 and 1.15*nni_2 < nni_3:
            beat_is = "atrial/nodal/supraventricular beat"

        if abs(nni_1-nni_2)<300 and (nni_1<800 or nni_2<800) and nni_3>1.2*mean(nni_1, nni_2):
            beat_is = "C4"

        if abs(nni_2-nni_3)< 300 and (nni_2<800 or nni_3<800) and nni_1>1.2*mean(nni_2, nni_3):
            beat_is = "C5"

        if (2200 < nni_2 < 3000) and (abs(nni_1-nni_2)< 200 or abs(nni_2-nni_3)< 200):
            beat_is = "C6"

        beat_classified.append(beat_is)        
        i+=1


def new_class(nni, fs):

    beat_classified = []
    i = 0
    while i < len(nni)-3:
        beat_is = ""
        nni_section = nni[i:i+3]
        nni_1 = nni_section[0]
        nni_2 = nni_section[1]
        nni_3 = nni_section[2]

        nni1_classificaficated = ""
        nni2_classificaficated = "N"
        nni3_classificaficated = ""

        # cat_1
        if nni_1>1.8*nni_2 and nni_2<600:
            if (nni_1 <0.7 and nni_2 < 0.7 and nni_3 < 0.7) or ((nni_1 + nni_2 + nni_3) < 1.7):
                beat_is = "vf/vt"
        
        # cat_2
        if nni_1 > 1.15*nni_2 and nni_3 > 1.15*nni_2 :
            beat_is = "ventricular premature beats"

        if abs(nni_1-nni_2)<0.3 and nni_1<0.8 and nni_2 < 0.8 and 1.2*mean(nni_1+nni_2)<nni_2:
            beat_is = "ventricular premature beats" # pvc couplets
        
        if abs(nni_2-nni_3)<0.3 and nni_2<0.8 and nni_3 < 0.8 and 1.2*mean(nni_2+nni_3)<nni_1:
            beat_is = "ventricular premature beats" # pvc couplets


        beat_classified.append(beat_is)        
        i+=1
    return beat_classified