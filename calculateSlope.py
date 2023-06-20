import matplotlib.pyplot as plt
import csv
import math
import numpy as np


def read_results(n):
    path = "e0_" + str(n) + "\\result\\result.txt"

    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])

    return y


def predictSlope(result, n, m):
    if n < m:
        x = np.array([i for i in range(n, m + 1)])
        y = np.array(result[n:m + 1])
    else:
        # print("aaaa")
        x = np.array([i for i in range(m, n + 1)])
        y = np.array(result[m:n + 1])
    logy = np.log(y)
    # print(x)
    # print(logy)
    # print(n, m)

    coeff = np.polyfit(x, logy, 1)

    return coeff


for index in range(12, 25, 2):
    slope = [[0 for i in range(index + 1)] for j in range(index + 1)]
    cof = [[0 for i in range(index + 1)] for j in range(index + 1)]
    result = read_results(index)[:-1]

    # slope.append(math.log(result[1]) - math.log(result[3]))
    for i in range(len(result)):
        length = len(result[i])
        for n in range(length):
            for m in range(length):
                if m == n:
                    pass
                else:
                    slope[n][m] = predictSlope(result[i], m, n)[0]
                    cof[n][m] = predictSlope(result[i], m, n)[1]
        with open("e0_" + str(n) + "\\result\\" + str(i) + "_slope.csv",
                  'w',
                  newline='') as file:
            writer = csv.writer(file)
            writer.writerows(slope)
        with open("e0_" + str(n) + "\\result\\" + str(i) + "_cof.csv",
                  'w',
                  newline='') as file:
            writer = csv.writer(file)
            writer.writerows(cof)
    length = len(result[-1])
    for n in range(length):
        for m in range(length):
            if m == n:
                pass
            else:
                slope[n][m] = predictSlope(result[-1], m, n)[0]
                cof[n][m] = predictSlope(result[-1], m, n)[1]
    with open("e0_" + str(n) + "\\result\\final_slope.csv", 'w',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerows(slope)
    with open("e0_" + str(n) + "\\result\\final_cof.csv", 'w',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cof)
# print(slope)
