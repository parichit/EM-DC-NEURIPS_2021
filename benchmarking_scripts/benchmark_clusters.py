import os, sys

file_dir = os.path.dirname(os.getcwd())
sys.path.append(file_dir)

from EMDC.eval_model import model_eval as emdc_model_eval
from EMSTAR.eval_model import model_eval as ems_model_eval
from EMT.eval_model import model_eval as emt_model_eval
from benchmarking_scripts.read_write_data import *
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np


parent_dir = os.path.dirname(os.getcwd())

input_loc = os.path.join(parent_dir, "datasets", "clustering_data")
output_loc = os.path.join(parent_dir, "benchmark_clus")

if os.path.exists(output_loc) is False:
    os.mkdir(output_loc)

else:
    curr_time = datetime.now()
    create_timestamp = str(curr_time.hour) + "_" + str(curr_time.minute) + "_" + str(curr_time.second)
    bkup_dir = os.path.join(parent_dir, "benchmark_clus_bkup" + create_timestamp)
    os.rename(output_loc, bkup_dir)
    os.mkdir(output_loc)

# Setting up parameters
epsilon = 0.01
num_iters = 500

prop = 3
num_clust = [2, 5, 7]
seed_cnt_clus = [9598, 1901, 3231, 453, 63987]
num_rep = 1

def do_pca(dataset, n_comp):
    pca = PCA(n_components=n_comp)
    ss = StandardScaler()
    dataset = ss.fit_transform(dataset)
    principalComponents = pca.fit_transform(dataset)
    # print("Variance: ", pca.explained_variance_)
    pc_esc = np.array(pd.DataFrame(data=principalComponents))
    return pc_esc


### Clustering Experiments

data, labels = read_data(os.path.join(input_loc, "crop.csv"), False)
# data = do_pca(data, 10)

print("#####################")
print("EMDC: Clustering Experiments")
print("#####################")

result_dict = {}

    
for nclus in num_clust:
    
    print("Number of clusters: ", nclus)
    temp = []
    j = 0

    for rep in range(num_rep):

        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emdc_model_eval(data, labels, nclus, num_iters, epsilon, prop, mu_indices)

        temp += [[ari, acc, trtime, iterations]]

        j += 1
        
    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [nclus] + avg_score

    if nclus not in result_dict.keys():
        result_dict[nclus] = [temp]
    else:
        result_dict[nclus] += [temp]

write_data(result_dict, output_loc, "emdc_res", "Clusters")


print("#####################")
print("EMSTAR: Clustering Experiments")
print("#####################")


result_dict = {}

for nclus in num_clust:
    print("Number of clusters: ", nclus)
    temp = []
    j = 0

    for rep in range(num_rep):
        
        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = ems_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)
        
        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [nclus] + avg_score   

    if nclus not in result_dict.keys():
        result_dict[nclus] = [temp]
    else:
        result_dict[nclus] += [temp]
    

write_data(result_dict, output_loc, "emstar_res", "Clusters")

print("#####################")
print("EMT: Clustering Experiments")
print("#####################")

num_iters = 1000
epsilon = 0.01

result_dict = {}

for nclus in num_clust:
    print("Number of clusters: ", nclus)
    temp = []
    j = 0

    for rep in range(num_rep):
        
        np.random.seed(seed_cnt_clus[j])
        mu_indices = np.random.randint(0, data.shape[0], nclus)

        ari, acc, trtime, iterations = emt_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)
        
        temp += [[ari, acc, trtime, iterations]]

        j += 1

    temp = np.array(temp)
    avg_score = np.round(temp.mean(0),2).tolist()
    temp = [nclus] + avg_score   

    if nclus not in result_dict.keys():
        result_dict[nclus] = [temp]
    else:
        result_dict[nclus] += [temp]


write_data(result_dict, output_loc, "emt_res", "Clusters")
