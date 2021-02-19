def read_table():
    """
        Чтение таблицы из файла "test.txt", также оттуда считываются n и х
    """
    x_tbl = [] 
    y_tbl = [] 
    dy_tbl = []
    f = open('test.txt')
    txt_table = f.read()
    txt_table = txt_table.replace(",", ".")
    txt_table = txt_table.split()
    tbl_len = len(txt_table)
    for i in range(int((tbl_len - 2)/ 3)):
        x_tbl.append(float(txt_table[3* i]))
        y_tbl.append(float(txt_table[3 * i + 1]))
        dy_tbl.append(float(txt_table[3 * i + 2]))
    n = float(txt_table[tbl_len - 2])
    x = float(txt_table[tbl_len - 1])
    return x_tbl, y_tbl, dy_tbl, n, x


def insertion_sort_tbl(x_tbl, y_tbl, dy_tbl):
    """
        Сортировка таблицы значений х и по ней сортировка значений у, у'
    """
    for i in range(1, len(x_tbl)):
        key = x_tbl[i]
        y_key = y_tbl[i]
        dy_key = dy_tbl[i]

        j = i-1
        while j >=0 and key < x_tbl[j] :
            x_tbl[j + 1] = x_tbl[j]
            y_tbl[j + 1] = y_tbl[j]
            dy_tbl[j + 1] = dy_tbl[j]
            j -= 1

        x_tbl[j + 1] = key 
        y_tbl[j + 1] = y_key
        dy_tbl[j + 1] = dy_key
    return x_tbl, y_tbl, dy_tbl

def find_nearest_x(x_tbl, y_tbl, dy_tbl, n, x):
    """
        Возвращение таблиц для n узлов
    """
    curr_ind = 0
    for i in range(1, len(x_tbl)):
        if (abs(x - x_tbl[i]) < x - x_tbl[i - 1]):
            curr_ind = i

    left = n // 2
    right = left - (n % 2 + 1) % 2

    while (curr_ind - left < 0):
        left -= 1
        right += 1
        print(1)

    while(curr_ind + right > len(x_tbl) - 1):
        right -= 1
        left += 1
        print(2)

    x_table = x_tbl[int(curr_ind - left):int(curr_ind + right) + 1]
    y_table = y_tbl[int(curr_ind - left):int(curr_ind + right) + 1]
    dy_table = dy_tbl[int(curr_ind - left):int(curr_ind + right) + 1]

    return x_table, y_table, dy_table

def double_list(arr):
    """
        Дублирование каждого значения в списке
    """
    n = len(arr)
    for i in range(n):
        arr.insert(i + 2 * i, arr[2 * i])

def create_dif_tbl(x_table, y_table, dy_table, n):
    """
        Создание таблицы разделенных разностей
    """
    dif_tbl = []
    dif_tbl.append(y_table)
    for i in range(n):
        tmp = []
        for j in range(n - i):
            if (abs(x_table[j] - x_table[j + i + 1]) < 1e-6):
                tmp.append(dy_table[j // 2])
            else:
                tmp.append((dif_tbl[i][j] - dif_tbl[i][j + 1]) / (x_table[j] - x_table[j + i + 1]))
        dif_tbl.append(tmp)
    return dif_tbl

def count_polynomial(n, x, x_table, dif_tbl):
    """
        Вычисление полинома
    """
    result = dif_tbl[0][0]
    for i in range(1, n + 1):
        multiple = 1
        for j in range(i):
            multiple *= (x - x_table[j])
        result += (dif_tbl[i][0] * multiple)
    return result

def interpolate_newton(x_tbl, y_tbl, dy_tbl, n, x):
    """
        Построение интерполяционного полинома Ньютона
    """
    x_table, y_table, dy_table = find_nearest_x(x_tbl, y_tbl, dy_tbl, n + 1, x)
    dif_tbl = create_dif_tbl(x_table, y_table,  dy_table, n)
    return count_polynomial(n, x, x_table, dif_tbl)

def interpolate_hermit(x_tbl, y_tbl, dy_tbl, n, x):
    """
        Построение интерполяционного полинома Эрмита
    """
    x_table, y_table, dy_table = find_nearest_x(x_tbl, y_tbl, dy_tbl, n // 2 + 1, x)

    double_list(x_table)
    if (n % 2 == 0):
        x_table.pop()

    double_list(y_table)
    if (n % 2 == 0):
        y_table.pop()

    dif_tbl = create_dif_tbl(x_table, y_table, dy_table, n)
    return count_polynomial(n, x, x_table, dif_tbl)


def main():
    try:
        x_tbl, y_tbl, dy_tbl, n, x = read_table()
    except IndexError:
        print("Something wrong with the file test.txt")
        return
    except FileNotFoundError:
        print("File not found")
        return

    x_tbl, y_tbl, dy_tbl = insertion_sort_tbl(x_tbl, y_tbl, dy_tbl)

    print(f"For n = {int(n)}, x = {x}:")

    result = interpolate_newton(x_tbl, y_tbl, dy_tbl, int(n), x)
    print("Newton: {:.6f}".format(result))

    result = interpolate_hermit(x_tbl, y_tbl, dy_tbl, int(n), x)
    print("Hermit: {:.6f}".format(result))

if __name__ == "__main__":
    main()