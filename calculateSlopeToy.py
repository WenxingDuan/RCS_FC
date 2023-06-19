import matplotlib.pyplot as plt
import csv
import math


def read_results(error, size):
    path = "6bits\\" + str(error) + "\\" + str(size) + "\\result\\result.txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


for error in range(11):
    for size in [1000, 10000, 100000, 1000000]:
        result = read_results(error, size)[:-1]

        slope = [[0 for i in range(7)] for j in range(7)]
        # slope.append(math.log(result[1]) - math.log(result[3]))
        for i in range(len(result)):
            length = len(result[i])
            for n in range(length):
                for m in range(length):
                    try:
                        slope[n][m] = (math.log(result[i][n]) - math.log(
                            result[i][m]))/abs(n-m)
                    except:
                        pass
            with open("6bits\\" + str(error) + "\\" + str(size) +
                      "\\result\\exp_" + str(i+1) + "_slope.csv",
                      'w',
                      newline='') as file:
                writer = csv.writer(file)
                writer.writerows(slope)
        length = len(result[-1])
        for n in range(length):
            for m in range(length):
                try:
                    slope[n][m] = (math.log(result[-1][n]) - math.log(result[-1][m]))/abs(n-m)
                except:
                    pass
        with open("6bits\\" + str(error) + "\\" + str(size) +
                  "\\result\\final_slope.csv",
                  'w',
                  newline='') as file:
            writer = csv.writer(file)
            writer.writerows(slope)
# print(slope)
