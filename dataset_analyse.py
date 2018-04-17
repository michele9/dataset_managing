#
#
# MD


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

appliance = 'microwave'

save_path_tra = '/media/michele/Dati/myREFIT/microwave/' + appliance + '_training_' + '.csv'
save_path_val = '/media/michele/Dati/myREFIT/microwave/' + appliance + '_validation_H17' + '.csv'
save_path_test = '/media/michele/Dati/myREFIT/microwave/' + appliance + '_test_H19' + '.csv'

chunksize = 10 ** 6

for idx, chunk in enumerate(pd.read_csv(save_path_test,
                                        # index_col=False,
                                        # names=['aggregate', application],
                                        # usecols=[1, 2],
                                        # iterator=True,
                                        chunksize=chunksize,
                                        # header=0
                                        )):

    if True:


        #chunk['aggregate'] = chunk['aggregate'] * 822 + 522
        #chunk[appliance] = chunk[appliance] * 1000 + 700

        fig2 = plt.figure()
        plt.plot(chunk['aggregate'])
        plt.plot(chunk[appliance])


        plt.show(fig2)
        #plt.close()
