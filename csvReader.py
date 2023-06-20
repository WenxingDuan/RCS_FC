import os
import glob
import csv
import math

from matplotlib import pyplot as plt

folders = glob.glob('e0_*')
slope = {}

for folder in folders:
    folder_data = []
    files = sorted(glob.glob(os.path.join(folder, 'result\\*_slope.csv')))
    for file in files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            file_data = [list(map(float, row)) for row in reader]
            folder_data.append(file_data)
    key = int(folder.split('_')[1])
    slope[key] = folder_data

# folders = glob.glob('e0_*')
cof = {}

for folder in folders:
    folder_data = []
    files = sorted(glob.glob(os.path.join(folder, 'result\\*_cof.csv')))
    for file in files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            file_data = [list(map(float, row)) for row in reader]
            folder_data.append(file_data)
    key = int(folder.split('_')[1])
    cof[key] = folder_data


def readSlope(qubit, circuit, n, m):
    return slope[qubit][circuit][n][m]


def readCof(qubit, circuit, n, m):
    return cof[qubit][circuit][n][m]


def read_results(n):
    path = "e0_" + str(n) + "\\result\\result.txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


def plotPredictions(qubit, circuit, n, m):
    data = read_results(qubit)[circuit]
    theSlope = readSlope(qubit, circuit, n, m)
    theCof = readCof(qubit, circuit, n, m)
    print(f"y = e ^ ( a x + b ) , a = {theSlope} , b = {theCof}")
    f = lambda x: math.e**(theSlope * x + theCof)
    plt.plot(list(range(1, qubit + 1)), data[1:])
    plt.plot(list(range(n, m + 1)), [f(i) for i in range(n, m + 1)])

    plt.yscale("log")
    plt.show()
