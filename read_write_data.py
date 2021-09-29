import pandas as pd
import numpy as np
import os


def write_data(results_dict, out_loc, dataset):

    outfile = open(os.path.join(out_loc, dataset + ".txt"), "a")

    for k in results_dict.keys():

        outfile.write("Proportion of data used : "+str(k)+"\n")
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


def read_crop_data(input_loc):

    data = pd.read_csv(os.path.join(input_loc, "crop.csv"), header=0, sep="\t")
    data = data.replace('?', np.NaN)
    data = data.dropna()

    # Get the label column from the data
    labels = list(data['labels'].values)
    data.drop(['labels'], inplace=True, axis=1)

    # Subset the feature columns from the data
    data = np.array(data, dtype=float)

    # Cast labels to a numpy array
    labels = np.array(labels)

    print("Data shape: ", data.shape)

    return data, labels
