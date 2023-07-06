import numpy as np

n = 50
_x = np.arange(n)
_y = np.arange(n)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()
z = np.zeros_like(x)

for i in range(50):
    print(f"2^x({ x[i]})+2^y({ y[i]})={2**x[i] + 2**y[i]}")
