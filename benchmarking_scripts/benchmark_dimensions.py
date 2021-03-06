import os, sys

file_dir = os.path.dirname(os.getcwd())
sys.path.append(file_dir)

from EMDC.eval_model import model_eval as emdc_model_eval
from EMSTAR.eval_model import model_eval as ems_model_eval
from EMT.eval_model import model_eval as emt_model_eval
from benchmarking_scripts.read_write_data import *
from datetime import datetime
import numpy as np


parent_dir = os.path.dirname(os.getcwd())
input_loc = os.path.join(parent_dir, "datasets", "dimensionality_data")
output_loc = os.path.join(parent_dir, "benchmark_dims")

if os.path.exists(output_loc) is False:
    os.mkdir(output_loc)

else:
    curr_time = datetime.now()
    create_timestamp = str(curr_time.hour) + "_" + str(curr_time.minute) + "_" + str(curr_time.second)
    bkup_dir = os.path.join(parent_dir, "benchmark_dims_bkup" + create_timestamp)
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


## Dimensioanlity Experiments
print("#####################")
print("EMDC: Dimensionality Experiments")
print("#####################")

result_dict = {}

    
for dims in num_dims:
    print("Number of dimensions: ", dims)
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(dims)+".csv"), False)

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

write_data(result_dict, output_loc, "emdc_res", "Dimensions")



print("#####################")
print("EMSTAR: Dimensionality Experiments")
print("#####################")

result_dict = {}

for dims in num_dims:
    print("Number of dimensions: ", dims)
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(dims)+".csv"), False)

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
print("EMT: Dimensionality Experiments")
print("#####################")

num_iters = 1000
epsilon = 0.01

result_dict = {}

for dims in num_dims:
    print("Number of Dimensions: ", nclus)
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(dims)+".csv"), False)

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



