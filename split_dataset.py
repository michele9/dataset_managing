# Use this script to pre-processing the dataset;
#
# First of all it merges all the houses including an appliance,
# then calculate mean and std for normalization (x-mean)/std and
# then it generates training, validation and test subsets
#
#
# Time | Unix | Aggregate | Appliance1 | Appliance2 | Appliance3 | Appliance4 | Appliance5 | Appliance6 | Appliance7 |..
# ----------------------------------------------------------------------------------------------------------------------
#   0  | 1    | 2         | 3          | 4          | 5          | 6          | 7          | 8          | 9          |..
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import time
import os
import pickle


def load(path, building, appliance, channel):
    # load csv
    file_name = path + 'CLEAN_House' + str(building) + '.csv'

    single_csv = pd.read_csv(file_name,
                             header=0,
                             names=['aggregate', appliance],
                             # index_col=0,
                             usecols=[2, channel+2],
                             dtype={'aggregate': int, "appliance": int},
                             # dtype=np.int32,
                             # engine='c',
                             na_filter=False,
                             parse_dates=True,
                             infer_datetime_format=True,
                             memory_map=True)

    return single_csv


def save_file(path, filename, variable):
    write = open(path+filename, "wb")
    pickle.dump(lengths, write)
    write.close()


start_time = time.time()

# CLEAN_REFIT_081116 path
path = '/media/michele/Dati/CLEAN_REFIT_081116/'
appliance_name = 'microwave'


params_appliance = {
    'kettle': {
        'windowlength': 599,
        'on_power_threshold': 2000,
        'max_on_power': 3998,
        'mean': 700,
        'std': 1000,
        's2s_length': 128,
        'houses': [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 19, 20],
        'channels': [8, 9, 9, 8, 7, 9, 9, 7, 6, 9, 5, 9],
        'test_house': 2,
        'validation_house': 5,
    },
    'microwave': {
        'windowlength': 599,
        'on_power_threshold': 200,
        'max_on_power': 3969,
        'mean': 500,
        'std': 800,
        's2s_length': 128,
        'houses': [2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 15, 17, 19],
        'channels': [5, 8, 8, 7, 6, 8, 6, 8, 5, 8, 7, 7, 4],
        'test_house': 19,
        'validation_house': 17,
    },
    'fridge': {
        'windowlength': 599,
        'on_power_threshold': 50,
        'max_on_power': 3323,
        'mean': 200,
        'std': 400,
        's2s_length': 512,
        'houses': [1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 15, 17, 19, 20],
        'channels': [1, 1, 2, 1, 1, 1, 1, 1, 4, 1, 1, 2, 1, 1],
        'test_house': 0,
        'validation_house': 0,
    },
    'dishwasher': {
        'windowlength': 599,
        'on_power_threshold': 10,
        'max_on_power': 3964,
        'mean': 700,
        'std': 1000,
        's2s_length': 1536,
        'houses': [5, 6, 7, 9, 10, 13, 16, 18, 20],
        'channels': [4, 3, 6, 4, 6, 4, 6, 6, 5],
        'test_house': 0,
        'validation_house': 0,
    },
    'washingmachine': {
        'windowlength': 599,
        'on_power_threshold': 20,
        'max_on_power': 3999,
        'mean': 400,
        'std': 700,
        's2s_length': 2000,
        'houses': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20],
        'channels': [5, 2, 6, 5, 3, 2, 5, 4, 3, 5, 3, 3, 5, 4, 5, 2, 4],
        'test_house': 20,
        'validation_house': 19,
    }
}


# Normalization parameters for the aggregate
aggregate_mean = 522
aggregate_std = 814
main_path = '/media/michele/Dati/myREFIT/' + appliance_name + '/'
save_path = main_path + appliance_name + '.csv'

# check if lengths of houses and channels are the same size
assert len(params_appliance[appliance_name]['houses']) == len(params_appliance[appliance_name]['channels'])

total_length = 0
lengths = []

print("\nPreparing dataset for:\n" + appliance_name + "\nfrom REFIT data. \n")
print("Parameters: ")
print("    houses: " + str(params_appliance[appliance_name]['houses']))
print("        number of houses: " + str(len(params_appliance[appliance_name]['houses'])))
print("    channels: " + str(params_appliance[appliance_name]['channels']))
print("    validation house: " + str(params_appliance[appliance_name]['validation_house']))
print("    test house: " + str(params_appliance[appliance_name]['test_house']))
print("\nStarting merge csv files...")


