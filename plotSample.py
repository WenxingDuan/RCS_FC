import matplotlib.pyplot as plt
import numpy

# def read_results(qub, n):
#     path = str(qub) + "\\sample\\" + str(n) + ".txt"
#     file1 = open(path, 'r')
#     y = file1.readlines()
#     for i in range(len(y)):
#         y[i] = y[i].split(',')
#         for j in range(len(y[i])):
#             y[i][j] = float(y[i][j])
#     return y


def readSampleData(qub, n, size):
    path = "Full Circuit\\e0_" + str(qub) + "\\sample\\" + str(size) + "\\" + str(n) + ".txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


def readAverageResult(n):
    path = "Full Circuit\\e0_" + str(n) + "\\result\\result.txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


qubits = [x for x in range(12, 25, 2)]
samplesize = [5, 7, 10]
sampleindex = [i for i in range (1,11)]
for qub in qubits:
    result = readAverageResult(qub)[-1]
    color = ["red", "blue", "green"]
    colorindex = 0
    for size in samplesize:
        for index in sampleindex:
            name = str(index) + "_" + str(size)
            points = readSampleData(qub, name, size)
            x = range(0, len(points[-1]))
            for exp in points:
                plt.plot(x[1:],
                         exp[1:],
                         marker="*",
                         linestyle="--",
                         alpha=0.1,
                         color=color[colorindex],
                         label=str(size) + " Groups")
            plt.plot(x[1:], [1 / (500000 / size) for k in x[1:]],
                     linestyle="-",
                     color=color[colorindex],
                     label="1/m")
        colorindex = colorindex + 1

    plt.yscale("log")
    plt.xlabel("Order")
    plt.ylabel("Average Correlator")
    plt.title(str(qub) + " Qubit, Sepreated into 5/7/10 Groups")
    plt.plot(x[1:],
             result[1:],
             marker=".",
             linestyle="-",
             color="black",
             label="Overall Average")
    plt.plot(x[1:], [1 / (500000) for k in x[1:]],
             linestyle="-",
             color="black",
             label="1/m")
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.savefig("Full Circuit\\e0_" + str(qub) + "\\sample\\sample_result")
    plt.clf()
