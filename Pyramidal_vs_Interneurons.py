# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 16:07:19 2022

@author: p.nazarirobati (p.nazarirobati@uleth.ca)


This code is find a roughly esimation of neurons type (Pyramidal vs interneurons)
Based on simple thresholding analysis of mean firing rate

Inputs:
    path_name: path address of epochs information file location
    spt_file: path address of spikes data file location

Variables:
    t_st: starting time (in NSMA format (0.1 ms))
    t_en: end time (in NSMA format (0.1 ms))
    nneu: number of recorded neurons
    sPC: array containing firing rate for each neuron (size: nneu x 1)

Outputs:
    neuType: array specifying each neuron type (size: nneu x 1)
        if neuType[i,0]==0:
            neuron is pyramidal  (it means that mean firing rate is less than 1 Hz)
        if neuType[i,0]==1:
            neuron is interneuron   (it means that mean firing rate is more than 5 Hz)
        if neuType[i,0]==10:(it means that mean firing rate is between 1-5 Hz)
            the algorithm cannot find the cell type



"""
### Importing packages
import numpy as np
import pickle
import neo
import quantities as pq
import pandas as pd
from spiketrain import spiketrain
from epochs_data import epochs_data
from elephant import statistics
import seaborn as sns
import matplotlib.pyplot as plt

################# MAIN CODE RUNNING ################
### file path location address
rats = ['rr5', 'rr6', 'rr7', 'rr8', 'rr9']

date_recording_rr5 = ['2015-04-14','2015-04-15','2015-04-16','2015-04-17','2015-04-18','2015-04-19','2015-04-20','2015-04-21','2015-04-22', '2015-04-23', '2015-04-24','2015-04-25', '2015-04-26', '2015-04-27', '2015-04-28']
date_recording_rr6 = ['2012-07-30','2012-07-31', '2012-08-01','2012-08-02', '2012-08-03', '2012-08-04', '2012-08-05', '2012-08-06', '2012-08-07', '2012-08-08']
date_recording_rr7 = ['2013-07-09','2013-07-10', '2013-07-13','2013-07-14', '2013-07-15', '2013-07-16', '2013-07-17', '2013-07-18', '2013-07-20', '2013-07-21', '2013-07-22', '2013-07-23', '2013-07-25']
date_recording_rr8 = ['2015-10-14','2015-10-15','2015-10-16','2015-10-17','2015-10-18','2015-10-19','2015-10-20','2015-10-21', '2015-10-22','2015-10-23','2015-10-24','2015-10-25','2015-10-26','2015-10-27','2015-10-28','2015-10-29','2015-10-30','2015-10-31','2015-11-01','2015-11-02']
date_recording_rr9 = ['2016-04-20','2016-04-21','2016-04-22','2016-04-23','2016-04-24','2016-04-25','2016-04-26','2016-04-27','2016-04-28','2016-04-29','2016-05-01','2016-05-02', '2016-05-03', '2016-05-04', '2016-05-05']

rat = rats[4]
dates = date_recording_rr9
rr7 = [1,2,5,6,7,8,9,10,12,13,14,15,17] # must be uncommented just for rr7
PyrInt = pd.DataFrame(columns=['Rat', 'date', 'nneu', 'Pyramidal', 'Interneuron', 'Unclassified'])


    
for idx, date in enumerate(dates):
        
    path_name = r"C:\Users\p.nazarirobati\Desktop\outputs\\"+ str(rat) + str("\\") + str (date)
    spt_file = r"C:\Users\p.nazarirobati\Desktop\\" + str(rat) + str("\\") + str(idx+1) + str(".pkl") # must be commented just for rat 7
    #spt_file = r"C:\Users\p.nazarirobati\Desktop\\" + str(rat) + str("\\") + str(rr7[idx]) + str(".pkl") # must be uncommented just for rr7
######### variables initialization
    spikes = spiketrain(spt_file)  
    nneu = len(spikes)

### Following variables are named and customized based on Mike reaching data (Ecekrt et al 2020)
    t_s1s = epochs_data(path_name)[2]
    t_s1e = epochs_data(path_name)[3]
    t_s2s = epochs_data(path_name)[4]
    t_s2e = epochs_data(path_name)[5]
    t_tks = epochs_data(path_name)[6]
    t_tke = epochs_data(path_name)[7]
### 
    spC=np.zeros((nneu,1))
    neuType = np.zeros((nneu,1))
        
    t_st = t_s1s # starting time should be initialized based on the data
    t_en = t_s2e # end time should be initialized based on the data

        #Time_binned = np.arange(t_st, t_en, 10000) # binned time to 1 sec intervals 

    for i in range(nneu):
        spikes[i] = [x for x in spikes[i] if ((x>=t_st) and (x<=t_en))]
    #if idx==11:
     #   spikes.pop(12)
    #elif idx==13:
     #  spikes.pop(1) 
      # spikes.pop(38) 
       #spikes.pop(49) 

    spT = [neo.SpikeTrain(spikes[i]*pq.ms, t_start = t_st*pq.ms, t_stop = t_en*pq.ms) for i in range(len(spikes))]   

    for i in range(len(spT)):
        spC[i,0] = statistics.mean_firing_rate(spT[i], t_start = t_st*pq.ms, t_stop = t_en*pq.ms) * 10000

#IQR = np.percentile(spC, 75) - np.percentile(spC, 25)
#h = 2 * IQR * (nneu)**(-0.3333)
#N_bins = (np.max(spC) - np.min(spC))/h


        #fig, ax = plt.subplots(1,1, figsize=(6,4))
        #sns.histplot(spC_df, bins=nneu, ax=ax)
        #ax.set_xlabel('Mean Firing Rate (Hz)', fontweight = 'bold')
        #ax.set_ylabel('Count', fontweight='bold')

        #fig.suptitle('Neurons Average Firing Rate_Rat4_day11', fontweight='bold')
 
    for n in range(nneu):
    
        if spC[n,0]>5:
            neuType[n,0]=1
        elif spC[n,0]<=1:
            neuType[n,0]=0
        else:
            neuType[n,0]=10
        
    PyramidalCells = np.where(neuType==0)[0]  
    InterneuronCells = np.where(neuType==1)[0]  
    UnclassifiedCells = np.where(neuType==10)[0]  
        
        
    PyrInt.loc[idx, 'Rat'] = rat 
    PyrInt.loc[idx, 'date'] = date 
    PyrInt.loc[idx, 'nneu'] = nneu  
    PyrInt.loc[idx, 'Pyramidal'] = len(PyramidalCells) 
    PyrInt.loc[idx, 'Interneuron'] = len(InterneuronCells) 
    PyrInt.loc[idx, 'Unclassified'] = len(UnclassifiedCells) 

PyrInt.to_csv('rr9_PyramidalInterneurons_len.csv')




        
    