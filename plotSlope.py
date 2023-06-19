import matplotlib.pyplot as plt
import numpy
import math


def read_results(n):
    path = "e0_" + str(n) + "\\result\\result.txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


# print(len(read_results(12)[-1]))
for index in range(12, 25, 2):
    result = read_results(index)[-1]
    slope = []
    for i in range(1, len(result)):
        slope.append(round(math.log(result[i - 1]) - math.log(result[i]),4))
        # slope.append((result[i - 1] - result[i])*10**10)
    print(slope)
    x = range(1, len(result))
    y = result[1:]
    plt.plot(x, y, marker=".", label=str(len(result) - 1))
    for i in range(len(y)):
        plt.text(x[i], y[i], slope[i])
    plt.yscale("log")
    plt.legend()
    plt.xticks(numpy.linspace(0, index, 13))
    plt.xlabel("Order")
    plt.ylabel("Average Correlator")
    plt.show()