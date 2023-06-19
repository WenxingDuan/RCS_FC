import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import numpy as cp
import sys


def int_to_bin_list(s):
    return list(map(int, str((bin(s)))[2:]))


def bin_to_int(a):
    return int(a, 2)


def calculateOrderAverages(order, n, m, bin_order, sBarList, data):
    sBar = sBarList[order]
    result = [0 for i in range(len(data))]
    index = 0
    for fileList in data:
        for s_num in range(len(sBar)):
            s = sBar[s_num]
            temp = cp.bitwise_and(s, fileList)
            binO = lambda x: bin_order[x]
            temp = (-1)**(binO(temp))
            result[index] = result[index] + int(cp.sum(temp))**2
        index = index + 1

    for i in range(len(result)):
        result[i] = result[i] / (
            math.factorial(n) /
            (math.factorial(order) * math.factorial(n - order)))
        result[i] = result[i] / (m**2)
    return result


def readFiles(filenames):
    data = []
    for filename in filenames:
        f = open(filename, "r")
        fileListLines = f.readlines()
        fileList = cp.array([bin_to_int(i) for i in fileListLines])
        data.append(fileList)
    return data


n = 14
# n = int(sys.argv[1])
fullCircuit = True
m = 500000
D = 10
sLength = 2**(n)
bin_order = cp.array([
    int(sum(int_to_bin_list(i)))
    for i in tqdm(range(0, sLength), desc='Initializing Step 1', leave=False)
])

sBarList = [[] for i in range(0, n + 1)]

for i in tqdm(range(0, sLength), desc='Initializing Step 2', leave=False):
    sBarList[sum(int_to_bin_list(i))].append(i)
sBarList = [cp.array(i) for i in sBarList]

Z = cp.array([0 for i in range(n + 1)])
Zlist = []

if fullCircuit:
    filenames = [
        "e0_" + str(n) + "\\measurements_n"+str(n)+"_m14_s" + str(i) + "_e0_pEFGH.txt"
        for i in range(10)
    ]
else:
    filenames = [
        "n" + str(n) + "\\measurements_patch_n"+str(n)+"_m14_s1" + str(i) +
        "_e18_pEFGH.txt" for i in range(10)
    ]
resultlist = [1]
averagelist = [1]
for i in range(1, n + 1):
    data = readFiles(filenames)
    result = calculateOrderAverages(i, n, m, bin_order, sBarList, data)
    resultlist.append(result)
    average = sum(result) / len(result)
    averagelist.append(average)
    # print(averagelist)
    slope = abs(
        round(math.log(averagelist[i - 1]) - math.log(averagelist[i]), 5))

    print(slope)
    if slope < 0.001:
        averagelist = averagelist + [[average] for j in range(i, n + 1)]
        break
print(averagelist)
