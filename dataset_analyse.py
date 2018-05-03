#
#
# MD

from dataset_managing.Arguments import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

appliance = args.appliance_name
print(appliance)

save_path_tra = '/media/michele/Dati/myREFIT/' + appliance + '/' + appliance + '_training_' + '.csv'
save_path_val = '/media/michele/Dati/myREFIT/' + appliance + '/' + appliance + '_validation_H17' + '.csv'
save_path_test = '/media/michele/Dati/myREFIT/' + appliance + '/' + appliance + '_test_H19' + '.csv'

chunksize = 4 * 10 ** 6

for idx, chunk in enumerate(pd.read_csv(save_path_tra,
                                        # index_col=False,
                                        names=['aggregate', appliance],
                                        # usecols=[1, 2],
                                        # iterator=True,
                                        skiprows=15 * 10 ** 6,
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
        ax1.set_title('{:}'.format(save_path_tra), fontsize=14, fontweight='bold',
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
