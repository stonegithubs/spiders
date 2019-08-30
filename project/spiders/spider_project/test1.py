import numpy as np

filename = './presidential_polls.csv'
data_arr = np.loadtxt(filename,
                      delimiter=',',
                      skiprows=1,
                      dtype=str,
                      usecols=(3, 17, 18, 19),
                      )
print(data_arr)
print(type(data_arr))

print(data_arr.ndim)
print(data_arr.shape)
print(data_arr.dtype)

import random

arr = np.random.rand(4, 4)
print(arr)

arr = np.random.randint(-1, 5, size=(3, 4))
print(arr)
print(type(arr))
print(arr.dtype)

arr1 = np.arange(10)
print(arr1)
print(arr1[2])
print(arr1[:4])
print(arr1[5:7])

arr2 = np.arange(12).reshape(3, 4)
print(arr2)
print(arr2[0:, 0:1])
