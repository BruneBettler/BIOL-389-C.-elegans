# Last Modified April 2024
# Brune Bettler

import pandas as pd
import numpy as np

'''
H202 Addition Time: 
WT0: 19.31 sec
WT1: 7.72 sec
WT2: 25.35 sec
WT3: 25.61 sec
'''

WT_H202_addTime = [19.31, 7.72, 25.35, 25.61]
MT_H202_addTime = [37.17,34.78,33.78]

def get_pre_post_H202(peak_data, worm_id):
    H_addTime = [19.31, 7.72, 25.35, 25.61][worm_id]
    pre = []
    post = []

    for E, R in peak_data:
        if E < H_addTime and R < H_addTime:
            pre.append([E, R])
        else:
            post.append([E,R])

    return np.array(pre), np.array(post)

def get_all_ER_times(data, start=1, save=False,name=None): # start = 100.0 for WT and 1.0 for MT
    csv_data = pd.read_csv(data)

    """
    peak type/annotation = column 3
    peak value = column 2 
    begin = column 7
    end = column 8  
    """
    all_ER_tuples = []
    # go through all rows and record the peak times of all E and R spikes
    row_num = len(csv_data.iloc[1:, 2])
    prev = None
    prev_val = 0.0
    curr_val = 0.0
    first = False

    for curr_row in range(start,row_num+1):
        annot = csv_data.iloc[curr_row, 3]
        peak = float(csv_data.iloc[curr_row, 2]) / 1000.0
        curr_val = float(csv_data.iloc[curr_row,6])
        if not first:
            if peak >= start:
                first = True
            else: continue
        if curr_val < 5.0:
            continue

        if annot == 'E':
            if prev == 'E': # there is an error with the annotation and it was split into two
                # check its sum value and record only the peak value with greatest amplitude
                if prev_val < float(csv_data.iloc[curr_row,6]):
                    E_peak = peak
                    prev = 'E'
                    prev_val = float(csv_data.iloc[curr_row,6])
            else:
                E_peak = peak
                prev_val = float(csv_data.iloc[curr_row, 6])
                prev = 'E'

        elif annot == 'R':
            if prev == 'R': # there is an error with the annotation and it was split into two
                # check its sum value and record only the peak value with greatest amplitude
                if prev_val < float(csv_data.iloc[curr_row,6]):
                    all_ER_tuples[-1][1] = peak
                    prev = 'R'
                    prev_val = float(csv_data.iloc[curr_row,6])
            elif prev == 'E':
                R_peak = peak
                prev = 'R'
                all_ER_tuples.append([E_peak, R_peak])
                prev_val = float(csv_data.iloc[curr_row, 6])

    if save:
        np.save('data/'+name+'.npy', all_ER_tuples)
    # all_ER_tuples has the following format: [[E_peak, R_peak], [E_peak, R_peak], ...]
    return np.array(all_ER_tuples)

def get_all_ER_lengths(ER_times_array):
    length_array = []
    for E, R in ER_times_array:
        length = R - E
        length_array.append(length)

    return np.array(length_array)

def get_all_RE_distances(ER_times_array):
    RE_distances = []
    first = True
    prev_R = 0.0
    for E, R in ER_times_array:
        if first: # this is first ER pump
            prev_R = R
            first = False
        else: # these are all other ER pumps
            distance = E - prev_R
            prev_R = R
            RE_distances.append(distance)

    return np.array(RE_distances)


if __name__ == '__main__':
    print("test here")




