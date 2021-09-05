# парсинг и генерация spi_chipselect, IdPeripheral, MyFactoryPeripheral

import clang.cindex
import jinja2


def protocol_checker(filename):
    """
    Проверка наличия протоколов Pin, I2C, SPI, UART
    :param node: clang.cindex.node
    :param filename: str
    :return: list
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    protocol_check_list = []

    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "main":
                for i in c.get_children():
                    for k in i.get_children():
                        if k.spelling and k.spelling != "HAL_Init" and k.spelling != "SystemClock_Config":
                            protocol_check_list.append(k.spelling)

    return protocol_check_list


def take_need_protocols(protocols):
    """
    Выбор протоколов UART, I2C, если имеются
    :param protocols: list
    :return: list (ex: [I2C1, UART1, I2C2, UART2])
    """
    need_protocols = []
    for elem in protocols:
        if "I2C" in elem:
            need_protocols.append(elem[3:-5])
        elif "UART" in elem:
            need_protocols.append(elem[10:-5]+elem[8])

    return need_protocols


def quant_prot(protocols):
    """
    Разделение на отдельные списки протоколов
    :param protocols: list
    :return: list (names protocols)
    """
    quant_prot = []

    for elem in protocols:
        if "GPIO" in elem and not "GPIO" in quant_prot:
            quant_prot.append("Pin")
        elif "I2C" in elem and not "I2C" in quant_prot:
            quant_prot.append("I2C")
        elif "SPI" in elem and not "SPI" in quant_prot:
            quant_prot.append("SPI")
        elif "UART" in elem and not "UART" in quant_prot:
            quant_prot.append("UART")

    return quant_prot


def parser(filename):
    """
    Парсит номерa строк в файле с требуемыми функциями из main.c
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
    Извлекает строку/строки из файла по полученным номерам строк
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


def work_with_nstr(data_str, filename):
    """
    Получение словаря из строки: {"pinname": None}
    :param data_str: list (strings)
    :return: list (list of dicts with necessary parameters)
    """

    data_list_dict = []  # список для словарей с требуемыми параметрами
    # получение из каждой строки подстроки в скобках
    file = open(filename, "r")
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
            data_dict = {"PINNAME": None}
            data_dict["PINNAME"] = a[1][j]
            data_list_dict.append(data_dict)

    file.close()

    return data_list_dict


def spi_devices(l_d):
    """
    Получение SPI устройств из основного словаря, полученного после парсинга main.c MX_GPIO_Init
    :param l_d: list (list of dicts with necessary parameters)
    :return: list (with one dict, which has spi devices)
    """
    spi_devices_list = []
    spi_dev = {"DEVICES": [], "CH": None}
    for i in l_d:
        if "SPI" in i["PINNAME"]:
            spi_dev["DEVICES"].append(i["PINNAME"][:-4])
    spi_dev["CH"] = len(spi_dev["DEVICES"])
    spi_devices_list.append(spi_dev)

    return spi_devices_list


def dict_for_myfactory_perips(all_dev, quant_prot):
    """
    Подготовка словаря для генерации MyFactoryPeripheral
    :param all_dev: list (список полученных данных)
    :param quant_prot: list (список протоколов)
    :return: dict (словарь данных)
    """
    dict_on_protocols = dict()
    for elem in quant_prot:
        dict_on_protocols[elem] = []

    for elem in all_dev[0]["DEVICES"]:
        if "SPI" in elem:
            dict_on_protocols["SPI"].append(elem)
        elif "I2C" in elem:
            dict_on_protocols["I2C"].append(elem)
        elif "UART" in elem:
            dict_on_protocols["UART"].append(elem)
        else:
            dict_on_protocols["Pin"].append(elem)

    return dict_on_protocols


def data_unification(l1, l2):
    """
    Объединение двух списков данных в один
    :param l1: list (полученные порты из main.c)
    :param l2: list (протоколы UART и I2C)
    :return:
    """
    devices_list = []
    dev = {"DEVICES": [], "CH": None}
    for i in l1:
        dev["DEVICES"].append(i["PINNAME"][:-4])
    for i in l2:
        dev["DEVICES"].append(i)
    dev["CH"] = len(dev["DEVICES"])
    devices_list.append(dev)
    return devices_list


