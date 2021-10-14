import csv


def read_file(file: str) -> list:
    """
    Функция принимает на вход название csv файла, считывает
    и создает список состоящий из словарей с данными сотрудников.
    """
    with open(file, newline = '', encoding = 'utf8') as csvfile:
        row_data = csv.reader(csvfile, delimiter = ';')
        data1 = []
        for row in row_data:
            data1.append(row)
        name_col = data1[0]
        data = []
        for row in data1[2::2]:
            data.append({name_col[i]: row[i] for i in range(len(name_col))})
    return data


def task(data: list) -> None:
    """
    Функция считывает команду и выполняет одну из трёх фукнций:
    вывести иерархию команд,
    вывести сводный отчёт по отделам,
    сохранить сводный отчёт в csv-файл
    """
    print('Здравствуйте! Выберете, пожалуйста, одну из следующих опций:\n'
          '(1) Dывести иерархию команд \n'
          '(2) Вывести сводный отчёт по отделам \n'
          '(3) Сохранить сводный отчёт в csv-файл'
          )
    option = ''
    options = {'1': departments_info, '2': display_report, '3': save_report}
    while option not in options:
        print('Выберите: {}/{}/{}'.format(*options))
        option = input()
    return options[option](data)


def departments_info(data: list, show: bool = True):
    departaments = []
    for row in data:
        departaments.append(row['Департамент'])
    departaments = set(departaments)
    depart_otdel = {x: [] for x in departaments}
    for row in data:
        if row['Отдел'] not in depart_otdel[row['Департамент']]:
            depart_otdel[row['Департамент']].append(row['Отдел'])
    if show:
        s = "|" + "{:^20} |"
        for dep in depart_otdel.keys():
            print(s.format(dep), end='')
            for i in depart_otdel[dep]:
                print(s.format(i), end='')
            print()
    return depart_otdel


def display_report(data: list, show: bool = True) -> list:
    """
    Функция выводит статистику по департаментам:
    Количестов сотрудников,
    Минимальный оклад,
    Максимальный оклад,
    Средний оклад
    """
    departaments = departments_info(data, show = False).keys()

    numbers = {k: 0 for k in departaments}
    maximum = {k: 0 for k in departaments}
    minimum = {k: 10000000 for k in departaments}
    summa = {k: 0 for k in departaments}

    for person in data:
        numbers[person['Департамент']] += 1

        if maximum[person['Департамент']] < int(person['Оклад']):
            maximum[person['Департамент']] = int(person['Оклад'])

        if minimum[person['Департамент']] > int(person['Оклад']):
            minimum[person['Департамент']] = int(person['Оклад'])

        summa[person['Департамент']] += int(person['Оклад'])

    average = {k: int(round(summa[k] / numbers[k], -2)) for k in departaments}

    all_dep = [[k, numbers[k], maximum[k], minimum[k], average[k]]
               for k in departaments]

    if show:
        s = "|" + "{:^18} | " * 5
        print(s.format('Название', 'Число сотрудников', 'MAX оклад', 'MIN оклад', 'Средний оклад'))
        print('-' * 41 + '$' * 64)
        for dep in all_dep:
            print(s.format(*dep))
    return all_dep


def save_report(data: list):
    dep = display_report(data, show = False)
    columns = ['Название', 'Число сотрудников', 'MAX оклад', 'MIN оклад', 'Средний оклад']
    with open('ans.csv', 'w') as file:
        out_file = csv.writer(file, delimiter=';')
        out_file.writerow(columns)
        out_file.writerows(dep)


if __name__ == '__main__':
    my_file = 'Corp Summary.csv'
    my_data = read_file(my_file)
    task(my_data)
