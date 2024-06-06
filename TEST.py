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
    fig, axs = plt.subplots(3, 3, figsize=(15, 15))
    fig.suptitle('DeGroot Dynamics for Graphs')
    ind = 0
    place_on_graph = 0
    while ind != len(lines):
        #print(lines[ind][:-1])
        out.write(lines[ind])
        ind += 1
        rebra=[[0, 2, 4], [0, 1, 2], [0, 3, 4], [1, 3, 2]]
        x0=[0, 0, 0, 5]
        orient = False
        iter = 10
        out.write('Если хотите ввести свои данные, напишите "1", иначе будет запущен базовый пример\n')
        start = lines[ind][:-1]
        out.write(lines[ind])
        ind += 1
        if start == '1':
            out.write('Введите "1", если вводите ориентированный граф, а иначе что-то другое\n')
            vvod = lines[ind][:-1]
            out.write(lines[ind])
            ind += 1
            if vvod == '1':
                orient = True
            out.write("Вводите информацию о ребрах как 3 целых числа без пробелов:  вершина1 вершина2 вес ребра\n")
            out.write("Когда закончите вводить ребра, напишите 0\n")
            line = lines[ind][:-1]
            out.write(lines[ind])
            ind += 1
            rebra=[]
            kol_ver = 0
            while len(rebra) == 0 or line != "0":
                if len(rebra) == 0 and line == '0':
                    out.write('Введите хотя бы одно ребро:\n')
                else:
                    r = list(map(str, line.split(' ')))
                    if len(r) != 3 or not(r[0].isdigit() and r[1].isdigit() and r[2].isdigit()):
                        out.write('Ошибка ввода, введите строку заново\n')
                    else:
                        r[0], r[1], r[2] = int(r[0]), int(r[1]), int(r[2])
                        kol_ver = max(kol_ver, r[0], r[1])
                        rebra.append([r[0]-1, r[1]-1, r[2]])
                line = lines[ind][:-1]
                out.write(lines[ind])
                ind += 1
            out.write("Введите начальное состояние для"+ str(kol_ver) + "вершин, перечисляя целые значения вершин без запятых через пробел\n")
            x0 = list(map(str, lines[ind][:-1].split(' ')))
            out.write(lines[ind])
            ind += 1
            flag = (len(x0) == kol_ver)
            for i in x0:
                if not i.isdigit():
                    flag = False
                    break
            while not flag:
                out.write("Ошибка ввода, введите начальное состояние для" + str(kol_ver) +"вершин заново\n")
                x0 = list(map(str, lines[ind][:-1].split(' ')))
                out.write(lines[ind])
                ind += 1
                flag = (len(x0) == kol_ver)
                for i in x0:
                    if not i.isdigit():
                        flag = False
                        break
            for i in range(len(x0)):
                x0[i] = int(x0[i])
            out.write("Введите количество итераций:\n")
            iter = lines[ind][:-1]
            out.write(lines[ind])
            ind += 1
            while not iter.isdigit():
                out.write('Ошибка ввода, введите одно целое число')
                iter = lines[ind][:-1]
                out.write(lines[ind])
                ind += 1
            iter = int(iter)

        w = matrix(rebra, orient)
        spisok_x = [x0]
        for i in range(iter):
            spisok_x.append(np.dot(w_k(w, i+1), x0))
        out.write('\n\nЗапуск модели DeGroot\nСостояния все вершин и их среднее на каждой итерации:\n')
        sostoinia = np.array(spisok_x).transpose()
        out.write('Начальное состояние\n')
        for el in spisok_x[0]:
            out.write(str(round(el, 2))+' ')
        out.write('\nсреднее значение: ' + str(round(mean(spisok_x[0]), 2)) + '\n\n')

        for i in range(1, len(spisok_x)):
            out.write('Итерация ' + str(i)+'\n')
            for el in spisok_x[i]:
                out.write(str(round(el, 2))+' ')
            out.write('\nсреднее значение: '+ str(round(mean(spisok_x[i]), 2)) +'\n\n')
        #plt.figure(figsize=(12, 7))
        #x = range(len(spisok_x))
        #for i in range(len(sostoinia)):
        #    plt.plot(x, sostoinia[i])
        #plt.show()
        out.write('---------------------------------------------\n\n')

        spisok_x = []
        for k in range(iter):
            spisok_x.append(np.dot(matrix_power(w, k + 1), x0))
        sostoinia = np.array(spisok_x).transpose()
        x = range(iter)
        for node_states in sostoinia:
            axs[place_on_graph // 3, place_on_graph % 3].plot(x, node_states)
        place_on_graph += 1
    plt.show()

    file.close()

for i in range(2):
    with open(f'test{i+1}.txt', 'r') as file:
        lines = file.readlines()
        print('Модель динамики мнений DeGroot.')
        with open(f"otus{i+1}.txt", "w") as out:
            degroot()
