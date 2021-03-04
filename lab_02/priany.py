import numpy as np

X_TABLE = [0, 1, 2, 3, 4]
Y_TABLE = [0, 1, 2, 3, 4]
Z_TABLE = [[0, 1, 4, 9, 16], [1, 2, 5, 10, 17], [4, 5, 8, 13, 20], [9, 10, 13, 18, 25], [16, 17, 20, 25, 32]]

# Функция подсчёта разделённой разности по заданным индексам

# x_table, y_table - таблицы значений

# list_indexes - индексы элементов, с которыми работаем
# Возвращает численный результат
def difference(x_table, y_table, list_indexes):
    result = 0
    length = len(list_indexes)

    # Если всего два элемента
    if (length == 2):

        # Элементы для подсчёта разделённой разности различны
        if (list_indexes[0] != list_indexes[1]):
            delta_y = y_table[list_indexes[0]] - y_table[list_indexes[1]]
            delta_x = x_table[list_indexes[0]] - x_table[list_indexes[1]]
            result = delta_y / delta_x
    # Если элементов больше, то подсчитываем через рекурсию
    elif (length > 2):
        dif_first = difference(x_table, y_table, list_indexes[:length - 1])
        dif_second = difference(x_table, y_table, list_indexes[1:])
        result = (dif_first - dif_second) / (x_table[list_indexes[0]] - x_table[list_indexes[length - 1]])
    return result

# Функция подсчёта коэффициентов для построения полиномов
# x_table, y_table - таблицы значений
# list_indexes - индексы элементов, с которыми работаем
# Возвращает массив коэффициентов для полинома
def count_polinom_diff_coefs(x_table, y_table, list_indexes):
    result_coefs = []
    for i in range(2, len(list_indexes) + 1):
        result_coefs.append(difference(x_table, y_table, list_indexes[:i]))
    return result_coefs

# Функция подсчёта значения полинома
# x_table, y_table - таблицы значений
# list_indexes - индексы элементов, с которыми работаем
# x_var - переменная, для которой ищем значение у апроксимирующей функции
# Возвращает результат по заданному x
def count_polinom_value(x_table, y_table, x_var, list_indexes):
    coefs = count_polinom_diff_coefs(x_table, y_table, list_indexes)
    x_multiply = 1
    result = y_table[list_indexes[0]]
    for i in range(len(list_indexes) - 1):
        x_multiply *= (x_var - x_table[list_indexes[i]])
        result += (x_multiply * coefs[i])
    return result

def find_near_index(x_var, x_table):
    length_table = len(x_table)
    index = 0
    while ((index < length_table) and (x_table[index] < x_var)):
        index += 1
    return index

def create_list_indexes_newton(x_var, n, x_table):
    index = find_near_index(x_var, x_table)
    list_indexes = np.array(list(range(index - ((n // 2) + 1), index - ((n // 2) + 1) + n + 1)))
    while (list_indexes[0] < 0):
        list_indexes += 1
    while (list_indexes[list_indexes.shape[0] - 1] >= len(x_table)):
        list_indexes -= 1
    return list(list_indexes)

def mul_polinom(x_table, y_table, z_table, nx, ny, x_var, y_var):
    index_x = create_list_indexes_newton(x_var, nx, x_table)
    index_y = create_list_indexes_newton(y_var, ny, y_table)

    x_table = x_table[index_x[0] : index_x[len(index_x) - 1] + 1]
    y_table = y_table[index_y[0] : index_y[len(index_y) - 1] + 1]
    z_table = z_table[index_y[0] : index_y[len(index_y) - 1] + 1]

    for i in range(ny + 1):
        z_table[i] = z_table[i][index_x[0] : index_x[len(index_x) - 1] + 1]

    print(x_table)
    print(y_table)
    print(z_table)
    print()
    x_first = []
    for i in range(ny + 1):
        x_first.append(count_polinom_value(x_table, z_table[i], x_var, list(range(nx + 1))))
    y_res = count_polinom_value(y_table, x_first, y_var, list(range(len(x_first))))
    print(x_first)

    return y_res

x = float(input("Введите x: "))
y = float(input("Введите y: "))
nx = int(input("Введите nx: "))

ny = int(input("Введите ny: "))

print(mul_polinom(X_TABLE, Y_TABLE, Z_TABLE, nx, ny, x, y))