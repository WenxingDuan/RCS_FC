import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import cupy as cp
import numpy as np
import sys
import matplotlib.gridspec as gridspec


@cp.vectorize
def int_to_bin_list(s):
    return sum(list(map(int, str((bin(s)))[2:])))


def bin_to_int(a):
    return int(a, 2)


from itertools import combinations


def generate_bitstrings(n):
    # Generate bitstrings containing exactly one '1'.
    bitstrings_one = [
        ''.join('1' if i in combo else '0' for i in range(n))
        for combo in combinations(range(n), 1)
    ]
    bitstrings_one.reverse()
    # Generate bitstrings containing exactly two '1's.
    bitstrings_two = [
        ''.join('1' if i in combo else '0' for i in range(n))
        for combo in combinations(range(n), 2)
    ]
    bitstrings_two.reverse()
    return [
        cp.array([bin_to_int(a) for a in bitstrings_one]),
        cp.array([bin_to_int(a) for a in bitstrings_two])
    ]


def calculate(filename, n, m, bin_order, sBarList):
    detail = dict()
    Z_file = [0 for i in range(n + 1)]

    indx = 0
    print(1)
    # binO = lambda x: np.array([bin_order[int(xx)] for xx in x])
    binO = lambda x: bin_order[int(x)]
    bin_order_indx = 0
    for sBar_num in range(0, len(sBarList)):
        sBar = sBarList[sBar_num]
        for s_num in tqdm(range(len(sBar)), leave=False):
            print(2)
            s = sBar[s_num]
            print(3)
            # temp = cp.bitwise_and(s, fileList)
            temp = list(range(bin_order_indx, bin_order_indx + m))
            # binO = lambda x: cp.array(
            #     [int(sum(int_to_bin_list(i))) for i in x])
            # binO = lambda x: bin_order[int(x)]

            print(4)
            temp = (-1)**(binO(temp))
            print(5)
            Z_file[indx] = Z_file[indx] + int(cp.sum(temp))**2
            detail[int(s)] = int(cp.sum(temp)) / m
            bin_order_indx = bin_order_indx + m

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


# def plot3D(ax, n, detail):
#     _x = np.arange(n)
#     _y = np.arange(n)
#     _xx, _yy = np.meshgrid(_x, _y)
#     x, y = _xx.ravel(), _yy.ravel()
#     z = np.zeros_like(x)
#     dx = dy = np.ones_like(z) * 0.5
#     dz = [
#         2**x[i] + 2**y[i] if x[i] != y[i] else 0 for i in range(len(x))
#     ]
#     ax.bar3d(x, y, z, dx, dy, dz)
#     # plt.show()
def plot3D(ax, n, detail):
    _x = np.arange(n).tolist()
    _y = np.arange(n).tolist()
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel().tolist(), _yy.ravel().tolist()
    z = [0] * len(x)
    dx = dy = [0.5] * len(z)
    dz = [2**x[i] + 2**y[i] if x[i] != y[i] else 0 for i in range(len(x))]
    ax.bar3d(x, y, z, dx, dy, dz)


# def plotHeatmap(ax, n, detail):
#     _x = np.arange(n)
#     _y = np.arange(n)
#     _xx, _yy = np.meshgrid(_x, _y)
#     x, y = _xx.ravel(), _yy.ravel()
#     z = np.zeros_like(x)
#     dx = dy = np.ones_like(z) * 0.5
#     dz = [
#         detail[2**x[i] + 2**y[i]] if x[i] != y[i] else 0 for i in range(len(x))
#     ]
#     square_list = []

#     for i in range(0, len(dz), n):
#         square_list.append(dz[i:i + n])
#     x_labels = [i for i in range(0, n)]
#     # y_labels = [str(i) for i in range(1, n + 1)]
#     ax.set_xticks(x_labels)
#     ax.set_yticks(x_labels)
#     x_labels = [str(i) for i in range(1, n + 1)]
#     ax.set_xticklabels(x_labels)
#     ax.set_yticklabels(x_labels)

#     im = ax.imshow(square_list,
#                    cmap='RdBu',
#                    origin='lower',
#                    vmin=-max(max(dz), -min(dz)),
#                    vmax=max(max(dz), -min(dz)))

#     fig.colorbar(im, ax=ax)  # 在指定的axes上添加colorbar


def plotHeatmap(ax, n, detail):
    _x = np.arange(n).tolist()
    _y = np.arange(n).tolist()
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel().tolist(), _yy.ravel().tolist()
    z = [0] * len(x)
    dx = dy = [0.5] * len(z)
    dz = [
        detail[2**x[i] + 2**y[i]] if x[i] != y[i] else 0 for i in range(len(x))
    ]
    square_list = []

    for i in range(0, len(dz), n):
        square_list.append(dz[i:i + n])
    x_labels = [i for i in range(0, n)]
    ax.set_xticks(x_labels)
    ax.set_yticks(x_labels)
    x_labels = [str(i) for i in range(1, n + 1)]
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(x_labels)

    im = ax.imshow(square_list,
                   cmap='RdBu',
                   origin='lower',
                   vmin=-max(max(dz), -min(dz)),
                   vmax=max(max(dz), -min(dz)))

    fig.colorbar(im, ax=ax)  # 在指定的axes上添加colorbar


@np.vectorize
def hamming_weight(n):
    return bin(n).count('1')


n = 50
# n = int(sys.argv[1])
m = 500000
D = 10
sLength = 2**(n)

sBarList = generate_bitstrings(n)

for filnum in tqdm(range(1, D + 1), desc='Processing circuit'):
    detail = dict()
    filename = "C:\\Users\\Duan\OneDrive - University of Edinburgh\\Year 4\\毕设\\doi_10.5061_dryad.k6t1rj8__v11\\n50_m14\\measurements_n" + str(
        n) + "_m14_s" + str(-1 + filnum) + "_e0_pEFGH.txt"
    # filename = "bit_strings.txt"

    # filename = "e0_" + str(n) + "\\measurements_n" + str(n) + "_m14_s" + str(
    #     -1 + filnum) + "_e0_pEFGH.txt"

    Z_file = [0 for i in range(n + 1)]
    f = open(filename, "r")
    fileListLines = f.readlines()
    fileList = cp.array([bin_to_int(i) for i in fileListLines])
    for sBar_num in range(0, len(sBarList)):
        sBar = sBarList[sBar_num]
        templ = []
        # print(len(sBar))
        for s_num in tqdm(range(len(sBar))):
            s = sBar[s_num]
            temp = cp.bitwise_and(s, fileList)
            temp = temp.get()
            temp = hamming_weight(temp)
            temp = (-1)**(temp)
            detail[int(s)] = int(np.sum(temp)) / m
    print(detail)

    fig = plt.figure(figsize=(20, 18))
    ax1 = fig.add_subplot(211)
    plotBar(ax1, [str(int(math.log(i, 2) + 1)) for i in sBarList[0]],
            [detail[int(i)] for i in sBarList[0]])

    # ax2 = fig.add_subplot(223, projection='3d')
    # plot3D(ax2, n, detail)

    ax3 = fig.add_subplot(212)
    plotHeatmap(ax3, n, detail)
    # plt.tight_layout()
    plt.show()
    # plt.savefig("e0_" + str(n) + "\\s" + str(filnum - 1))
