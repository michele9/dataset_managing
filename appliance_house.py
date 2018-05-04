from dataset_managing.Arguments import *
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd

"""
kettle
        'houses': [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 19, 20],
        'channels': [8, 9, 9, 8, 7, 9, 9, 7, 6, 9, 5, 9],

microwave
        'houses': [2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 15, 17, 19],
        'channels': [5, 8, 8, 7, 6, 8, 6, 8, 5, 8, 7, 7, 4],


fridge
        'houses': [1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 15, 17, 19, 20],
        'channels': [1, 1, 2, 1, 1, 1, 1, 1, 4, 1, 1, 2, 1, 1],

dishwasher
        'houses': [5, 6, 7, 9, 10, 13, 16, 18, 20],
        'channels': [4, 3, 6, 4, 6, 4, 6, 6, 5],

washingmachine
        'houses': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20],
        'channels': [5, 2, 6, 5, 3, 2, 5, 4, 3, 5, 3, 3, 5, 4, 5, 2, 4],
"""

path = '/media/michele/Dati/CLEAN_REFIT_081116/'

appliance = 'fridge'

house = 6

# Looking for the selected test set
for filename in os.listdir(path):
    if str(house) in filename.upper():
        actual_filename = filename

print('file: ' + actual_filename)


# Number of sample to plot
chunksize = 1*10**6

print('AAA: ' + str(params_appliance[appliance]['houses'].index(house)))

for idx, chunk in enumerate(pd.read_csv(path + actual_filename,
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
    label = params_appliance[appliance]['channels'][params_appliance[appliance]['houses'].index(house)]
    ax1.plot(chunk['Appliance{}'.format(label)])


    ax1.set_title('{:}'.format(actual_filename), fontsize=14, fontweight='bold',
                  # y=1.08
                  )
    ax1.set_ylabel('Power [W]')
    ax1.set_xlabel('samples')
    ax1.legend(['aggregate', 'Appliance{}'.format(label)])
    ax1.grid()

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show(fig)

    del chunk
