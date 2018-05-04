import argparse



def remove_space(string):
    return string.replace(" ","")


def get_arguments():
    parser = argparse.ArgumentParser(description='Predict the appliance\
                                     give a trained neural network\
                                     for energy disaggregation -\
                                     network input = mains window;\
                                     network target = the states of\
                                     the target appliance.')
    parser.add_argument('--appliance_name',
                        type=remove_space,
                        default='kettle',
                        help='the name of target appliance')
    parser.add_argument('--datadir',
                        type=str,
                        default='/media/michele/Dati/myREFIT/',
                        help='this is the directory of the training samples')
    parser.add_argument('--batchsize',
                        type=int,
                        default=1000,
                        help='The batch size of training examples')
    parser.add_argument('--n_epoch',
                        type=int,
                        default=50,
                        help='The number of epoches.')
    parser.add_argument('--nosOfWindows',
                        type=int,
                        default=100,
                        help='The number of windows for prediction \
                            for each iteration.')
    parser.add_argument('--save_model',
                        type=int,
                        default=-1,
                        help='Save the learnt model:\
                        0 -- not to save the learnt model parameters;\
                        n (n>0) -- to save the model params every n steps;\
                        -1 -- only save the learnt model params\
                        at the end of training.')
    parser.add_argument('--test_type',
                        type=str,
                        default='test',
                        help='Type of the test set to load: \
                            test -- test on the proper test set;\
                            train -- test on a slice of the train set;\
                            uk -- test on UK_DALE (unseen scenrio).')
    parser.add_argument('--transfer',
                        type=bool,
                        default=False,
                        help='Using a pre-trained CNN:\
                                True -- do use a pre-trained CNN;\
                                False -- train the CNN.')
    parser.add_argument('--cnn',
                        type=str,
                        default='kettle',
                        help='Which CNN to load.')
    parser.add_argument('--gpus',
                        type=int,
                        default=-1,
                        help='Number of GPUs to use:\
                            n -- number of GPUs the system should use;\
                            -1 -- do not use any GPU.')
    parser.add_argument('--crop_dataset',
                        type=int,
                        default=None,
                        help='for debugging porpose should be helpful to crop the training dataset size')
    parser.add_argument('--ram',
                        type=int,
                        default=5*10**5,
                        help='Maximum number of rows of csv dataset can handle without loading in chunks')
    return parser.parse_args()


args = get_arguments()

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
        'test_house': 20,
        'validation_house': 19,
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
        'test_house': 20,
        'validation_house': 18,
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

print('Arguments: ')
print(args)
print('Parameters: ')
print(params_appliance[args.appliance_name])

