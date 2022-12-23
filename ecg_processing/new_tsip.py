import datetime
from ecg_processing.utils import mean
import numpy as np
from math import isclose

def new_tsipouras(signal, nni, rpeaks, pulse):
    beatClassificationList = []

    for i in rpeaks:
        beatClassificationList.append("N")
    x = 0

    pulse = 0
    start_vf_loop = False
    
    for i in range(0, len(nni)-2):
        # the i iteration of the article = x 
        this_nni = [nni[i], nni[i+1], nni[i+2]]
        this_rr = "cat_2"
        vf_nni = []

        hearth_rythm = "normal"

        if nni[i+1] < 600 and nni[i+1]*1.8>nni[i]:
            start_vf_loop = True
                
        if start_vf_loop:
            x = i
            while start_vf_loop:
                if nni[x+1] < 600 and nni[x+1]*1.8>nni[x]:
                    beatClassificationList[x+1] = "ventricular premature beats"
                    vf_nni = [nni[x], nni[x+1], nni[x+2]]
                    
                    # Starts of VF (fribrillation/flutter)
                    if nni[x] < 700 and nni[x+1] < 700 and nni[x+2]<700 or (nni[x] + nni[x+1] + nni[x+2]) < 1700: #c2 
                        hearth_rythm = "VF"
                        pulse = pulse+1
                        print("VF")
                    else:
                        if pulse>=4:
                            print("FIBRILLATION")
                            start_fibrillation = datetime.timedelta(seconds=rpeaks[i+1]/fs)
                            end_fibrillation = datetime.timedelta(seconds=rpeaks[x+1]/fs)
                            print("VF Start: " + str(start_fibrillation) + " - VF Stop: " + str(end_fibrillation))
                        beatClassificationList[x+1] = "N"
                        pulse = 0
                    # x = x+3 # loop every 3 beats (sequencial 3 nni windows)
                    x = x+1 # loop every 3 beats (moving windows nni)
                else:
                    start_vf_loop = False
                    pulse = 0
        else:
            """ C3 or C4 or C5 """    
            if nni[i+1]*1.15 < nni[i] and nni[i+1]*1.15 < nni[i+2]: #C3
                beatClassificationList[i+1] = "ventricular premature beats" # CATEGORY 2
                # ISOLATED PVC
            if (abs(nni[i]-nni[i+1])<300) and (nni[i]<800 or nni[i+1]<800) and (nni[i+2]>1.2*mean(nni[i], nni[i+1])): #C4    
                beatClassificationList[i+1] = "ventricular premature beats" # CATEGORY 2
                # PVC COUPLET 
            if (abs(nni[i+1]-nni[i+2])<300) and ((nni[i+1]<800) or (nni[i+2]<800)) and (nni[i]>1.2*mean(nni[i+1], nni[i+2])): #C5 
                beatClassificationList[i+1] = "ventricular premature beats" # CATEGORY 2

    return beatClassificationList


