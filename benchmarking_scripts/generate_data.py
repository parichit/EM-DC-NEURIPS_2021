import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from read_write_data import *


parent_dir = os.path.dirname(os.getcwd())
input_loc = os.path.join(parent_dir, "datasets", "raw_data")
clus_out_loc = os.path.join(parent_dir, "datasets", "clustering_data")
dims_out_loc = os.path.join(parent_dir, "datasets", "dimensionality_data")
scal_out_loc = os.path.join(parent_dir, "datasets", "scalability_data")


# PCA for capturing the PCs with most variance
def do_pca(dataset, n_comp, labels):

    pca = PCA(n_components=n_comp)
    ss = StandardScaler()
    dataset = ss.fit_transform(dataset)
    principalComponents = pca.fit_transform(dataset)

    if labels is not "":
        temp = pd.DataFrame(principalComponents)
        temp["label"] = labels
        return temp

    pc_esc = np.array(pd.DataFrame(data=principalComponents))
    return pc_esc


# Read the original data
raw_data, orig_labels = read_data(os.path.join(input_loc, "WinnipegDataset.txt"), True)


# Function to create the data for clustering experiments
def create_clustering_data(raw_data, orig_labels):

    """
        Create the clustering data from the raw
        cropland mapping dataset.

        For clustering experiments:
        The number of dimensions after PCA are fixed at 10.
    """
    out_data = pd.DataFrame(raw_data[np.where(orig_labels == 1)[0].tolist(), :])
    out_data = out_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 3)[0].tolist(), :]))
    out_data = out_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 4)[0].tolist(), :]))
    out_data = out_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 5)[0].tolist(), :]))
    out_data = out_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 6)[0].tolist(), :]))

    out_labels = orig_labels[np.where(orig_labels == 1)[0].tolist()].tolist()
    out_labels += orig_labels[np.where(orig_labels == 3)[0].tolist()].tolist()
    out_labels += orig_labels[np.where(orig_labels == 4)[0].tolist()].tolist()
    out_labels += orig_labels[np.where(orig_labels == 5)[0].tolist()].tolist()
    out_labels += orig_labels[np.where(orig_labels == 6)[0].tolist()].tolist()

    out_data = do_pca(out_data, 10, "")

    # print(out_data.shape, len(out_labels))
    out_data["label"] = out_labels

    # print(out_data.shape, "\n", out_data.head)
    out_data.to_csv(os.path.join(clus_out_loc, "crop.csv"), index=False, sep="\t")

    print("Saved clustering data to disk at: ", clus_out_loc)
    return None


# Uncomment below function call to overwrite the existing data.
# create_clustering_data(raw_data, orig_labels)


