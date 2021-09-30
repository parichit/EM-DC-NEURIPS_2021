from EMDC.eval_model import model_eval as emdc_model_eval
from EMSTAR.eval_model import model_eval as ems_model_eval
from EMT.eval_model import model_eval as emt_model_eval
from read_write_data import *
from datetime import datetime
from collections import Counter

import numpy as np
import os

parent_dir = os.getcwd()
input_loc = os.path.join(parent_dir, "datasets", "dimensionality_data")
output_loc = os.path.join(parent_dir, "benchmark_dims")

if os.path.exists(output_loc) is False:
    os.mkdir(output_loc)

else:
    curr_time = datetime.now()
    create_timestamp = str(curr_time.hour) + "_" + str(curr_time.minute) + "_" + str(curr_time.second)
    bkup_dir = os.path.join(parent_dir, "benchmark_dim_bkup" + create_timestamp)
    os.rename(output_loc, bkup_dir)
    os.mkdir(output_loc)

# Setting up parameters
epsilon = 0.01
num_iters = 500

prop = 3
num_dims = [10, 20, 50, 80, 100]
seed_cnt_clus = [9598, 1901, 3231, 453, 63987]
num_rep = 3
nclus = 10


### Dimensioanlity Experiments

print("#####################")
print("EMDC: Clustering Experiments")
print("#####################")

result_dict = {}

# def do_pca(dataset, n_comp, labels):
#     pca = PCA(n_components=n_comp)
#     ss = StandardScaler()
#     dataset = ss.fit_transform(dataset)
#     principalComponents = pca.fit_transform(dataset)
#     temp = pd.DataFrame(principalComponents)
#     temp["labels"] = labels
#     temp.to_csv(os.path.join(input_loc, "crop_"+str(n_comp)+".csv"), index=False, sep="\t")
#     # print("Variance: ", pca.explained_variance_)
#     pc_esc = np.array(pd.DataFrame(data=principalComponents))
#     return pc_esc

    
for dims in num_dims:
    print("Number of dimensions: ", dims)
    temp = []
    j = 0

    # Load data
    data, labels = read_dims_data(os.path.join(input_loc, "crop_"+str(dims)+".csv"))
    # data, labels = read_dims_data(os.path.join(input_loc, "crop.csv"))
    # data = do_pca(data, dims, labels)
    # continue

    # print(np.unique(labels), Counter(labels))

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emdc_model_eval(data, labels, nclus, num_iters, epsilon, prop, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [dims] + avg_score

    if dims not in result_dict.keys():
        result_dict[dims] = [temp]
    else:
        result_dict[dims] += [temp]

    #break

write_data(result_dict, output_loc, "emdc_res", "Dimensions")

print("#####################")
print("EMSTAR: Clustering Experiments")
print("#####################")


result_dict = {}

for dims in num_dims:
    print("Number of dimensions: ", dims)
    temp = []
    j = 0

    # Load data
    data, labels = read_dims_data(os.path.join(input_loc, "crop_"+str(dims)+".csv"))

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = ems_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [dims] + avg_score

    if dims not in result_dict.keys():
        result_dict[dims] = [temp]
    else:
        result_dict[dims] += [temp]


write_data(result_dict, output_loc, "emstar_res", "Dimensions")

print("#####################")
print("EMT: Clustering Experiments")
print("#####################")

num_iters = 1000
epsilon = 0.01

result_dict = {}

for dims in num_dims:
    print("Number of Dimensions: ", nclus)
    temp = []
    j = 0

    # Load data
    data, labels = read_dims_data(os.path.join(input_loc, "dimensionality_data", "crop_"+str(dims)+".csv"))

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emt_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [dims] + avg_score

    if dims not in result_dict.keys():
        result_dict[dims] = [temp]
    else:
        result_dict[dims] += [temp]


write_data(result_dict, output_loc, "emt_res", "Dimensions")



