import matplotlib.pyplot as plt
import csv
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


for index in range(12, 25, 2):
    slope = [[0 for i in range(index + 1)] for j in range(index + 1)]
    result = read_results(index)[:-1]
    
    # slope.append(math.log(result[1]) - math.log(result[3]))
    for i in range(len(result)):
        length = len(result[i])
        for n in range(length):
            for m in range(length):
                if m==n:
                    pass
                else:
                    slope[n][m] = (math.log(result[i][n]) - math.log(result[i][m]))/(abs(n-m))
        with open("e0_" + str(n) + "\\result\\" + str(i) + "_slope.csv",
                  'w',
                  newline='') as file:
            writer = csv.writer(file)
            writer.writerows(slope)
    
    length = len(result[-1])
    for n in range(length):
        for m in range(length):
            if m==n:
                pass
            else:
                slope[n][m] = (math.log(result[i][n]) - math.log(result[i][m]))/(abs(n-m))
    with open("e0_" + str(n) + "\\result\\final_slope.csv", 'w',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerows(slope)
# print(slope)
