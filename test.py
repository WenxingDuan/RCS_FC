import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义可能的函数形式，例如指数函数
def func(x, a, b):
    return a * np.power(x, b)

# x为输入的索引

# y为实际的数据值
y = np.array([0.00010734521023030304,7.802284341818183e-05,6.534640731151516e-05,5.638831208888889e-05,5.1025149513419915e-05,4.574705914343434e-05,4.2067672087272726e-05,3.728420493090909e-05,3.0994441163636365e-05,2.6831631200000004e-05,9.3911584e-06])
x = np.array(range(1, len(y) + 1))

# 使用curve_fit进行拟合，popt为拟合得到的参数值
popt, pcov = curve_fit(func, x, y)

# 打印拟合得到的参数值
print("拟合得到的参数值：", popt)

# 使用拟合得到的参数值生成拟合曲线的y值
y_fit = func(x, *popt)

# 创建新图像
plt.figure()

# 绘制原始数据点
plt.plot(x, y, 'bo', label='ori')

# 绘制拟合曲线
plt.plot(x, y_fit, 'r-', label='fit')

# 设置y轴为对数尺度
plt.yscale('log')

# 添加图例
plt.legend()

# 显示图像
plt.show()
