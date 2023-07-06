import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import cupy as cp
import sys


def int_to_bin_list(s):
    return list(map(int, str((bin(s)))[2:]))


def bin_to_int(a):
    return int(a, 2)


def calculate(filename, n, m, bin_order, sBarList):
    Z_file = [0 for i in range(n + 1)]
    f = open(filename, "r")
    fileListLines = f.readlines()
    fileList = cp.array([bin_to_int(i) for i in fileListLines])

    indx = 0
    for sBar_num in tqdm(range(len(sBarList)),
                         leave=False,
                         desc='Processing sBar'):
        sBar = sBarList[sBar_num]
        for s_num in tqdm(range(len(sBar)), leave=False):
            s = sBar[s_num]
            temp = cp.bitwise_and(s, fileList)
            binO = lambda x: bin_order[x]
            temp = (-1)**(binO(temp))
            Z_file[indx] = Z_file[indx] + int(cp.sum(temp))**2
        # print(indx)
        # Z_file[indx] = Z_file[indx] / (math.factorial(n) /
        #                        (math.factorial(indx) * math.factorial(n - indx)))
        # Z_file[indx] = Z_file[indx] / (m**2)
        # print(Z_file)
        
        indx = indx + 1

    # print(Z_file)

    Z_plt = Z_file.copy()

    for i in range(len(Z_file)):
        Z_plt[i] = Z_plt[i] / (math.factorial(n) /
                               (math.factorial(i) * math.factorial(n - i)))
        Z_plt[i] = Z_plt[i] / (m**2)
    # print(Z_plt)
    return (Z_plt)


n = 12
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
# for filnum in tqdm(range(1, D + 1), desc='Processing circuit'):

#     filenames = "n" + str(n) + "\\measurements_patch_n" + str(
#         n) + "_m14_s" + str(9 + filnum) + "_e18_pEFGH.txt"

#     Z_file = calculate(filenames, n, m, bin_order, sBarList)
#     Zlist.append(Z_file)
#     Z = Z + cp.array(Z_file)

#     plt.plot(list(range(1, n + 1)), Z_file[1:])
#     plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
#     plt.yscale("log")
#     plt.savefig("n" + str(n) + "\\result\\" + "measurements_patch_n" + str(n) +
#                 "_m14_s" + str(9 + filnum) + "_e18_pEFGH_LOG")
#     plt.clf()

#     plt.plot(list(range(1, n + 1)), Z_file[1:])
#     plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
#     plt.savefig("n" + str(n) + "\\result\\" + "measurements_patch_n" + str(n) +
#                 "_m14_s" + str(9 + filnum) + "_e18_pEFGH")
#     plt.clf()

# Z = Z / D
# Zlist.append(Z)

# # ========================================================
# f = open("n" + str(n) + "\\result\\result.txt", "w")
# for i in Zlist:
#     f.write(",".join([str(j) for j in i]) + "\n")
# # ========================================================

# plt.plot(list(range(1, n + 1)), list(Z.get())[1:])
# plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
# plt.yscale("log")
# plt.savefig("n" + str(n) + "\\result\\finalResult_LOG")
# # plt.show()
# plt.clf()

# plt.plot(list(range(1, n + 1)), list(Z.get())[1:])
# plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
# plt.savefig("n" + str(n) + "\\result\\finalResult")
# # plt.show()
# plt.clf()

#========================================================
#========================================================
#========================================================
for filnum in tqdm(range(1, D + 1), desc='Processing circuit'):

    filenames = "Full Circuit\\e0_" + str(n) + "\\measurements_n" + str(
        n) + "_m14_s" + str(-1 + filnum) + "_e0_pEFGH.txt"

    Z_file = calculate(filenames, n, m, bin_order, sBarList)
    Zlist.append(Z_file)
    Z = Z + cp.array(Z_file)

    plt.plot(list(range(1, n + 1)), Z_file[1:])
    plt.plot(list(range(1, n + 1)), [1 / (2**n)] * len(list(range(1, n + 1))))
    plt.yscale("log")
    plt.savefig("Full Circuit\\e0_" + str(n) + "\\result\\" + str(-1 + filnum) +
                "_LOG")
    plt.clf()



Z = Z / D
Zlist.append(Z)

# ========================================================
f = open("Full Circuit\\e0_" + str(n) + "\\result\\result.txt", "w")
for i in Zlist:
    f.write(",".join([str(j) for j in i]) + "\n")
# ========================================================

plt.plot(list(range(1, n + 1)), list(Z.get())[1:])
plt.plot(list(range(1, n + 1)), [1 / (2**n)] * len(list(range(1, n + 1))))
plt.yscale("log")
plt.savefig("Full Circuit\\e0_" + str(n) + "\\result\\finalResult_LOG")
# plt.show()
plt.clf()


#========================================================
#========================================================
#========================================================

# Z = calculate("e0_12\measurements_n12_m14_s0_e0_pEFGH.txt", 12, m, bin_order, sBarList)
# plt.plot(list(range(1,n + 1)), list(Z)[1:])
# plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
# plt.yscale("log")
# # plt.savefig("n" + str(n) + "\\GBSLOG")
# plt.show()
# plt.clf()

# plt.plot(list(range(1,n + 1)), list(Z)[1:])
# plt.plot(list(range(1, n + 1)),[1/(2**n)]*len(list(range(1, n + 1))))
# # plt.savefig("n" + str(n) + "\\GBS")
# plt.show()
# plt.clf()