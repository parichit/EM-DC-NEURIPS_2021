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
input_loc = "/u/parishar/nobackup/DATASETS/geokmeans_data/real_data/"

# input_loc = os.path.join(parent_dir, "datasets", "clustering_data")
output_loc = os.path.join(parent_dir, "benchmark_clus/")
print(output_loc)

if os.path.exists(output_loc) is False:
    os.mkdir(output_loc)

else:
    curr_time = datetime.now()
    create_timestamp = str(curr_time.hour) + "_" + str(curr_time.minute) + "_" + str(curr_time.second)
    bkup_dir = os.path.join(parent_dir, "benchmark_clus_bkup" + create_timestamp)
    os.rename(output_loc, bkup_dir)
    os.mkdir(output_loc)


def do_pca(dataset, n_comp):
    pca = PCA(n_components=n_comp)
    ss = StandardScaler()
    dataset = ss.fit_transform(dataset)
    principalComponents = pca.fit_transform(dataset)
    # print("Variance: ", pca.explained_variance_)
    pc_esc = np.array(pd.DataFrame(data=principalComponents))
    return pc_esc



# Setting up parameters
epsilon = 0.001
num_iters = 200

prop = 3
num_clust = [2, 5, 10]
seed_cnt_clus = [9598, 1901, 3231, 453, 63987, 7821, 8903, 1234, 4321, 5678]
num_rep = 5

data_list = ['ringnorm', 'wisconsin', 'census', 'spambase', 'magic', 'crop']
# data_list = ['ringnorm', "wisconsin"]


### Clustering Experiments
all_results = pd.DataFrame(columns=["Dataset", "Model", "Clusters", "ARI", "ACC", "Time", "Iters"])
avg_results = pd.DataFrame(columns=["Dataset", "Model", "Clusters", "ARI", "ACC", "Time", "Iters"])



for data_name in data_list:

    data, labels = read_data(data_name)

    print("#####################")
    print("EMDC: Clustering Experiments")
    print("#####################")

    if data_name in ["census", "spambase", "magic"]:
        num_clust = [2, 10, 20, 30, 35]
    
    elif data_name in ["wisconsin", "ringnorm"]:
        num_clust = [2, 5, 10, 15, 20]
    
    elif data_name == "crop":
        num_clust = [5, 20, 30, 40, 50]
    
    for nclus in num_clust:
        
        print("Number of clusters: ", nclus)
        temp = pd.DataFrame()
        j = 0

        for rep in range(num_rep):

            np.random.seed(seed_cnt_clus[j])
            mu_indices = np.random.randint(0, data.shape[0], nclus)
            # mu_indices = [i for i in range(nclus)]

            ari, acc, trtime, iterations = emdc_model_eval(data, labels, nclus, num_iters, epsilon, prop, mu_indices)
            
            temp_series = pd.Series([data_name, "EM-D", nclus, ari, acc, trtime, iterations], index=all_results.columns)
            temp = pd.concat([temp, pd.DataFrame([temp_series])], ignore_index=True)

            j += 1

        all_results = pd.concat([all_results, temp], ignore_index=True)   
        avg_score = pd.Series([data_name, "EM-D"] + temp.iloc[:, 2:].mean().to_list(), index=avg_results.columns)
        avg_results = pd.concat([avg_results, pd.DataFrame([avg_score])], ignore_index=True)

    
    print("\n#####################")
    print("EMSTAR: Clustering Experiments")
    print("#####################\n")


    for nclus in num_clust:
        print("Number of clusters: ", nclus)
        temp = pd.DataFrame()
        j = 0

        for rep in range(num_rep):
            
            np.random.seed(seed_cnt_clus[j])
            mu_indices = np.random.randint(0, data.shape[0], nclus)
            # mu_indices = [i for i in range(nclus)]
            
            ari, acc, trtime, iterations = ems_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)

            temp_series = pd.Series([data_name, "EM*", nclus, ari, acc, trtime, iterations], index=all_results.columns)
            temp = pd.concat([temp, pd.DataFrame([temp_series])], ignore_index=True)

            j += 1

        all_results = pd.concat([all_results, temp], ignore_index=True)   
        avg_score = pd.Series([data_name, "EM*"] + temp.iloc[:, 2:].mean().to_list(), index=avg_results.columns)
        avg_results = pd.concat([avg_results, pd.DataFrame([avg_score])], ignore_index=True)

    
    print("\n#####################")
    print("EMT: Clustering Experiments")
    print("#####################")

    for nclus in num_clust:
        print("Number of clusters: ", nclus)
        temp = pd.DataFrame()
        j = 0

        for rep in range(num_rep):
            
            np.random.seed(seed_cnt_clus[j])
            mu_indices = np.random.randint(0, data.shape[0], nclus)
            # mu_indices = [i for i in range(nclus)]

            ari, acc, trtime, iterations = emt_model_eval(data, labels, nclus, num_iters, epsilon, mu_indices)
            
            temp_series = pd.Series([data_name, "EM-T", nclus, ari, acc, trtime, iterations], index=all_results.columns)
            temp = pd.concat([temp, pd.DataFrame([temp_series])], ignore_index=True)
            
            j += 1

        all_results = pd.concat([all_results, temp], ignore_index=True)
        avg_score = pd.Series([data_name, "EM-T"] + temp.iloc[:, 2:].mean().to_list(), index=avg_results.columns)
        avg_results = pd.concat([avg_results, pd.DataFrame([avg_score])], ignore_index=True)


# print(avg_results)
all_results.to_csv(output_loc + "all_results.csv", index=False)
avg_results.to_csv(output_loc + "avg_results.csv",  index=False)
