import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import numpy as cp
import sys
import matplotlib.gridspec as gridspec


def int_to_bin_list(s):
    return list(map(int, str((bin(s)))[2:]))


def bin_to_int(a):
    return int(a, 2)


def calculate(filename, n, m, bin_order, sBarList):
    detail = dict()
    Z_file = [0 for i in range(n + 1)]
    f = open(filename, "r")
    fileListLines = f.readlines()
    fileList = cp.array([bin_to_int(i) for i in fileListLines])

    indx = 0
    for sBar_num in tqdm(range(1, len(sBarList)),
                         leave=False,
                         desc='Processing sBar'):
        sBar = sBarList[sBar_num]
        for s_num in tqdm(range(len(sBar)), leave=False):
            s = sBar[s_num]
            temp = cp.bitwise_and(s, fileList)
            binO = lambda x: bin_order[x]
            temp = (-1)**(binO(temp))
            Z_file[indx] = Z_file[indx] + int(cp.sum(temp))**2
            detail[int(s)] = int(cp.sum(temp)) / m
        if sBar_num >= 2:
            break
        indx = indx + 1

    # print(Z_file)

    Z_plt = Z_file.copy()

    for i in range(len(Z_file)):
        Z_plt[i] = Z_plt[i] / (math.factorial(n) /
                               (math.factorial(i) * math.factorial(n - i)))
        Z_plt[i] = Z_plt[i] / (m**2)
    # print(Z_plt)
    return (Z_plt, detail)


def plotBar(ax, categories, values):
    bars = ax.bar(categories,
                  values,
                  color=['blue' if v > 0 else 'red' for v in values])

    ax.axhline(0, color='black', linewidth=0.8)

    for bar in bars:
        yval = bar.get_height()
        if yval >= 0:
            label_position = yval - 0.1
        else:
            label_position = yval + 0.05
        ax.text(bar.get_x() + bar.get_width() / 2,
                label_position,
                round(yval, 2),
                color='white',
                ha='center',
                va='center')

    # plt.show()


def plot3D(ax, n, detail):
    _x = cp.arange(n)
    _y = cp.arange(n)
    _xx, _yy = cp.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()
    z = cp.zeros_like(x)
    dx = dy = cp.ones_like(z) * 0.5
    dz = [
        detail[2**x[i] + 2**y[i]] if x[i] != y[i] else 0 for i in range(len(x))
    ]
    ax.bar3d(x, y, z, dx, dy, dz)
    # plt.show()


def plotHeatmap(ax, n, detail):
    _x = cp.arange(n)
    _y = cp.arange(n)
    _xx, _yy = cp.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()
    z = cp.zeros_like(x)
    dx = dy = cp.ones_like(z) * 0.5
    dz = [
        detail[2**x[i] + 2**y[i]] if x[i] != y[i] else 0 for i in range(len(x))
    ]
    square_list = []

    for i in range(0, len(dz), n):
        square_list.append(dz[i:i + n])
    x_labels = [i for i in range(0, n)]
    # y_labels = [str(i) for i in range(1, n + 1)]
    ax.set_xticks(x_labels)
    ax.set_yticks(x_labels)
    x_labels = [str(i) for i in range(1, n+1)]
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(x_labels)


    im = ax.imshow(square_list,
                   cmap='RdBu',
                   origin='lower',
                   vmin=-max(max(dz), -min(dz)),
                   vmax=max(max(dz), -min(dz)))


    fig.colorbar(im, ax=ax)  # 在指定的axes上添加colorbar


n = 16
# n = int(sys.argv[1])
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

for filnum in tqdm(range(1, D + 1), desc='Processing circuit'):

    filenames = "e0_" + str(n) + "\\measurements_n" + str(n) + "_m14_s" + str(
        -1 + filnum) + "_e0_pEFGH.txt"

    Z_file, detail = calculate(filenames, n, m, bin_order, sBarList)
    fig = plt.figure(figsize=(20, 18))
    ax1 = fig.add_subplot(221) 
    plotBar(ax1, [str(i) for i in sBarList[1]],
            [detail[int(i)] for i in sBarList[1]])

    ax2 = fig.add_subplot(223, projection='3d') 
    plot3D(ax2, n, detail)

    ax3 = fig.add_subplot(224)
    plotHeatmap(ax3, n, detail)
    # plt.tight_layout()
    # plt.show()
    plt.savefig("e0_" + str(n) + "\\s" + str(filnum - 1))
    Zlist.append(Z_file)
    Z = Z + cp.array(Z_file)

# Z = Z / D
# Zlist.append(Z)

# # ========================================================
# f = open("e0_" + str(n) + "\\result\\result.txt", "w")
# for i in Zlist:
#     f.write(",".join([str(j) for j in i]) + "\n")
# # ========================================================

# plt.plot(list(range(1, n + 1)), list(Z.get())[1:])
# plt.plot(list(range(1, n + 1)), [1 / (2**n)] * len(list(range(1, n + 1))))
# plt.yscale("log")
# plt.savefig("e0_" + str(n) + "\\result\\finalResult_LOG")
# # plt.show()
# plt.clf()
