import numpy as np
from matplotlib import pyplot as plt
from numpy import mean
from numpy.linalg import matrix_power


def matrix(rebra, orient):
    n = 0
    for i in rebra:
        n = max(n, i[0]+1, i[1]+1)
    matrica = np.zeros((n,n), dtype="float32")
    for line in rebra:
        if orient:
            matrica[line[0]][line[1]] = line[2]
        else:
            matrica[line[0]][line[1]] = line[2]
            matrica[line[1]][line[0]] = line[2]
    for i in range(n):
        k = sum(matrica[i])
        if k != 0:
            for j in range(n):
                matrica[i][j] /= k
    return matrica


def w_k(matrica, k):
    return matrix_power(matrica, k)


def degroot():
    rebra=[[0, 2, 4], [0, 1, 2], [0, 3, 4], [1, 3, 2]]
    x0=[0, 0, 0, 5]
    orient = False
    iter = 10
    start = input('Если хотите ввести свои данные, напишите "1", иначе будет запущен базовый пример\n')
    if start == '1':
        vvod = input('Введите "1", если вводите ориентированный граф, а иначе что-то другое\n')
        if vvod == '1':
            orient = True
        print("Вводите информацию о ребрах как 3 целых числа без пробелов:  вершина1 вершина2 вес ребра")
        print("Когда закончите вводить ребра, напишите 0")
        line = input()
        rebra=[]
        kol_ver = 0
        while len(rebra) == 0 or line != "0":
            if len(rebra) == 0 and line == '0':
                print('Введите хотя бы одно ребро:')

            else:
                r = list(map(str, line.split(' ')))
                if len(r) != 3 or not(r[0].isdigit() and r[1].isdigit() and r[2].isdigit()):
                    print('Ошибка ввода, введите строку заново')
                else:
                    r[0], r[1], r[2] = int(r[0]), int(r[1]), int(r[2])
                    kol_ver = max(kol_ver, r[0], r[1])
                    rebra.append([r[0]-1, r[1]-1, r[2]])
            line = input()
        print("Введите начальное состояние для",  kol_ver, "вершин, перечисляя целые значения вершин без запятых через пробел")
        x0 = list(map(str, input().split(' ')))
        flag = (len(x0) == kol_ver)
        for i in x0:
            if not i.isdigit():
                flag = False
                break
        while not flag:
            print("Ошибка ввода, введите начальное состояние для",  kol_ver, "вершин заново")
            x0 = list(map(str, input().split(' ')))
            flag = (len(x0) == kol_ver)
            for i in x0:
                if not i.isdigit():
                    flag = False
                    break
        for i in range(len(x0)):
            x0[i] = int(x0[i])
        print("Введите количество итераций:")
        iter = input()
        while not iter.isdigit():
            print('Ошибка ввода, введите одно целое число')
            iter = input()
        iter = int(iter)

    w = matrix(rebra, orient)
    spisok_x = [x0]
    for i in range(iter):
        spisok_x.append(np.dot(w_k(w, i+1), x0))
    print('\n\nЗапуск модели DeGroot\nСостояния все вершин и их среднее на каждой итерации:\n')
    sostoinia = np.array(spisok_x).transpose()
    print('Начальное состояние')
    for el in spisok_x[0]:
        print("%.2f" % el, end='  ')
    print('\nсреднее значение:', "%.2f" % mean(spisok_x[0]), '\n')

    for i in range(1, len(spisok_x)):
        print('Итерация', i)
        for el in spisok_x[i]:
            print("%.6f" % el, end='  ')
        print('\nсреднее значение:', "%.2f" % mean(spisok_x[i]), '\n\n')
    plt.figure(figsize=(12, 7))
    x = range(len(spisok_x))
    for i in range(len(sostoinia)):
        plt.plot(x, sostoinia[i])
    plt.show()


print('Модель динамики мнений DeGroot.')
degroot()
