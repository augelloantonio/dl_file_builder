import pandas as pd

def countAnnotationAnomalies(annotation):
    beatClassificationList_annotation = annotation.symbol

    char = ["+", "~", "|"]
    for i in beatClassificationList_annotation:
        if i in char: 
            beatClassificationList_annotation.remove(i)

    cat1_arr = ["N", "P", "f", "p", "Q", "s", "t", ".", "L", "R", "/", "F"]
    cat2_arr = ["A", "a", "J", "S"]
    cat3_arr = ["V"]
    cat4_arr = ["e", "j", "n", "E"]
    cat5_arr = ["[", "!", "]"]

    cat1_arr_count = 0
    cat2_arr_count = 0
    cat3_arr_count = 0
    cat4_arr_count = 0
    cat5_arr_count = 0

    isshalla = False

    for i in beatClassificationList_annotation:
        if i in cat1_arr:
            cat1_arr_count +=1
            isshalla = True
        if i in cat2_arr:
            cat2_arr_count +=1
            isshalla = True
        if i in cat3_arr:
            cat3_arr_count +=1
            isshalla = True
        if i in cat4_arr:
            cat4_arr_count +=1
            isshalla = True
        if i in cat5_arr:
            cat5_arr_count +=1
            isshalla = True
    
    dict_cat = {"cat_1":cat1_arr_count,"cat_2":cat2_arr_count,"cat_3":cat3_arr_count,"cat_4":cat4_arr_count,"cat_5":cat5_arr_count}

    return dict_cat


def countAnnotationAnomaliesFromBeat(annotation, our_beat, my_dict):
    ann_1 = my_dict['ann_1']
    ann_2 = my_dict['ann_2']
    ann_3 = my_dict['ann_3']
    ann_4 = my_dict['ann_4']
    ann_5 = my_dict['ann_5']

    # cat_1 
    if annotation == "cat_1":
        if our_beat == "cat_1":
            ann_1['1_1'] = ann_1['1_1'] + 1
        if our_beat == "cat_2":
            ann_1['1_2'] = ann_1['1_2']+1
        if our_beat == "cat_3":
            ann_1['1_3'] = ann_1['1_3']+1
        if our_beat == "cat_4":
            ann_1['1_4'] = ann_1['1_4']+1
        if our_beat == "cat_5":
            ann_1['1_5'] = ann_1['1_5']+1
    
    # cat_2
    if annotation == "cat_2":
        if our_beat == "cat_1":
            ann_2['1_1'] = ann_2['1_1']+1
        if our_beat == "cat_2":
            ann_2['1_2'] = ann_2['1_2']+1
        if our_beat == "cat_3":
            ann_2['1_3'] = ann_2['1_3']+1
        if our_beat == "cat_4":
            ann_2['1_4'] = ann_2['1_4']+1
        if our_beat == "cat_5":
            ann_2['1_5'] = ann_2['1_5']+1

    # cat_3
    if annotation == "cat_3":
        if our_beat == "cat_1":
            ann_3['1_1'] = ann_3['1_1']+1
        if our_beat == "cat_2":
            ann_3['1_2'] = ann_3['1_2']+1
        if our_beat == "cat_3":
            ann_3['1_3'] = ann_3['1_3']+1
        if our_beat == "cat_4":
            ann_3['1_4'] = ann_3['1_4']+1
        if our_beat == "cat_5":
            ann_3['1_5'] = ann_3['1_5']+1

    # cat_4
    if annotation == "cat_4":
        if our_beat == "cat_1":
            ann_4['1_1'] = ann_4['1_1']+1
        if our_beat == "cat_2":
            ann_4['1_2'] = ann_4['1_2']+1
        if our_beat == "cat_3":
            ann_4['1_3'] = ann_4['1_3']+1
        if our_beat == "cat_4":
            ann_4['1_4'] = ann_4['1_4']+1
        if our_beat == "cat_5":
            ann_4['1_5'] = ann_4['1_5']+1

    # cat_5
    if annotation == "cat_5":
        if our_beat == "cat_1":
            ann_5['1_1'] = ann_5['1_1']+1
        if our_beat == "cat_2":
            ann_5['1_2'] = ann_5['1_2']+1
        if our_beat == "cat_3":
            ann_5['1_3'] = ann_5['1_3']+1
        if our_beat == "cat_4":
            ann_5['1_4'] = ann_5['1_4']+1
        if our_beat == "cat_5":
            ann_5['1_5'] = ann_5['1_5']+1

    dict_cat = {"ann_1":ann_1, "ann_2":ann_2,"ann_3":ann_3,"ann_4":ann_4,"ann_5":ann_5}

    return dict_cat

def getAnnotationAsCategory(annotation_symbol):
    """
    Conver annotation in category used to validate our found beats
    """
    cat = []

    count = 0

    """ char = ["+", "~", "|", "Q"]
    for i in annotation_symbol:
        if i in char: 
            annotation_symbol.remove(i) """

    cat1_arr = ["+", "Q", "N", "P", "f", "p", "s", "t", ".", "L", "R", "/",  "F"]
    cat2_arr = ["A", "a", "J", "S"]
    cat3_arr = ["V"]
    cat4_arr = ["e", "j", "n", "E"]
    cat5_arr = ["[", "!", "]"]

    for i in annotation_symbol:
        count += 1
        if i in cat1_arr:
            cat.append("cat_1")
        if i in cat2_arr:
            cat.append("cat_2")
        if i in cat3_arr:
            cat.append("cat_3")
        if i in cat4_arr:
            cat.append("cat_4")
        if i in cat5_arr:
            cat.append("cat_5")
        """ if i not in cat1_arr and i not in cat2_arr and i not in cat3_arr and i not in cat4_arr and i not in cat5_arr:
            print(i) """
    return cat


def getOurClassificationAsCategory(our_classification):
    cat = []

    print("LEN OUR CLASSIFICATION IN getOurClassificationAsCategory")
    print(len(our_classification))

    # INSERT
    our_classification.insert(0, "N")
    # our_classification.insert(0, "N")
    # our_classification.insert(0, "N")

    for index, val in enumerate(our_classification):
        if val == "N":
            cat.append("cat_1")
        if val == "escape beat":
            cat.append("cat_4")
        if val == "ventricular premature beats":
            cat.append("cat_3")
        if val == "vf/vt":
            cat.append("cat_5")
        if val == "atrial/nodal/supraventricular beat":
            cat.append("cat_2")
        
    return cat