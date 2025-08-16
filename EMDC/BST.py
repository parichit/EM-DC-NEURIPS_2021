# @Parichit, 2017, IUB, Computer Scince Department
# Edited by for BST implementation - @Parichit Sharma, 2021, IUB, Computer Science Department
import numpy as np
from sortedcontainers import SortedList

def buildHeap(data, W, n, d, nclust, thres): #build heap

	bst_list = [[] for i in range(nclust)]  # build a BST for each cluster
	maxIndex = W.argmax(axis=0)  # predict the cluster

	for i in range(n):
		bst_list[maxIndex[i]].append([W[maxIndex[i], i], i])

	# Use BST to sort the data in order
	for i in range(nclust):
		bst_list[i] = SortedList(bst_list[i])

	# Separate the LE and HE data
	bst_list, he_index, he_data, temp1 = seperate_he_le(data, nclust, bst_list, d, thres)

	return bst_list, he_index, he_data, temp1


def newHeap(data, bst_list, W1, he_index, d, nclust, thres): # updating bst

	maxIndex = W1.argmax(axis=0)

	for i in range(len(he_index)):
		# print(i, "\n", maxIndex[i], "\n", bst_list[maxIndex[i]][0:10])
		bst_list[maxIndex[i]].add([W1[maxIndex[i], i], he_index[i][1]])

	bst_list, he_index, he_data, temp2 = seperate_he_le(data, nclust, bst_list, d, thres)

	return bst_list, he_index, he_data, temp2


def seperate_he_le(data, nclust, bst_list, d, thres): # seperate low and high expression data

	leaves = [[] for i in range(nclust)]

	for index in range(nclust):

		# Low expression data
		leaves[index] = bst_list[index][0:int(len(bst_list[index])/thres)]

		# High expression data
		bst_list[index] = SortedList(bst_list[index][int(len(bst_list[index])/thres):len(bst_list[index])])

		# print("Clus: ", index, "\n", "Cluster size: ", len(leaves[index]), "\n", 
		# "leaves size: ", len(leaves),)

	he_Index = sum(leaves, [])
	he_IndexLen = len(he_Index)
	badData = np.zeros((he_IndexLen, d), dtype=float)
	temp = []
	for j in range(he_IndexLen):
		badData[j] = data[he_Index[j][1]]
		temp.append(he_Index[j][1])

	return bst_list, he_Index, badData, temp