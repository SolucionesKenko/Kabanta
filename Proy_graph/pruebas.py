# from collections import deque
# from PyQt5 import QtWidgets, QtCore
# import pyqtgraph as pg 
# import sys 
# import numpy as np
# number = 4
# pokemon = deque(list([1,2,3,4,5,6,7,8,9,10]))
# prueba = deque(list([0,0,0,0,0,0,0,0,0,0]),maxlen=10)

# for i in range(number):
#     prueba.append(list(pokemon)[i])
# print(prueba[1])
# print(list(pokemon)[0:number])
# print(prueba)

from collections import deque
number = 4
pokemon = deque(range(1, 11))
prueba = deque([9,10,11,12,13,0,0,0,0,0],maxlen=10)
prueba = deque(list(prueba) + list(pokemon)[:number],maxlen=10)

print(prueba)


