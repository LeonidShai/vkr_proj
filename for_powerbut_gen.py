import clang.cindex
import binascii
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

    num_str_write_pin = []  # список для номеров строк write_pin
    num_str_init = []  # список для номеров строк init_struct

    for c in node.get_children():
        if c.location.file.name == filename:
            # print(c.spelling, c.location.line)  # for test
            if c.spelling == "MX_GPIO_Init":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling)  # for test
                        if k.spelling == "HAL_GPIO_WritePin":
                            num_str_write_pin.append(k.location.line)
                        elif k.spelling == "Pin":
                            num_str_init.append(k.location.line)

    return num_str_write_pin, num_str_init


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
            data_str.append(lines[i-1].lstrip() + lines[i].lstrip())
        else:
            data_str.append(lines[i-1].lstrip())
    file.close()

    return data_str


def extract_initstruct(filename, num_str):
    """
    получаем InitStruct из main.c целиком все строки
    :param filename: str (имя файла)
    :param num_str: list (номера строк, с началом конструкций InitStruct)
    :return: list (список словарей, в каждом словаре один ключ со списком строк)
    """
    data_str_list = []
    file = open(filename, 'r')
    lines = file.read().splitlines()

    for i in num_str:
        s = i
        dict_data_str = {"INITS": []}
        while not "HAL_GPIO_Init" in lines[s]:
            if lines[s][-1] != ";":
                dict_data_str["INITS"].append(lines[s].lstrip() + lines[s+1].lstrip())
            else:
                dict_data_str["INITS"].append(lines[s].lstrip())
            s += 1
        data_str_list.append(dict_data_str)

    file.close()
    return data_str_list


def work_with_nstr(data_str, data_init):
    """
    Получение словаря из строки: {"portname": None, "pinport": None, "funcname": None}
    :param data_str: list (strings)
    :param data_init: list(strings of InitStruct)
    :return: list (list of dicts with necessary parameters)
    """

    data_list_dict = []  # список для словарей с требуемыми параметрами
    # получение из каждой строки подстроки в скобках
    file = open("D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h", "r")
    for stroka in data_str:
        schet = 0  # счетчик, нужен для data_dict["INITS"]
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
            data_dict = {"PORTNAME": None, "PINNAME": None, "FUNCNAME": None, "IDKEY": None, "PIN": None, "INITS": None}
            data_dict["PORTNAME"] = a[0]
            data_dict["PINNAME"] = a[1][j]
            data_dict["FUNCNAME"] = a[2]
            data_dict["IDKEY"] = hex(binascii.crc32(str.encode("STM32"+a[1][j])))
            data_dict["PIN"] = "P" + a[0][-1::] + pin_find(a[1][j], file)
            data_dict["INITS"] = data_init[schet]["INITS"]
            data_list_dict.append(data_dict)

        schet += 1

    file.close()

    return data_list_dict


def pin_find(pin_name, file):
    """
    Парсинг номера пина, к кот. подключено устройство
    :param pin_name: str
    :param file: str (уже открытый файл)
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


if __name__ == "__main__":

    main_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"

    num_hal_write, num_init = parser(main_work_file)
    # print(num_hal_write, num_init)

    data_str = extract_string(main_work_file, num_hal_write)
    # print(data_str)

    data_init = extract_initstruct(main_work_file, num_init)
    # print(data_init)

    data_list_dict = work_with_nstr(data_str, data_init)
    print(data_list_dict)

    generation_powerbut_pins(data_list_dict)