def new_tsipouras_2(signal, nni, rpeaks, pulse, fs):
    beatClassificationList = []

    a = 0.9
    b = 0.9
    c = 1.5

    for i in rpeaks:
        beatClassificationList.append("N")
    x = 0

    pulse = 0
    threshold = 0
    beat_list_peaks = []
    start_vf_loop = False
    counter_anomalies_loop = 0
    peak_list = []
    
    for i in range(0, len(nni)-2):
        # the i iteration of the article = x 
        this_nni = [nni[i], nni[i+1], nni[i+2]]
        this_rr = "cat_2"
        vf_nni = []

        ecgANList = ["N", "N", "N"]
        hearth_rythm = "normal"

        if nni[i+1] < 500 and nni[i+1]*1.8>nni[i]:
            start_vf_loop = True
                
        if start_vf_loop:
            x = i
            
            while start_vf_loop:
                if x<len(nni)-3:
                    if nni[x+1] < 500 and nni[x+1]*2>nni[x]:
                        if nni[x+1] < 2000:
                            beatClassificationList[x+1] = "atrial/nodal/supraventricular beat"
                            vf_nni = [nni[x], nni[x+1], nni[x+2]]
                        
                        # Starts of VF (fribrillation/flutter)
                        if nni[x] < 500 and nni[x+1] < 500 and nni[x+2]<500 or (nni[x] + nni[x+1] + nni[x+2]) < 1500: #c2 
                            if nni[x+1] < 2000:
                                hearth_rythm = "VF"
                                pulse = pulse+1
                                beatClassificationList[x+1] = "atrial/nodal/supraventricular beat"
                        else:
                            if pulse>=4:
                                # print("FIBRILLATION")
                                start_fibrillation = datetime.timedelta(seconds=rpeaks[i+1]/fs)
                                end_fibrillation = datetime.timedelta(seconds=rpeaks[x+1]/fs)
                                # print("VF Start: " + str(start_fibrillation) + " - VF Stop: " + str(end_fibrillation))
                            beatClassificationList[x+1] = "N"
                            pulse = 0
                        #  x = x+3 # loop every 3 beats (sequencial 3 nni windows)
                        x = x+1 # loop every 3 beats (moving windows nni)
                    else:
                        start_vf_loop = False
                        i=x-pulse 
                        pulse = 0
                else:
                    start_vf_loop = False
                    i=x-pulse 
                    pulse = 0
        else:
            """ C3 or C4 or C5 """    
            if nni[i+1]*1.2 < nni[i] and nni[i+1]*1.2 < nni[i+2]: #C3
                if nni[i+2] > 200 and nni[i+2] < 2000:
                    # Isolated PVC
                    beatClassificationList[i+2] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    beat_list_peaks.append(rpeaks[i+2])

            if abs(nni[i]-nni[i+1])<300 and nni[i]<500 or nni[i+1]<500 and nni[i+2]>1.3*mean(nni[i], nni[i+1]): #C4
                # PVC Couplets
                if nni[i+2] > 200 and nni[i+2] < 2000:
                    is_equal_1 = isclose(nni[i+1], nni[i], abs_tol=1e-8)
                    if is_equal_1:
                        if nni[i+2] > nni[i+1]:
                            beatClassificationList[i+2] = "ventricular premature beats " # CATEGORY 3
                            beatClassificationList[i+1] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[0] = "ventricular premature beats" # CATEGORY 3
                            beat_list_peaks.append(rpeaks[i+2])

            if abs(nni[i+1]-nni[i+2])<300 and nni[i+1]<500 or nni[i+2]<500 and nni[i]>1.3*mean(nni[i+1], nni[i+2]): #C5 
                # PVC Couplet
                if nni[i+2] > 200 and nni[i+2] < 2000:
                    is_equal_2 = isclose(nni[i+1], nni[i+2], abs_tol=1e-8)
                    if is_equal_2:
                        if nni[i] > nni[i+1]:
                            beatClassificationList[i+2] = "ventricular premature beats" # CATEGORY 3
                            beatClassificationList[i+1] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[2] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[2] = "ventricular premature beats" # CATEGORY 3
                            beat_list_peaks.append(rpeaks[i+2])

            """
            PVC BEAT
            """               
            if threshold!=0:
                try:
                    if signal[rpeaks[i+2]][0] < threshold*0.4 and nni[i]+nni[i+2] >= 2*nni[i+1]:
                        if nni[i+2] > 200 and nni[i+2] < 2000:
                            beatClassificationList[i+2] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[1] = "ventricular premature beats" # CATEGORY 3 
                except:
                    pass

            """ if ecgANList[1] != "N":
                if threshold!=0:
                    if signal[rpeaks[i+2]][0] < threshold*0.8 and nni[i]+nni[i+2] >= 2*nni[i+1]:
                        beatClassificationList[i+2] = "ventricular premature beats" # CATEGORY 3
                        ecgANList[1] = "ventricular premature beats" # CATEGORY 3  """

            """ if threshold!=0:
                if signal[rpeaks[i]][0] < threshold*0.4:
                    beatClassificationList[i] = "ventricular premature beats" # CATEGORY 3
                    ecgANList[1] = "ventricular premature beats" # CATEGORY 3 """

            if nni[i+1] > c*nni[i]:
                if nni[i+1] > 200 and nni[i+1] < 2000:
                    ecgANList[1] = "escape beat" # CAT 4
                    beatClassificationList[i+1] = "escape beat" # CATEGORY 4

            try:
                if ecgANList[1] == "N":
                    peak_list.append(signal[rpeaks[i+2]])
                    threshold = np.mean(peak_list)
            except:
                pass
    
    return beatClassificationList




def original_tsipouras(signal, nni, rpeaks, pulse):
    beatClassificationList = []

    for i in rpeaks:
        beatClassificationList.append("N")
    x = 0

    pulse = 0
    start_vf_loop = False

    a = 0.9
    b = 0.9
    c = 1.5
    
    for i in range(0, len(nni)-2):
        # the i iteration of the article = x 
        this_nni = [nni[i], nni[i+1], nni[i+2]]
        this_rr = "cat_2"
        vf_nni = []

        hearth_rythm = "normal"

        if nni[i+1] < 500 and nni[i+2]>nni[i+1]:
            start_vf_loop = True
                
        if start_vf_loop:
            x = i
            while start_vf_loop:
                if nni[x+1] < 500 and nni[x+2]>nni[x+1]:
                    beatClassificationList[x+1] = "vf/vt"
                    vf_nni = [nni[x], nni[x+1], nni[x+2]]
                    
                    if nni[x] < 800 and nni[x+1] < 800 and nni[x+2]<800 or (nni[x] + nni[x+1] + nni[x+2]) < 1800: #c2 
                        hearth_rythm = "VF"
                        pulse = pulse+1
                        print("VF")
                    
                    else:
                        if pulse>=4:
                            print("FIBRILLATION")
                            start_fibrillation = datetime.timedelta(seconds=rpeaks[i+1]/fs)
                            end_fibrillation = datetime.timedelta(seconds=rpeaks[x+1]/fs)
                            print("VF Start: " + str(start_fibrillation) + " - VF Stop: " + str(end_fibrillation))
                        beatClassificationList[x+1] = "N"
                        pulse = 0
                        break
                else:
                    start_vf_loop = False
                    pulse = 0
                x = x+1

        # CAT 3 & CAT 2
        if nni[i+1] < nni[i]*a and nni[i] < b*nni[i+2]:
            if nni[i+1]+nni[i+2] < 2*nni[i]:
                beatClassificationList[i+1] = "atrial/nodal/supraventricular beat" # CAT 2
            else:
                beatClassificationList[i+1] = "ventricular premature beats" # CAT 3
                   
        # CAT 4
        if nni[i+1] > c*nni[i]:
            beatClassificationList[i+1] = "escape beat" # CAT 4
    
    return beatClassificationList


