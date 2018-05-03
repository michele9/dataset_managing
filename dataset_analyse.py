#
#
# MD

from dataset_managing.Arguments import *
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd

appliance = args.appliance_name

dataset = 'training'
#dataset = 'test'
#dataset = 'validation'

# Looking for the selected test set
for filename in os.listdir(args.datadir + appliance):
    if dataset.upper() in filename.upper():
        test_filename = filename

print(test_filename)

chunksize = 4 * 10 ** 6

for idx, chunk in enumerate(pd.read_csv(args.datadir + appliance + '/' + test_filename,
                                        # index_col=False,
                                        names=['aggregate', appliance],
                                        # usecols=[1, 2],
                                        # iterator=True,
                                        #skiprows=15 * 10 ** 6,
                                        chunksize=chunksize,
                                        header=0
                                        )):

    if True:

        # de-normalization
        #chunk['aggregate'] = chunk['aggregate'] * 822 + 522
        #chunk[appliance] = chunk[appliance] * params_appliance[args.appliance_name]['std'] \
         #                  + params_appliance[args.appliance_name]['mean']

        fig = plt.figure(num='Figure {:}'.format(idx))
        ax1 = fig.add_subplot(111)

        ax1.plot(chunk['aggregate'])
        ax1.plot(chunk[appliance])

        ax1.grid()
        ax1.set_title('{:}'.format(test_filename), fontsize=14, fontweight='bold',
                      #y=1.08
                      )
        ax1.set_ylabel('Power normalized')
        ax1.set_xlabel('samples')
        ax1.legend(['aggregate', appliance])

        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show(fig)

        #plt.close()

        del chunk
