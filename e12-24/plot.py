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
for i in results:
    plt.plot(range(len(i[-1])), i[-1], marker=".", label=str(len(i[-1]) - 1))
plt.yscale("log")
plt.legend()
plt.xticks(numpy.linspace(0, 24, 13))
plt.xlabel("Order")
plt.ylabel("Average Correlator")
# plt.show()
plt.savefig("e12-24\\12-24")
plt.clf()
for i in results:
    for j in range(0, len(i) - 1):
        x = range(0, len(i[j]))
        y = i[j]
        plt.scatter(x, y, marker="*")
    plt.plot(x, i[-1], marker=".", linestyle="-")
    plt.yscale("log")
    plt.xticks(numpy.linspace(0, len(i[-1]) - 1, int((len(i[-1]) - 1) / 2 + 1)))
    plt.xlabel("Order")
    plt.ylabel("Average Correlator")
    # plt.show()
    # print(len(i[-1]) - 1)
    plt.savefig("e12-24\\"+str(len(i[-1]) - 1))
    plt.clf()