def create_scal_data(raw_data, orig_labels):

    """
    Create the scalability data from the raw
    cropland mapping dataset.

    The number of dimensions after PCA are fixed at 30
    Note: beyond 20 dimensions the PCs don't capture much variance.
    """

    raw_data = do_pca(raw_data, 30, "")

    # 100k
    red_data = pd.DataFrame(raw_data[np.where(orig_labels == 1)[0].tolist()[1:20000], :])
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 3)[0].tolist()[1:20000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 4)[0].tolist()[1:20000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 5)[0].tolist()[1:20000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 6)[0].tolist()[1:20000], :]))

    out_labels = orig_labels[np.where(orig_labels == 1)[0].tolist()[1:20000]].tolist()
    out_labels += (orig_labels[np.where(orig_labels == 3)[0].tolist()[1:20000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 4)[0].tolist()[1:20000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 5)[0].tolist()[1:20000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 6)[0].tolist()[1:20000]]).tolist()

    red_data["label"] = out_labels

    # print(out_data.shape, "\n", out_data.head)
    red_data.to_csv(os.path.join(scal_out_loc, "crop_100.csv"), index=False, sep="\t")
    print("Data for 100k points saved at: ", scal_out_loc)

    # 150k
    red_data = pd.DataFrame(raw_data[np.where(orig_labels == 1)[0].tolist()[1:30000], :])
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 3)[0].tolist()[1:30000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 4)[0].tolist()[1:30000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 5)[0].tolist()[1:30000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 6)[0].tolist()[1:30000], :]))

    out_labels = orig_labels[np.where(orig_labels == 1)[0].tolist()[1:30000]].tolist()
    out_labels += (orig_labels[np.where(orig_labels == 3)[0].tolist()[1:30000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 4)[0].tolist()[1:30000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 5)[0].tolist()[1:30000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 6)[0].tolist()[1:30000]]).tolist()

    red_data["label"] = out_labels

    # print(out_data.shape, "\n", out_data.head)
    red_data.to_csv(os.path.join(scal_out_loc, "crop_150.csv"), index=False, sep="\t")
    print("Data for 150k points saved at: ", scal_out_loc)

    # 200k
    red_data = pd.DataFrame(raw_data[np.where(orig_labels == 1)[0].tolist()[1:36000], :])
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 3)[0].tolist()[1:41000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 4)[0].tolist()[1:41000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 5)[0].tolist()[1:41000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 6)[0].tolist()[1:41000], :]))

    out_labels = orig_labels[np.where(orig_labels == 1)[0].tolist()[1:36000]].tolist()
    out_labels += (orig_labels[np.where(orig_labels == 3)[0].tolist()[1:41000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 4)[0].tolist()[1:41000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 5)[0].tolist()[1:41000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 6)[0].tolist()[1:41000]]).tolist()

    red_data["label"] = out_labels

    # print(out_data.shape, "\n", out_data.head)
    red_data.to_csv(os.path.join(scal_out_loc, "crop_200.csv"), index=False, sep="\t")
    print("Data for 200k points saved at: ", scal_out_loc)

    # 250k
    red_data = pd.DataFrame(raw_data[np.where(orig_labels == 1)[0].tolist()[1:38000], :])
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 3)[0].tolist()[1:53000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 4)[0].tolist()[1:53000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 5)[0].tolist()[1:53000], :]))
    red_data = red_data.append(pd.DataFrame(raw_data[np.where(orig_labels == 6)[0].tolist()[1:53000], :]))

    out_labels = orig_labels[np.where(orig_labels == 1)[0].tolist()[1:38000]].tolist()
    out_labels += (orig_labels[np.where(orig_labels == 3)[0].tolist()[1:53000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 4)[0].tolist()[1:53000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 5)[0].tolist()[1:53000]]).tolist()
    out_labels += (orig_labels[np.where(orig_labels == 6)[0].tolist()[1:53000]]).tolist()

    red_data["label"] = out_labels

    # print(out_data.shape, "\n", out_data.head)
    red_data.to_csv(os.path.join(scal_out_loc, "crop_250.csv"), index=False, sep="\t")
    print("Data for 250k points saved at: ", scal_out_loc)

    # 320k
    raw_data = pd.DataFrame(raw_data)
    raw_data['label'] = orig_labels

    # print(out_data.shape, "\n", out_data.head)
    raw_data.to_csv(os.path.join(scal_out_loc, "crop_320.csv"), index=False, sep="\t")
    print("Data for 320k points saved at: ", scal_out_loc)

    print("Saved scalability data to disk at: ", scal_out_loc)
    return None


# Uncomment the function call below to overwrite the existing data.
# create_scal_data(raw_data, orig_labels)


# Function to create the data for dimensionality experiments.
def create_dimensionality_data(raw_data, orig_labels):

    print("######################")
    print("Generating data for dimensionality experiments")
    print("######################")

    num_dims = [10, 20, 50, 80, 100]

    for n_dim in num_dims:
        temp = do_pca(raw_data, n_dim, orig_labels)
        temp.to_csv(os.path.join(dims_out_loc, "crop_"+str(n_dim)+".csv"), index=False, sep="\t")

        print("Data for ", n_dim, " dimensions saved at: ", dims_out_loc)

    return None

# Uncomment the function call below to overwrite the existing data.
create_dimensionality_data(raw_data, orig_labels)
