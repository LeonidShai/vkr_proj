# function for copy from MX_GPIO_Init data and parse this data

import clang.cindex
import jinja2


def parser(filename):
    """
    Парсит номерa строк в файле с требуемыми функциями
    :param node: str (filename)
    :return: list (string's numbers)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []  # список для номеров строк

    for c in node.get_children():
        if c.location.file.name == work_file:
            # print(c.spelling, c.location.line)  # for test
            if c.spelling == "MX_GPIO_Init":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling)  # for test
                        if k.spelling == "HAL_GPIO_WritePin":
                            num_str.append(k.location.line)

    return num_str


def extract_string(filename, num_str):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for i in num_str:
        if lines[i - 1][-1] != ";":
            data_str.append(lines[i-1] + lines[i].lstrip())
        else:
            data_str.append(lines[i-1])
    file.close()

    return data_str


def work_with_nstr(data_str):
    """
    Получение словаря из строки: {"portname": None, "pinport": None, "funcname": None}
    :param data_str: list (strings)
    :return: list (list of dicts with necessary parameters)
    """

    data_list_dict = []  # список для словарей с требуемыми параметрами
    # получение из каждой строки подстроки в скобках
    for stroka in data_str:
        s = int()
        e = int()
        for i in range(len(stroka)):
            if stroka[i] == "(":
                s = i+1
            elif stroka[i] == ")":
                e = i

        # разделение полученной подстроки на параметры
        a = stroka[s:e].split(", ")  # list of strings, with splitting
        a[1] = a[1].split("|")

        # создание слваря с нужными параметрами и добаление в список (59)
        for j in range(len(a[1])):
            data_dict = {"portname": None, "pinport": None, "funcname": None}
            data_dict["portname"] = a[0]
            data_dict["pinport"] = a[1][j]
            data_dict["funcname"] = a[2]
            data_list_dict.append(data_dict)

    return data_list_dict


def generation_powerbuttons_pins(l_d):
    """
    Генерирует по шаблону file.c
    :param l_d: list (list of dicts with necessary data from strings)
    :return: None
    """
    text_template = "D:\python/vkr/tasks\jij_test_templ.c"  # шаблон для автогенерации
    text = open(text_template).read()
    template = jinja2.Template(text)

    # генерация файла с классами для всех powerbuttons_pins
    for i in range(len(l_d)):
        model = l_d[i]
        temp = template.render(model)
        f = open("test_jiji.c", "a")
        f.writelines(temp)
        f.writelines("\n\n\n")
        f.close()

    return None


if __name__ == "__main__":

    # work_file = "D:\python\cubemx\Core\Src\main.c"
    work_file = "D:\python\cubemx/all_powerbuttons\Core\Src\main.c"
    # work_file = "D:\python\cubemx/three_powerbuttons\Core\Src\main.c"

    number_str = parser(work_file)  # парсим номера нужных строк в файле

    data_str = extract_string(work_file, number_str)  # извлечение нужных строк из заданного файла
    # print(data_str)

    l_d = work_with_nstr(data_str)  # работа со строками, получение списка словарей с данными
    # print(l_d)

    generation_powerbuttons_pins(l_d)  # функция, генерирующая файл по шаблону