def beatsClassification4(signal, nni, rpeaks, pulse):
    """ 
    Latest beat classification algorithm wrote.
    ** args:
    - signal: signal average mean removed signal;
    - nni: nni list;
    - rpeaks: our detected rpeak list;
    - pulse: not really needed;
    - 

    """

    ecgAnomaliesList = []
    a = 0.9
    b = 0.9
    c = 1.5
    pulse = 0

    peak_list = []
    threshold = 0

    beat_list_peaks = []  
    mean_1_list = []
    mean_2_list = []

    mean_1 = 0
    mean_2 = 0

    counter_afib = 0

    ecgANTotal = []
    counter_anomalies_loop = 0

    for i in range(0, len(nni)-2):
        if i<len(rpeaks)+2:
            ecgAnomaliesList.append("N")
            ecgANList = ["N", "N", "N"]
            
            is_ventriculat_rythm = True
            nni = [int(x) for x in nni]

            if i < len(nni)-2:
                
                # print([nni[i], nni[i+1], nni[i+2]])

                """ C1 """
                if (nni[i+1] < 500) and (nni[i+2] < nni[i]): #c1
                    while is_ventriculat_rythm:  
                        # print("HERE AFIB")
                        # print(pulse)
                        # print(i)
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
                            
                        else:
                            # print("PULSE")
                            # print(pulse)
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
                                    ecgAnomaliesList[x] = "vt/vf" # CATEGORY 5

                """ C3 or C4 or C5 """    
                if nni[i+1]*1.2 < nni[i] and nni[i+1]*1.2 < nni[i+2]: #C3
            
                    ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    beat_list_peaks.append(rpeaks[i+2])
                    """ if (nni[i+1]*2 < nni[i+2]):
                        # print("HERE PVC C3")
                        ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                        ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                        beat_list_peaks.append(rpeaks[i+2]) """

                # if abs(nni[i]-nni[i+1])<200 and nni[i]<800 or nni[i+1]<800 and nni[i+2]>1.2*mean(nni[i], nni[i+1]): #C4
                if nni[i+2]>1.2*mean(nni[i], nni[i+1]): #C4
                        
                    # print(abs(nni[i]-nni[i+1]))
                    # print(abs(nni[i]-nni[i+1])<200 and nni[i]<1000)
                    ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    beat_list_peaks.append(rpeaks[i+2])
                    """ if (nni[i+1]*2 < nni[i+2]):
                        # print("HERE PVC C4")
                        ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                        ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                        beat_list_peaks.append(rpeaks[i+2]) """

                # if abs(nni[i+1]-nni[i+2])<200 and nni[i+1]<800 or nni[i+2]<800 and nni[i]>1.2*mean(nni[i+1], nni[i+2]): #C5 
                if nni[i]>1.2*mean(nni[i+1], nni[i+2]): #C5 
                    ecgAnomaliesList[-1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    ecgANList[1] = "atrial/nodal/supraventricular beat" # CATEGORY 2
                    beat_list_peaks.append(rpeaks[i+2])
                

                if nni[i+1] > c*nni[i] and (nni[i+1]*1.9 > nni[i+2]):
                    ecgANList[1] = "escape beat" # CAT 4

                """
                PVC BEAT
                """                
                if ecgANList[1] != "N":
                    if threshold!=0:
                        if signal[rpeaks[i+2]] < threshold*0.8 and nni[i]+nni[i+2] >= 2*nni[i+1]:
                            # print([nni[i], nni[i+1], nni[i+2]])
                            # print()
                            ecgAnomaliesList[-1] = "ventricular premature beats" # CATEGORY 3
                            ecgANList[1] = "ventricular premature beats" # CATEGORY 3
                            
            if counter_anomalies_loop == 0:
                ecgANTotal.append(ecgANList[1])
                counter_anomalies_loop += 1
            else:
                ecgANTotal.append(ecgANList[1])
            
            try:
                #if ecgANList[1] == "N":
                peak_list.append(signal[rpeaks[i+2]])
                threshold = np.mean(peak_list)
            except:
                pass
            
            mean_1 = np.mean(mean_1_list)
            mean_2 = np.mean(mean_2_list)

    return beatClassificationList 
