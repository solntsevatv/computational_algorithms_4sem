def read_table():
    """
        Чтение таблицы из файла "test.txt", также оттуда считываются n и х
    """
    x_tbl = [] 
    y_tbl = [] 
    z_tbl = []
    f = open('test.txt')
    txt_table = f.read()
    txt_table = txt_table.replace(",", ".")
    txt_table = txt_table.split("\n")
    tbl_len = len(txt_table)
    if txt_table[tbl_len - 1] == '':
        txt_table.pop(tbl_len - 1)
        tbl_len -= 1

    x_tbl.extend(txt_table[0].split())
    for i in range(len(x_tbl)):
        x_tbl[i] = float(x_tbl[i])
    for i in range(1, tbl_len - 2):
        tbl_str = txt_table[i].split()
        y_tbl.append(float(tbl_str[0]))
        z_tbl.append([])
        for j in range(1, len(tbl_str)):
            z_tbl[i - 1].append(float(tbl_str[j]))

    tbl_str = txt_table[tbl_len - 2].split()
    n_x, n_y = float(tbl_str[0]), float(tbl_str[1])
    tbl_str = txt_table[tbl_len - 1].split()
    x, y  = float(tbl_str[0]), float(tbl_str[1])
    return x_tbl, y_tbl, z_tbl, n_x, n_y, x, y


def find_nearest(x_tbl, n, x):
    """
        Возвращение таблиц для n узлов
    """
    curr_ind = 0
    for i in range(1, len(x_tbl)):
        if (abs(x - x_tbl[i]) <= abs(x - x_tbl[i - 1])):
            curr_ind = i

    left = n // 2
    right = left - (n % 2 + 1) % 2

    while (curr_ind - left < 0):
        left -= 1
        right += 1

    while(curr_ind + right > len(x_tbl) - 1):
        right -= 1
        left += 1

    x_table = x_tbl[int(curr_ind - left):int(curr_ind + right) + 1]

    return x_table

def create_dif_tbl(x_table, y_table, n):
    """
        Создание таблицы разделенных разностей
    """
    dif_tbl = []
    dif_tbl.append(y_table)
    for i in range(int(n)):
        tmp = []
        for j in range(int(n) - i):
            if (abs(x_table[j] - x_table[j + i + 1]) > 1e-6):
                tmp.append((dif_tbl[i][j] - dif_tbl[i][j + 1]) / (x_table[j] - x_table[j + i + 1]))
        dif_tbl.append(tmp)
    return dif_tbl

def count_polynomial(n, x, x_table, dif_tbl):
    """
        Вычисление полинома
    """
    result = dif_tbl[0][0]
    for i in range(1, int(n) + 1):
        multiple = 1
        for j in range(i):
            multiple *= (x - x_table[j])
        result += (dif_tbl[i][0] * multiple)
    return result

def interpolate(table_x, table_y, n, x):
    """
        Построение интерполяционного полинома Ньютона
    """
    dif_tbl = create_dif_tbl(table_x, table_y, n)
    return count_polynomial(n, x, table_x, dif_tbl)

def interpolate_multi(x_tbl, y_tbl, z_tbl, n_x, n_y, x, y):
    x_table = find_nearest(x_tbl, n_x + 1, x)
    y_table = find_nearest(y_tbl, n_y + 1, y)

    start_ind = y_tbl.index(y_table[0])
    z_table = z_tbl[start_ind:start_ind+len(y_table)]

    start_ind = x_tbl.index(x_table[0])
    for i in range(int(n_y) +  1):
        z_table[i] = z_table[i][start_ind:start_ind+len(x_table)]

    x_first = []
    for i in range(int(n_y) + 1):
        x_first.append(interpolate(x_table, z_table[i], n_x, x))
    y_res = interpolate(y_table, x_first, len(x_first) - 1, y)
    return y_res


def main():
    try:
        x_tbl, y_tbl, z_tbl, n_x, n_y, x, y = read_table()
    except IndexError:
        print("Something wrong with the file test.txt")
        return
    except FileNotFoundError:
        print("File not found")
        return

    y_res = interpolate_multi(x_tbl, y_tbl, z_tbl, n_x, n_y, x, y)
    print(y_res)

if __name__ == "__main__":
    main()