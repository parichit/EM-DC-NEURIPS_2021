# @Parichit, 2017, IUB, Computer Scince Department
# Edited by for BST implementation - @Parichit Sharma, 2021, IUB, Computer Science Department
from EMDC.BSTEM import *
from EMDC.testing import *
import time
from sklearn.metrics.cluster import adjusted_rand_score, adjusted_mutual_info_score


def model_eval(X, y, nclust, maxiter, epsilon, thres, mu_indices):
    # training
    start_time = time.time()
    mu, sigma, prior, iters = em_clustering(X, nclust, maxiter, epsilon, thres, mu_indices)
    TraningTime = time.time() - start_time

    # testing
    W = e_step(X, mu, sigma, prior, nclust)
    accuracy, pred = test(y, W, X)
    ari = adjusted_rand_score(y, pred)
    print("ARI: ", ari)
    accuracy = int(round(accuracy*100))
    TraningTime = round(TraningTime, 3)
    
    # print(" Traning running time :%s seconds " % TraningTime)
    # print( "accuracy:%s%%" % accuracy)
    return ari, accuracy, TraningTime, iters


# Census data
# data = pd.read_csv(os.path.join(input_loc, "census.txt"), header=0, sep=",")
# data = data.replace('?', np.NaN)
# data = data.dropna()
# pred1 = data.iloc[:, -1]
# data = data.iloc[:, 0:6] # subset the data
# # print(data.head(5))
# data = np.asarray(data, dtype=float)
# pred1 = np.asarray(pred1)
# print(pred1[0:10])

# result_dict = {}
# # nclust = [2, 5]
# nclust = [2, 5, 10, 20, 30]
#
# for i in [2, 3, 4]:
#     for nclus in nclust:
#         acc, trtime, iterations = model_eval(data, pred1, nclus, iter_cutoff, epsilon, i)
#         if i not in result_dict.keys():
#             result_dict[i] = [[nclus, acc, trtime, iterations]]
#         else:
#             result_dict[i] += [[nclus, acc, trtime, iterations]]

# for j in result_dict.keys():
#     print("Data proportion: 1/", j)
#     for m in result_dict[j]:
#         print("Cluster: ", m[0], " Acc: ", m[1], " Time: ", m[2], " Iters: ", m[3])

# Spambase data
# data = pd.read_csv(os.path.join(input_loc, "spambase.data"), header=None, sep=",")
# data = data.replace('?', np.NaN)
# data = data.dropna()
# pred1 = data.iloc[:, -1]
# data = data.iloc[:, 0:57] # subset the data
# data = np.asarray(data, dtype=float)
# pred1 = np.asarray(pred1)


# result_dict = {}
# nclust = [2, 5, 10, 20, 30]
#
# for i in [2, 3, 4]:
#     for nclus in nclust:
#         acc, trtime, iterations = model_eval(data, pred1, nclus, iter_cutoff, epsilon, i)
#         if i not in result_dict.keys():
#             result_dict[i] = [[nclus, acc, trtime, iterations]]
#         else:
#             result_dict[i] += [[nclus, acc, trtime, iterations]]
