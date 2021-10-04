import pandas as pd
import numpy as np
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


def read_data(input_loc, raw):

    if raw:
        seperator = ","
    else:
        seperator = "\t"

    data = pd.read_csv(input_loc, header=0, sep=seperator)
    data = data.replace('?', np.NaN)
    data = data.dropna()
    # print(data.columns)

    # Get the label column from the data
    labels = list(data['label'].values)
    data.drop(['label'], inplace=True, axis=1)

    # Subset the feature columns from the data
    data = np.array(data, dtype=float)

    # Cast labels to a numpy array
    labels = np.array(labels)
    print("Data shape: ", data.shape)
    return data, labels


