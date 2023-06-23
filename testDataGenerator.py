import random

# 预定义的概率列表
probabilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6]
probabilities.reverse()
# probabilities = [i/10 for i in range(0,10)]
print(probabilities)
# probabilities = [0.3 for _ in range(12)]

# 生成一万个比特串
bit_strings = []
for _ in range(500000):
    bit_string = ""
    for prob in probabilities:
        if random.random() < prob:
            bit_string += "1"
        else:
            bit_string += "0"
    bit_strings.append(bit_string)

# 将比特串写入文件
with open("bit_strings.txt", "w") as f:
    for bit_string in bit_strings:
        f.write(bit_string + "\n")
