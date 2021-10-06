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
input_loc = os.path.join(parent_dir, "datasets", "scalability_data")
output_loc = os.path.join(parent_dir, "benchmark_scal")

if os.path.exists(output_loc) is False:
    os.mkdir(output_loc)

else:
    curr_time = datetime.now()
    create_timestamp = str(curr_time.hour) + "_" + str(curr_time.minute) + "_" + str(curr_time.second)
    bkup_dir = os.path.join(parent_dir, "benchmark_scal_bkup" + create_timestamp)
    os.rename(output_loc, bkup_dir)
    os.mkdir(output_loc)

# Setting up parameters
epsilon = 0.01
num_iters = 500

prop = 3
num_data = [100, 150, 200, 250, 320]
seed_cnt_clus = [9598, 1901, 3231, 453, 63987]
num_rep = 3
nclus = 10


### Scalability Experiments

print("#####################")
print("EMDC: Scalability Experiments")
print("#####################")

result_dict = {}


for n in num_data:
    print("Number of data points: ", n, " thousand")
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(n)+".csv"), False)

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emdc_model_eval(data, labels, nclus, num_iters, epsilon, prop, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [n] + avg_score

    if n not in result_dict.keys():
        result_dict[n] = [temp]
    else:
        result_dict[n] += [temp]


write_data(result_dict, output_loc, "emdc_res", "Num_points")

print("#####################")
print("EMSTAR: Clustering Experiments")
print("#####################")


result_dict = {}

for n in num_data:
    print("Number of data points: ", n, " thousand")
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(n)+".csv"), False)

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = ems_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [n] + avg_score

    if n not in result_dict.keys():
        result_dict[n] = [temp]
    else:
        result_dict[n] += [temp]


write_data(result_dict, output_loc, "emstar_res", "Num_points")

print("#####################")
print("EMT: Clustering Experiments")
print("#####################")

num_iters = 1000
epsilon = 0.01

result_dict = {}

for n in num_data:
    print("Number of data points: ", n, " thousand")
    temp = []
    j = 0

    # Load data
    data, labels = read_data(os.path.join(input_loc, "crop_"+str(n)+".csv"), False)

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emt_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [n] + avg_score

    if n not in result_dict.keys():
        result_dict[n] = [temp]
    else:
        result_dict[n] += [temp]


write_data(result_dict, output_loc, "emt_res", "Num_points")



