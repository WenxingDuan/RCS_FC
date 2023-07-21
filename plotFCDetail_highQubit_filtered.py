import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import cupy as cp
import numpy as np
import sys
import matplotlib.gridspec as gridspec
from Circuit import CircuitReadder


@cp.vectorize
def int_to_bin_list(s):
    return sum(list(map(int, str((bin(s)))[2:])))


def bin_to_int(a):
    return int(a, 2)


from itertools import combinations


@np.vectorize
def hamming_weight(n):
    return bin(n).count('1')


def filterCorrectedTermOrder_1(corrected_term, _, y):
    outputX = [i for i in range(1, len(corrected_term) + 1)]
    outputY = [y[x] for x in corrected_term]
    x_labels = [str(i + 1) for i in corrected_term]
    return (outputX, outputY, x_labels)


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

    # binO = lambda x: np.array([bin_order[int(xx)] for xx in x])
    binO = lambda x: bin_order[int(x)]
    bin_order_indx = 0
    for sBar_num in range(0, len(sBarList)):
        sBar = sBarList[sBar_num]
        for s_num in tqdm(range(len(sBar)), leave=False):

            s = sBar[s_num]

            # temp = cp.bitwise_and(s, fileList)
            temp = list(range(bin_order_indx, bin_order_indx + m))
            # binO = lambda x: cp.array(
            #     [int(sum(int_to_bin_list(i))) for i in x])
            # binO = lambda x: bin_order[int(x)]

            temp = (-1)**(binO(temp))

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


def plotBar(ax, categories, values, xtick):
    bars = ax.bar(categories,
                  values,
                  color=['blue' if v > 0 else 'red' for v in values])
    # print(values)
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
    ax.set_xlabel('Qubit')
    ax.set_xticks(categories)  # Set x-axis tick positions
    ax.set_xticklabels(xtick)  # Set x-axis tick labels
    # plt.show()


def filterCorrectedTermOrder_2(corrected_term, square_list):
    fullQubit = [i for i in range(len(square_list))]
    delQubit = [i for i in fullQubit if i not in corrected_term]
    delQubit.sort(reverse=True)
    for i in delQubit:
        square_list.pop(i)
        for j in range(len(square_list)):
            square_list[j].pop(i)
    x_labels = [str(i + 1) for i in corrected_term]
    xtick = [i for i in range(1, len(corrected_term) + 1)]
    return (square_list, xtick, x_labels)


def plotHeatmap(ax, n, detail):
    _x = np.arange(n).tolist()
    _y = np.arange(n).tolist()
    _x.reverse()
    _y.reverse()
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
    square_list, xtick, x_labels = filterCorrectedTermOrder_2(
        corrected_term, square_list)
    # x_labels = [i for i in range(0, n)]
    ax.set_xticks(xtick)
    ax.set_yticks(xtick)
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(x_labels)

    im = ax.imshow(square_list,
                   cmap='RdBu',
                   origin='lower',
                   vmin=-max(max(dz), -min(dz)),
                   vmax=max(max(dz), -min(dz)))

    fig.colorbar(im, ax=ax)


for n in tqdm(range(12, 41, 2), desc='Processing qubit', leave=True):

    m = 500000
    D = 10
    sLength = 2**(n)
    corrected_term = CircuitReadder.correct_index(n)

    sBarList = generate_bitstrings(n)
    # print(sBarList[0])

    for filnum in tqdm(range(1, D + 1), desc='Processing circuit',
                       leave=False):
        detail = dict()

        filename = "Full Circuit/e0_" + str(n) + "/measurements_n" + str(
            n) + "_m14_s" + str(-1 + filnum) + "_e0_pEFGH.txt"

        Z_file = [0 for i in range(n + 1)]
        f = open(filename, "r")
        fileListLines = f.readlines()
        fileList = cp.array([bin_to_int(i) for i in fileListLines])
        for sBar_num in range(0, len(sBarList)):
            sBar = sBarList[sBar_num]
            templ = []
            # print(len(sBar))
            for s_num in tqdm(range(len(sBar)), leave=False):
                s = sBar[s_num]
                temp = cp.bitwise_and(s, fileList)
                temp = temp.get()
                temp = hamming_weight(temp)
                temp = (-1)**(temp)
                detail[int(s)] = int(np.sum(temp)) / m
        # print(detail)

        fig = plt.figure(figsize=(20, 18))
        ax1 = fig.add_subplot(211)
        ax1_x = [str(int(math.log(i, 2) + 1)) for i in sBarList[0]]
        ax1_y = [detail[int(i)] for i in sBarList[0]]
        ax1_y.reverse()
        ax1_x, ax1_y, x_labels = filterCorrectedTermOrder_1(
            corrected_term, ax1_x, ax1_y)
        plotBar(ax1, ax1_x, ax1_y, x_labels)

        # ax2 = fig.add_subplot(223, projection='3d')
        # plot3D(ax2, n, detail)

        ax3 = fig.add_subplot(212)
        plotHeatmap(ax3, n, detail)
        # plt.tight_layout()
        # plt.show()
        plt.savefig("Full Circuit/e0_" + str(n) + "/s_filter" +
                    str(filnum - 1))
        plt.close()
        plt.close(fig)
