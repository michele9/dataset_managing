#
#
# MD

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


path = '/media/michele/Dati/CLEAN_REFIT_081116/'

# Change house number from here
building = 'House20'


filename = path + 'CLEAN_' + building + '.csv'

# Number of sample to plot
chunksize = 5*10**5



for idx, chunk in enumerate(pd.read_csv(filename,
                                        # index_col=False,
                                        # names=['aggregate', application],
                                        # usecols=[1, 2],
                                        # iterator=True,
                                        chunksize=chunksize,
                                        # header=0
                                        )):

    fig2 = plt.figure()
    plt.plot(chunk['Aggregate'])
    plt.plot(chunk['Appliance4'])
    #plt.plot(chunk['Appliance2'])
    #plt.plot(chunk['Appliance3'])
    #plt.plot(chunk['Appliance4'])
    #plt.plot(chunk['Appliance5'])
    #plt.plot(chunk['Appliance6'])
    #plt.plot(chunk['Appliance7'])
    #plt.plot(chunk['Appliance8'])
    #plt.plot(chunk['Appliance9'])
    plt.grid()
    plt.show(fig2)
