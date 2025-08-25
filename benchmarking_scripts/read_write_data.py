import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
import os


def write_data(results_dict, out_loc, dataset, key):

    outfile = open(os.path.join(out_loc, dataset + ".txt"), "a")
    outfile.write(key + "\t" + "ARI" + "\t" + "Accuracy" + "\t" + "Time" + "\t" + "Iterations" + "\n")

    for k in results_dict.keys():

        for res in results_dict[k]:
            outfile.write(str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2]) +  "\t" + str(res[3])
                          + "\t" + str(res[4]) + "\n")

        print("\n")

    outfile.close()
    print("Output file written to the disk")


def write_emdc_data(results_dict, out_loc, dataset):

    for k in results_dict.keys():

        outfile = open(os.path.join(out_loc, dataset + "_" + str(k) + ".txt"), "a")
        outfile.write("Clusters" + "\t" + "ARI" + "\t" + "Accuracy" + "\t" + "Time" + "\t" + "Iterations" + "\n")

        for res in results_dict[k]:
            outfile.write(str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2]) +  "\t" + str(res[3])
                          + "\t" + str(res[4]) + "\n")

        print("\n")

    outfile.close()
    print("Output file written to the disk")


# Wisconsin data
def read_wisconsin_data(input_loc):

    data = pd.read_csv(os.path.join(input_loc, "breastcancer.txt"), header=None, sep=",")
    data = data.replace('?', np.NaN)
    data = data.dropna()

    # Get the label column from the data
    labels = data.iloc[:, -1]

    # Subset the feature columns from the data
    data = data.iloc[:, 1:10]
    data = np.asarray(data, dtype=float)

    # Cast labels to a numpy array
    labels = np.asarray(labels)

    return data, labels


# def read_data(input_loc, raw):

#     if raw:
#         seperator = ","
#     else:
#         seperator = "\t"

#     data = pd.read_csv(input_loc, header=0, sep=seperator)
#     data = data.replace('?', np.NaN)
#     data = data.dropna()

#     # Get the label column from the data
#     labels = list(data['label'].values)
#     data.drop(['label'], inplace=True, axis=1)

#     # Subset the feature columns from the data
#     data = np.array(data, dtype=float)

#     # Cast labels to a numpy array
#     labels = np.array(labels)
#     print("Data shape: ", data.shape)
#     return data, labels


def read_data(data_name):

    data_id = {
        'wisconsin': 17,
        'census': 20,
        'magic': 159,
        'spambase': 94
        }

    file_loc = '/u/parishar/nobackup/DATASETS/geokmeans_data/real_data/'

    if data_name in ['wisconsin', 'spambase', 'magic']:
        
        base_data = fetch_ucirepo(id=data_id[data_name])
        data = base_data.data.features
        labels = base_data.data.targets

        if data_name == 'wisconsin':
            labels.loc[labels['Diagnosis'] == 'M', 'Diagnosis'] = 0
            labels.loc[labels['Diagnosis'] == 'B', 'Diagnosis'] = 1
        
        elif data_name == 'magic':
            labels.loc[labels['class'] == 'g', 'class'] = 0
            labels.loc[labels['class'] == 'h', 'class'] = 1

    elif data_name == "census":
        data = pd.read_csv(file_loc + 'census.txt')
        labels = data['incomelevel']
        data.drop(columns=['incomelevel'], inplace=True) 
        # print(data.head())

    elif data_name == "crop":
        data = pd.read_csv(file_loc + 'Crop_after_pca.csv', header=None)
        labels = pd.read_csv(file_loc + 'labels_Crop.csv', header=None)

    elif data_name == "ringnorm":
        data = pd.read_csv(file_loc + 'ringnorm.csv', header=None)
        labels = pd.read_csv(file_loc + 'labels_ringnorm.csv', header=None)


    # data = pd.read_csv(file_loc, header=None)
    # data = np.asarray(data, dtype=float)
    
    print("\nLoading Data: ", data_name)
    print("Data shape: ", data.shape, "Labels shape: ", labels.shape)
    print("\n")
    
    return np.array(data), np.array(labels).reshape(-1)


def read_labels(label_loc):
    labels = pd.read_csv(label_loc, header=None)
    labels = np.asarray(labels).flatten()
    return labels


def read_syn_data(data_name, type_data=""):
    

    if type_data == "scalability":
        input_loc = "/u/parishar/nobackup/DATASETS/scal_data/"
        data_loc = os.path.join(input_loc, data_name + "_points.csv")
        labels_loc = os.path.join(input_loc, data_name + "_labels.csv")

    elif type_data == "clusters":
        input_loc = "/u/parishar/nobackup/DATASETS/clustering_data/"
        data_loc = os.path.join(input_loc, str(data_name) + "_clusters.csv")
        labels_loc = os.path.join(input_loc, str(data_name) + "_labels.csv")
    
    elif type_data == "dimensions":
        input_loc = "/u/parishar/nobackup/DATASETS/dims_data/"
        data_loc = os.path.join(input_loc, data_name + "_dims.csv")
        labels_loc = os.path.join(input_loc, data_name + "_labels.csv")
    
    # print("Hello: ", labels_name)

    data = pd.read_csv(data_loc, header=None)
    data = np.asarray(data, dtype=float)

    labels = pd.read_csv(labels_loc, header=None)
    labels = np.asarray(labels).flatten()

    return data, labels


