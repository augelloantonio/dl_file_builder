import numpy as np
from mit_processing.mit_reader import countAnnotationAnomaliesFromBeat, getAnnotationAsCategory, getOurClassificationAsCategory

#################
#
# Check Positive
#
#################
def checkPositive(ann, peaks, fs, time_window):
    realPeaks = []
    fakePositive = []
    i = 0
    lenght = 0
    if len(peaks) > len(ann):
        lenght = len(peaks)
        arr = peaks
        arr2 = ann
    else:
        lenght = len(ann)
        arr = ann
        arr2 = peaks

    for i in peaks:
        for n in ann:
            if i+(time_window*fs/1000) > n > i-(time_window*fs/1000):
                realPeaks.append(i)
    
    for i in peaks:
        if i not in realPeaks:
            fakePositive.append(i)

    #print("Fake +")
    print("fake + :" + str(len(fakePositive)))
    # print(fakePositive)
    return fakePositive

def returnRealPeaks(annotationSample, peaks, time_window, fs, ann):
    our_realPeaks = []
    ann_realPeaks = []
    annotation_symbol = []

    for i in peaks: 
        try:
            for n in annotationSample:
                if i+(time_window*fs/1000) > n > i-(time_window*fs/1000):
                    """ if n == 546792:
                        print("HERE")
                        print()
                        indexing = np.where(annotationSample == n)[0][0]
                        print() """
                    our_realPeaks.append(i)
                    ann_realPeaks.append(n)  
                    indexing = np.where(annotationSample == n)[0][0]
                    annotation_symbol.append(ann.symbol[indexing])
        except:
            pass   

    """ print()
    print("LENGHTS")
    print("symbols  " + str(len(ann.symbol)))
    print("our_realPeaks " + str(len(our_realPeaks)))
    print("ann_realPeaks " + str(len(ann_realPeaks)))
    print("annotationSample " + str(len(annotationSample))) 
    count = 0 """
    
    """ for a in range(1, len(ann_realPeaks)):
        try:
            index = np.where(annotationSample == ann_realPeaks[a])[0][0]
            print(index)
            count=index
            
            # print("a " + str(a))
            # print(index)
            #annotation_symbol.append(ann.symbol[index])
        except:
            pass  """
    # print("annotation_symbol " + str(len(annotation_symbol)))
    # print(annotation_symbol)
    # print()
        
    return our_realPeaks, ann_realPeaks, annotation_symbol

