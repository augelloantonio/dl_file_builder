import wfdb
import numpy as np 

def loadSample(path):
    fileList = []
    for filename in os.listdir("/Users/antonioaugello/Desktop/projects/ecg_analisys/data/mit/converted/"):
        fileList.append(filename)
    for f in listFile:
        filename = str(f)
        record = wfdb.rdrecord('mit_regular/' + filename)

        f = open("data/sinus_mit/" + str(filename) + ".txt", "w+")
        for i in record.p_signal:
            f.write(str(i[0]) + "\n")
    return fileList

def loadAnnotationSample(filename):
    #ANNOTATIONS

    # file = filename[:12]
    file = filename[9:-8]
    
    #print(file)

    annotation = wfdb.rdann('/Users/antonioaugello/Desktop/projects/ecg_analisys/data/mit-bih-arrhythmia-database-1.0.0/' + file, 'atr')
    
    # annotation = wfdb.rdann('/Users/antonioaugello/Desktop/projects/ecg_analisys/mit_regular/' + file, 'atr')

    ann = annotation.sample

    return ann

def loadAnnotationSampleFromPath(path, filename):
    #ANNOTATIONS

    file = filename
    
    annotation = wfdb.rdann(path + file, 'atr')
    print(annotation)
    
    ann = annotation.sample

    return ann

def loadAnnotationSampleFromPath(path, filename):
    #ANNOTATIONS

    file = filename
    
    anno = wfdb.rdann(path + file, 'atr')
    anno = np.unique(anno.sample[np.in1d(anno.symbol, ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?'])])

    return anno

def loadAnnotationSampleFromPathforVFDB(path, filename):
    #ANNOTATIONS

    file = filename
    
    anno = wfdb.rdann(path + file, 'atr')
    ann_rythm = [str(i).replace('\x00','').replace('(','') for i in anno.aux_note]
    anno = np.unique(anno.sample[np.in1d(ann_rythm, ['AFIB', 'ASYS', 'BI', 'HGEA', 'N', 'NSR', 'NOD', 'SVTA', 'VER', 'VF', 'VFIB', 'VFL', 'VT'])])
    
    return anno, ann_rythm

def loadAnnotationFromPath(path, filename):
    #ANNOTATIONS

    file = filename
    # HERE THE SAMPFROM SAMPTO
    anno = wfdb.rdann(path + file, 'atr')
    """ anno = wfdb.rdann(path + file, 'atr')
    anno = np.unique(anno.sample[np.in1d(anno.symbol, ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?'])])
    """
    return anno

def loadAnnotationSampleFromPathSinus(path, filename, counter, sampfrom, sampTo):
    #ANNOTATIONS

    file = filename
    
    annotation = wfdb.rdann(path + file, 'atr', sampfrom=sampfrom, sampto=sampTo)
    
    ann = annotation.sample

    if sampTo>sampTo-sampfrom:
        ann = [i-((sampTo-sampfrom)*counter) for i in ann]

    return ann