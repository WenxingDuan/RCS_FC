import matplotlib.pyplot as plt
import numpy


def read_results(n):
    path = "e12-24\\" + str(n) + ".txt"
    file1 = open(path, 'r')
    y = file1.readlines()
    for i in range(len(y)):
        y[i] = y[i].split(',')
        for j in range(len(y[i])):
            y[i][j] = float(y[i][j])
    return y


results = [read_results(i) for i in range(12, 26, 2)]

# print (results)
# for i in results:
#     plt.plot(range(len(i[-1])), i[-1], marker=".", label=str(len(i[-1]) - 1))
# plt.yscale("log")
# plt.legend()
# plt.xticks(numpy.linspace(0, 24, 13))
# plt.xlabel("Order")
# plt.ylabel("Average Correlator")
# # plt.show()
# plt.savefig("12-24\\12-24")
# plt.clf()
n=12
for i in results:
    # for j in range(0, len(i) - 1):
    #     x = range(0, len(i[j]))
    #     y = i[j]
    #     plt.scatter(x, y, marker="*")
    x = range(0, len(i[-1]))
    plt.plot(x[1:], i[-1][1:], marker=".", linestyle="-",label="Experiment")
    plt.plot(list(range(1, n + 1)), [1 / (2**n)] * len(list(range(1, n + 1))),label="Ideal")
    plt.legend()
    plt.yscale("log")
    plt.xticks(numpy.linspace(1, len(i[-1]), int((len(i[-1]) - 1) / 2 + 1)))
    plt.xlabel("Order")
    plt.ylabel("Average Correlator")
    # plt.show()
    # print(len(i[-1]) - 1)
    plt.savefig("e12-24\\e\\"+str(len(i[-1]) - 1)+"_e")
    plt.clf()
    n=n+2