def checkValues(annotationSample, annotation_symbol, beat_classification, peaks, fs, time_window, cat_dict):
    
    l1 = getAnnotationAsCategory(annotation_symbol)
    l2 = beat_classification
    
    """ print("lenght")
    print(len(l1))
    print(len(l2)) """

    ann_1 = cat_dict['ann_1']
    ann_2 = cat_dict['ann_2']
    ann_3 = cat_dict['ann_3']
    ann_4 = cat_dict['ann_4']
    ann_5 = cat_dict['ann_5']

    for i in range(0, len(l1)):
        if i < len(l2):
            #print(i)
            try:
                if l1[i] != l2[peaks.index(peaks[i])]['cat']:
                    """ print("---")
                    print(i)
                    print("CAT")
                    print(l1[i])
                    print(l2[i])
                    print("peak")
                    print(annotationSample[i])
                    print(peaks[i])
                    print("PEAK FROM INDEX")
                    print(l2[peaks.index(peaks[i])])  """
                    # cat_1 
                if l1[i] == "cat_1":
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_1":
                        ann_1['1_1'] = ann_1['1_1'] + 1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_2":
                        ann_1['1_2'] = ann_1['1_2']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_3":
                        ann_1['1_3'] = ann_1['1_3']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_4":
                        ann_1['1_4'] = ann_1['1_4']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_5":
                        ann_1['1_5'] = ann_1['1_5']+1
                    
                    # cat_2
                if l1[i]  == "cat_2":
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_1":
                        ann_2['1_1'] = ann_2['1_1']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_2":
                        ann_2['1_2'] = ann_2['1_2']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_3":
                        ann_2['1_3'] = ann_2['1_3']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_4":
                        ann_2['1_4'] = ann_2['1_4']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_5":
                        ann_2['1_5'] = ann_2['1_5']+1

                    # cat_3
                if l1[i]  == "cat_3":
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_1":
                        ann_3['1_1'] = ann_3['1_1']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_2":
                        ann_3['1_2'] = ann_3['1_2']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_3":
                        ann_3['1_3'] = ann_3['1_3']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_4":
                        ann_3['1_4'] = ann_3['1_4']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_5":
                        ann_3['1_5'] = ann_3['1_5']+1

                    # cat_4
                if l1[i]  == "cat_4":
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_1":
                        ann_4['1_1'] = ann_4['1_1']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_2":
                        ann_4['1_2'] = ann_4['1_2']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_3":
                        ann_4['1_3'] = ann_4['1_3']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_4":
                        ann_4['1_4'] = ann_4['1_4']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_5":
                        ann_4['1_5'] = ann_4['1_5']+1

                    # cat_5
                if l1[i]  == "cat_5":
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_1":
                        ann_5['1_1'] = ann_5['1_1']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_2":
                        ann_5['1_2'] = ann_5['1_2']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_3":
                        ann_5['1_3'] = ann_5['1_3']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_4":
                        ann_5['1_4'] = ann_5['1_4']+1
                    if l2[peaks.index(peaks[i])]['cat'] == "cat_5":
                        ann_5['1_5'] = ann_5['1_5']+1
            except:
                pass
    dict_cat = {"ann_1":ann_1, "ann_2":ann_2,"ann_3":ann_3,"ann_4":ann_4,"ann_5":ann_5}

    # print(dict_cat)
    return dict_cat
    

def checkRealAnomaly(annotationSample, annotation_symbol, beat_classification, peaks, fs, time_window, cat_dict):

    symbols_as_cat = getAnnotationAsCategory(annotation_symbol)
    our_beat_classification_as_cat = beat_classification

    # FINO A QUI TUTTO OK

    realPeaks = []
    lenght = 0
    if len(peaks) > len(annotationSample):
        lenght = len(peaks)
        arr = peaks
        arr2 = annotationSample
    else:
        lenght = len(annotationSample)
        arr = annotationSample
        arr2 = peaks    

    count=0
    
    indexing = 0
    our_index = 0
    for i in peaks:
        try:
            for n in annotationSample:
                if i+(time_window*fs/1000) > n > i-(time_window*fs/1000):

                    indexing = np.where(annotationSample == n)[0][0]
                    our_index = peaks.index(i)+1

                    count = our_index 
                    countAnnotationAnomaliesFromBeat(symbols_as_cat[indexing], beat_classification[our_index], cat_dict) 
        except IndexError:
            pass
    return cat_dict

#################
#
# Check Negative
#
#################
# start from annotation and subtract number of real annotation from the presents
def checkNegative(ann, peaks, fs, time_window):
    fakePeaks = []
    fakeNegative = []

    # [[L5[l2 - 1] * sl1 for sl1, l3 in zip(l1, L3) for l2 in L2 if L4[l2 - 1] == l3] for l1 in L1]

    for i in ann:
        for n in peaks:
            if i+(time_window*fs/1000) > n > i-(time_window*fs/1000): #try with 95
                fakePeaks.append(i)

    for i in ann:
        if i not in fakePeaks:
            fakeNegative.append(i)

    # print("fake -")
    print("fake - :" + str(len(fakeNegative)))
    return fakeNegative


#################
#
# Check Rythm
#
#################
def checkRythm(annotation_index, annotation_rhytm, rpeaks):
    
    categorization_list = []
    categorization = {}
    i = 0
    while i < len(annotation_index)-1:
        values = np.where(np.logical_and(rpeaks>=annotation_index[i], rpeaks<=annotation_index[i+1]))
        peaks_idx=[]
        for idx in values[0]:
            peaks_idx.append(rpeaks[idx])
        categorization_list.append({"rythm":annotation_rhytm[i], "peaks":[i for i in peaks_idx]})
        i=i+1
    return categorization_list