#
#
# MD

from dataset_managing.Arguments import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



path = '/media/michele/Dati/CLEAN_REFIT_081116/'

# Change house number from here
building = 'House6'


filename = path + 'CLEAN_' + building + '.csv'

# Number of sample to plot
chunksize = 5*10**5



for idx, chunk in enumerate(pd.read_csv(filename,
                                        # index_col=False,
                                        # names=['aggregate', application],
                                        # usecols=[1, 2],
                                        # iterator=True,
                                        chunksize=chunksize,
                                        header=0
                                        )):


    fig = plt.figure(num='Figure {:}'.format(idx))
    ax1 = fig.add_subplot(111)

    ax1.plot(chunk['Aggregate'])
    ax1.plot(chunk['Appliance1'])
    ax1.plot(chunk['Appliance2'])
    #ax1.plot(chunk['Appliance3'])
    #ax1.plot(chunk['Appliance4'])
    #ax1.plot(chunk['Appliance5'])
    #ax1.plot(chunk['Appliance6'])
    #ax1.plot(chunk['Appliance7'])
    #ax1.plot(chunk['Appliance8'])
    #ax1.plot(chunk['Appliance9'])


    ax1.set_title('{:}'.format(filename), fontsize=14, fontweight='bold',
                  # y=1.08
                  )
    ax1.set_ylabel('Power [W]')
    ax1.set_xlabel('samples')
    ax1.legend(['aggregate', 'appliance'])
    ax1.grid()

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show(fig)

    del chunk
