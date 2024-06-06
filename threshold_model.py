import random
import numpy as np
from matplotlib import pyplot as plt

n = 100  #количество агентов
mu_matrix = [random.random() for i in range(n)] #создание матрицы пороговых значений
neighboor_matrix = np.random.randint(0, 2, (n, n)) #матрица соседей (симметричная)
neighboor_matrix ^= neighboor_matrix.T


#возращает массив длинной n с заданным x - количеством единиц
def mas_x_edinic(n, x):
    mas = np.zeros(n)
    while sum(mas) < x:
        mas[random.randint(0, n-1)] = 1
    return mas

def threshold(pred_sost):
    global n, neighboor_matrix, mu_matrix
    t=0
    print('t = 0:', sum(pred_sost), '- сумма значений "1" в начальный момент')
    #создание массива, в котором будут храниться все состояния агентов во все моменты времени
    sost_mas_tek = [pred_sost]
    #создание массива, в котором будут хранится количества "единиц" у агентов
    y_mas= [sum(pred_sost)]
    stop_kol = 20
    while stop_kol > 0 and sum(pred_sost) < n:
        stop_kol -= 1
        current_matrix = []
        for i in range(n):
            k = np.dot(pred_sost, neighboor_matrix[i])
            if k / sum(neighboor_matrix[i]) > mu_matrix[i]: # сравнение полченного значения с пороговым
                current_matrix.append(1)
            else:
                current_matrix.append(0)
        #обновление данных
        pred_sost = current_matrix
        sost_mas_tek.append(pred_sost)
        t += 1
        y_mas.append(sum(pred_sost))
    print('t =', len(y_mas), ':', sum(pred_sost), '- сумма значений "1" в последний момент\n')
    x = range(len(y_mas))
    plt.plot(x, y_mas)


plt.figure(figsize=(12,7))
count_test = 50 #количество тетстов
for i in range(count_test):
    print("Тест №", i + 1, sep='')
    sostoinie = mas_x_edinic(n, n//count_test* i)
    threshold(sostoinie)
plt.show()