def generation_spi_chipselect(text_template, data):
    """
    Генерирует по шаблону spi_chipselect и IdPeripheral
    :param data: list (list of dict with spi devices)
    :return: None
    """
    # text_template = "./templates/spi_chipselect_templ.h"  # шаблон для автогенерации
    text = open(text_template).read()
    template = jinja2.Template(text)
    model = data[0]
    temp = template.render(model)

    if "chipselect_templ" in text_template:
        f = open("./stm_project/spi_chipselect.h", "w")
        f.writelines(temp)
        f.close()
    elif "chipselect.cpp" in text_template:
        f = open("./stm_project/src/spi_chipselect.cpp", "w")
        f.writelines(temp)
        f.close()
    elif "peripheral_templ.cpp" in text_template:
        f = open("./stm_project/src/id_periherial.cpp", "w")
        f.writelines(temp)
        f.close()
    else:
        f = open("./stm_project/id_periherial.h", "w")
        f.writelines(temp)
        f.close()

    return None


def generation_myfactory_periph(data):
    """
    Генерация MyFactoryPeripheral
    :param data: dict (Словарь с данными)
    :return: None
    """
    text_template = "./templates/myfactory_peripherals.h"
    text = open(text_template).read()
    template = jinja2.Template(text)
    model = {"PERIPS": data}
    temp = template.render(model)

    f = open("./stm_project/my_factory_peripherals.h", "w")
    f.writelines(temp)
    f.close()

    return None


def maybe_main(mainc_work_file, inc_main_file):
    """
    Основная функция, парсинг и генерация spi_chipselect, IdPeripheral, MyFactoryPeripheral
    :param mainc_work_file: str (main.c)
    :param inc_main_file: str (main.h)
    :return:
    """
    text_template_spi_chipselect = "./templates/spi_chipselect_templ.h"
    text_template_id_periherial = "./templates/Periherial_id_templ.h"
    text_template_id_periherial_cpp = "./templates/id_peripheral_templ.cpp"
    text_template_spi_chipselect_cpp = "./templates/spi_chipselect.cpp"
    
    number_str = parser(mainc_work_file)  # парсим номера нужных строк в файле main.c

    protocols = protocol_checker(mainc_work_file)  # получение названия всех протоколов
    # print(protocols)
    quant_protocols = quant_prot(protocols)  # определение существующих протоколов
    # print(quant_protocols)

    data_str = extract_string(mainc_work_file, number_str)  # извлечение нужных строк из заданного файла main.c
    # print(data_str)

    l_d = work_with_nstr(data_str, inc_main_file)  # работа со строками, получение списка словарей с данными
    # print(l_d)

    if "SPI" in quant_protocols:
        l_s_d = spi_devices(l_d)  # какие устройства входят в spi
        # print(l_s_d)
        generation_spi_chipselect(text_template_spi_chipselect, l_s_d)  # функция, генерирующая spi_chipselect.h
        generation_spi_chipselect(text_template_spi_chipselect_cpp, l_s_d)  # функция, генерирующая spi_chipselect.cpp
        
    need_protocols = take_need_protocols(protocols)  # выделение UART-ов и I2C-протоколов
    # print(need_protocols)
    all_dev = data_unification(l_d, need_protocols)  # объединение с SPI и powerbutt протоколов UART, I2C
    # print(all_dev)

    generation_spi_chipselect(text_template_id_periherial, all_dev)  # генерация IdPeriherial.h
    generation_spi_chipselect(text_template_id_periherial_cpp, all_dev)  # генерация IdPeriherial.cpp

    dict_for_myfact = dict_for_myfactory_perips(all_dev, quant_protocols)
    # подготовка данных для шаблона MyFactoryPeripherals
    # print(dict_for_myfact)

    generation_myfactory_periph(dict_for_myfact)  # генерация MyFactoryPeripherals

    return None


if __name__ == "__main__":

    # mainc_work_file = "D:\python\my_pin\Core\Src\main.c"
    mainc_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    # hal_msp_work_file = "D:\python\my_pin\Core\Src\stm32f1xx_hal_msp.c"
    hal_msp_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    inc_main_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h"

    maybe_main(mainc_work_file, inc_main_file)