# -------------------------------------------- loading and merging -----------------------------------------------------
if not os.path.isfile(save_path):

    for idx in range(len(params_appliance[appliance_name]['houses'])):
        single_step_time = time.time()

        building = params_appliance[appliance_name]['houses'][idx]
        channel = params_appliance[appliance_name]['channels'][idx]

        # loading in chunks
        csv = load(path, building, appliance_name, channel)

        rows, columns = csv.shape

        total_length += rows
        lengths.append(rows)

        # saving the whole merged file
        if total_length <= 1:
            csv.to_csv(save_path, mode='a', index=False)
        else:
            csv.to_csv(save_path, mode='a', index=False, header=False)

        del csv

        print("    file {:d} of {:d} took {:.0f} s".format(idx+1,
                                                           len(params_appliance[appliance_name]['houses']),
                                                           time.time() - single_step_time))


save_file('./', 'lengths' + appliance_name + '.p', lengths)
save_file('./', 'total_lengths' + appliance_name + '.p', total_length)

save_path_tra = main_path + appliance_name + '_training_' + '.csv'
save_path_val = main_path + appliance_name + '_validation_' + 'H' + \
                str(params_appliance[appliance_name]['validation_house']) + '.csv'
save_path_test = main_path + appliance_name + '_test_' + 'H' + \
                 str(params_appliance[appliance_name]['test_house']) + '.csv'


# -------------------------------------- normalization and splitting ---------------------------------------------------
print("Normalization and splitting into train, validation and test...")
if not os.path.isfile(save_path_tra):

    if lengths == []:
        read_l = open("./lengths" + appliance_name + ".p", "rb")
        pickle.load(read_l)
        read_l.close()
        read_t = open("./total_lengths" + appliance_name + ".p", "rb")
        pickle.load(read_t)
        read_t.close()
        print("    Variable lengths and total_lengths loaded.")
    print("    Done. \n")

    print("    Total size of dataset is {:d}".format(total_length))

    temp = pd.read_csv(save_path,
                       index_col=False,
                       names=['aggregate', appliance_name],
                       dtype={'aggregate': float, appliance_name: float},
                       na_filter=False,
                       header=0,
                       memory_map=True)

    mean_agg_actual = int(temp['aggregate'].mean())
    std_agg_actual = int(temp['aggregate'].std())
    temp['aggregate'] = round((temp['aggregate'] - aggregate_mean) / aggregate_std, 5)

    temp[appliance_name] =\
        (temp[appliance_name] - params_appliance[appliance_name]['mean']) / params_appliance[appliance_name]['std']

    n_rows_test = sum(lengths[0:params_appliance[appliance_name]['houses']
                       .index(params_appliance[appliance_name]['test_house'])])

    n_rows_val = sum(lengths[0:params_appliance[appliance_name]['houses']
                      .index(params_appliance[appliance_name]['validation_house'])])

    # ------------------------------------------  saving splitted  -----------------------------------------------------
    test = temp.iloc[n_rows_test:n_rows_test+lengths[params_appliance[appliance_name]['houses']
                       .index(params_appliance[appliance_name]['test_house'])], :]
    print("    size of test set is {:d}".format(test.shape[0]))
    test.to_csv(save_path_test, index=False)
    del test

    val = temp.iloc[n_rows_val:n_rows_val + lengths[params_appliance[appliance_name]['houses']
                      .index(params_appliance[appliance_name]['validation_house'])], :]
    print("    size of validation set is {:d}".format(val.shape[0]))
    val.to_csv(save_path_val, index=False)
    del val

    train = temp.iloc[0:n_rows_val, :]
    print("    size of training set is {:d}".format(train.shape[0]))
    train.to_csv(save_path_tra, index=False)
    del train

    save_file('./parameters/', 'mean_agg.p', mean_agg_actual)
    save_file('./parameters/', 'std_agg.p', std_agg_actual)


print("    Mean and standard deviation values used are:")
print("    Mean = " + str(aggregate_mean) + " ," + "STD = " + str(aggregate_std))
print("    Mean = {:d}, STD = {:d}".format(aggregate_mean, aggregate_std))
print("    Mean and standard deviation values calculated are:")
print("    Mean = " + str(mean_agg_actual) + " ," + "STD = " + str(std_agg_actual))
print("    Mean = {:.6f}, STD = {:.6f}".format(mean_agg_actual, std_agg_actual))
print("    Done.")
print("    - whole merged file in: " + save_path)
print("    - training sequence in: " + save_path_tra)
print("    - validation sequence in: " + save_path_tra)
print("    - training sequence in: " + save_path_tra)

tot = int(int(time.time() - start_time) / 60)
print("\nTotal elapsed time: " + str(tot) + ' min')







# ------------------------------------------------  DROPPING  ----------------------------------------------------------

"""
    temp.drop(temp.index[n_rows_test:n_rows_test+lengths[buildings.index(test_build)]], inplace=True)
    temp.drop(temp.index[n_rows_val:n_rows_val+lengths[buildings.index(val_build)]], inplace=True)
    #save train
    temp.to_csv(save_path_norm)
    del temp
"""
# ----------------------------------------------------------------------------------------------------------------------
