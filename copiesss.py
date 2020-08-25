# function for copy from MX_GPIO_Init data and parse this data

import clang.cindex
import jinja2
import binascii


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
        if c.location.file.name == filename:
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
    file = open("D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h", "r")
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

        # создание словаря с нужными параметрами и добаление в список (59)
        for j in range(len(a[1])):
            data_dict = {"PORTNAME": None, "PINNAME": None, "FUNCNAME": None, "IDKEY": None, "PIN": None}
            data_dict["PORTNAME"] = a[0]
            data_dict["PINNAME"] = a[1][j]
            data_dict["FUNCNAME"] = a[2]
            data_dict["IDKEY"] = hex(binascii.crc32(str.encode("STM32"+a[1][j])))
            data_dict["PIN"] = "P" + a[0][-1::] + pin_find(a[1][j], file)
            data_list_dict.append(data_dict)

    file.close()

    return data_list_dict


def pin_find(pin_name, file):
    """
    Парсинг номера пина, к кот. подключено устройство
    :param pin_name: str
    :param file: str
    :return: str
    """
    for line in file:
        if pin_name in line:
            simple_list = line.split()
            gpio_pin = simple_list[-1]
            simple_list = gpio_pin.split("_")
            gpio_pin = simple_list[-1]
            break

    return gpio_pin


def spi_devices(l_d):
    """
    Получение SPI устройств из основного словаря, полученного после парсинга main.c MX_GPIO_Init
    :param l_d: list (list of dicts with necessary parameters)
    :return: list (with one dict, which has spi devices)
    """
    spi_devices_list = []
    spi_dev = {"DEVICES": []}
    for i in l_d:
        if "SPI" in i["PINNAME"]:
            spi_dev["DEVICES"].append(i["PINNAME"][:-4])
    spi_devices_list.append(spi_dev)

    return spi_devices_list


def generation_powerbut_pins(data):
    """
    Генерирует по шаблону powerbut_pins
    :param l_d: list (list of dicts with necessary data from strings)
    :return: None
    """
    text_template = "./templates/powbut_templ.h"  # шаблон для автогенерации
    text = open(text_template).read()
    template = jinja2.Template(text)

    # генерация файла с классами для всех powerbuttons_pins
    f = open("./stm32_project/gpio_pins.h", "w")
    for i in range(len(data)):
        model = data[i]
        temp = template.render(model)
        f.writelines(temp)
        f.writelines("\n\n\n")
    f.close()

    return None


def generation_spi_chipselect(data):
    """
    Генерирует по шаблону spi_chipselect
    :param data: list (list of dict with spi devices)
    :return: None
    """
    text_template = "./templates/spi_chipselect_templ.h"  # шаблон для автогенерации
    text = open(text_template).read()
    template = jinja2.Template(text)
    model = data[0]
    temp = template.render(model)

    f = open("./stm32_project/spi_chipselect.h", "w")
    f.writelines(temp)
    f.close()

    return None


if __name__ == "__main__":

    # work_file = "D:\python\cubemx\Core\Src\main.c"
    # work_file = "D:\python\cubemx/all_powerbuttons\Core\Src\main.c"
    # work_file = "D:\python\cubemx/three_powerbuttons\Core\Src\main.c"
    work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"

    number_str = parser(work_file)  # парсим номера нужных строк в файле

    data_str = extract_string(work_file, number_str)  # извлечение нужных строк из заданного файла
    # print(data_str)

    l_d = work_with_nstr(data_str)  # работа со строками, получение списка словарей с данными
    # print(l_d)

    generation_powerbut_pins(l_d)  # функция, генерирующая файл по шаблону для powerbutton_pins

    l_s_d = spi_devices(l_d)  # какие устройства входят в spi
    # print(l_s_d)

    generation_spi_chipselect(l_s_d)  # функция, генерирующая файл по шаблону для spi_chipselect
