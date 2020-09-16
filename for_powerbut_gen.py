import clang.cindex
import binascii
import jinja2

import f_pow_gen_secondpart  # для powerbuttons
import spi_dev_gen  # для генерации spi_devs
import i2c_gen  # для генерации i2c_devs и uart_devs


def quant_prot(protocols):
    """
    Разделение на отдельные списки протоколов
    :param protocols: list
    :return: list (names protocols)
    """
    quant_prot = []

    for elem in protocols:
        if "GPIO" in elem and not "GPIO" in quant_prot:
            quant_prot.append("GPIO")
        elif "I2C" in elem and not "I2C" in quant_prot:
            quant_prot.append("I2C")
        elif "SPI" in elem and not "SPI" in quant_prot:
            quant_prot.append("SPI")
        elif "UART" in elem and not "UART" in quant_prot:
            quant_prot.append("UART")

    return quant_prot


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


def work_with_nstr(data_str, data_init, file_inc):
    """
    Получение словаря из строки: {"portname": None, "pinport": None, "funcname": None}
    :param data_str: list (strings)
    :param data_init: list(strings of InitStruct)
    :return: list (list of dicts with necessary parameters)
    """

    data_list_dict = []  # список для словарей с требуемыми параметрами
    # получение из каждой строки подстроки в скобках
    # file = open("D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h", "r")
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
            data_dict = {a[1][j]: {"PORTNAME": None, "CLCEN": None, "PINNAME": None, "IDKEY": None,
                                   "PIN": None, "INITS": None}}
            data_dict[a[1][j]]["PORTNAME"] = a[0]
            if len(a[0]) > 5:
                port = port_finder(a[0], file_inc)
                data_dict[a[1][j]]["CLCEN"] = port
                data_dict[a[1][j]]["PIN"] = "P" + port[-1] + pin_find(a[1][j], file_inc)
            else:
                data_dict[a[1][j]]["CLCEN"] = a[0]
                data_dict[a[1][j]]["PIN"] = "P" + a[0][-1] + pin_find(a[1][j], file_inc)

            data_dict[a[1][j]]["PINNAME"] = a[1][j]
            data_dict[a[1][j]]["IDKEY"] = hex(binascii.crc32(str.encode("STM32"+a[1][j])))
            data_dict[a[1][j]]["INITS"] = data_init[schet]["INITS"]
            data_list_dict.append(data_dict)

        schet += 1

    # file.close()

    return data_list_dict


def port_finder(name_port, file_name):
    """
    Функция для поиска правильного названия порта: GPIOx, where x - A, B or C
    :param name_port: str (if portname != GPIOx, where x - A, B or C)
    :param file_name: str (filename of main.h)
    :return: str (port: GPIOx, where x - A, B or C)
    """
    file = open(file_name)
    lines_list = []
    for line in file:
        if name_port in line:
            line = line[8:]
            lines_list = line.split()

    port = lines_list[1]
    return port


def pin_find(pin_name, file_name):
    """
    Парсинг номера пина, к кот. подключено устройство
    :param pin_name: str
    :param file: str (уже открытый файл)
    :return: str
    """
    # file = open("D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h", "r")
    # file = open("D:\python\my_pin\Core\Inc\main.h")
    file = open(file_name)
    gpio_pin = str()
    for line in file:
        if pin_name in line:
            simple_list = line.split()
            gpio_pin = simple_list[-1]
            simple_list = gpio_pin.split("_")
            gpio_pin = simple_list[-1]
            break
            
    file.close()        

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
    f = open("./stm_project/gpio_pins.h", "w")
    f.write("#include "'"IPin.h"')
    for i in range(len(data)):
        for key in data[i].keys():
            model = data[i][key]
        temp = template.render(model)
        f.writelines(temp)
        f.writelines("\n\n\n")
    f.close()

    return None


def maybe_main_gpiogen(main_work_file, hal_msp_work_file, incmain_file):
    """
    Основная функция
    :return: None
    """
    # main_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    # main_work_file = "D:\python\my_pin\Core\Src\main.c"
    # hal_msp_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    # hal_msp_work_file = "D:\python\my_pin\Core\Src\stm32f1xx_hal_msp.c"
    # template_gpiopin = "./templates/powbut_templ.h"

    protocols = protocol_checker(main_work_file)  # все имеющиеся протоколы
    print(protocols)

    num_hal_write, num_init = parser(main_work_file)  # номера строк HalWritePin и начало Init
    # print(num_hal_write, num_init)

    data_str_main = extract_string(main_work_file, num_hal_write)  # строки HalWritePin
    # print(data_str_main)
    data_init = extract_initstruct(main_work_file, num_init)  # строки Init
    # print(data_init)

    data_list_dict = work_with_nstr(data_str_main, data_init, incmain_file)  # соединение воедино всех данных
    print(data_list_dict)

    porotocols_names = quant_prot(protocols)
    if "I2C" in porotocols_names:
        i2c_list_dict = f_pow_gen_secondpart.device_main(hal_msp_work_file, "I2C")
        data_list_dict = data_list_dict + i2c_list_dict
        i2c_gen.maybe_i2c_uart(main_work_file, hal_msp_work_file, "I2C")

    if "UART" in porotocols_names:
        uart_list_dict = f_pow_gen_secondpart.device_main(hal_msp_work_file, "UART")
        data_list_dict = data_list_dict + uart_list_dict
        i2c_gen.maybe_i2c_uart(main_work_file, hal_msp_work_file, "UART")

    if "SPI" in porotocols_names:
        spi_list_dict = f_pow_gen_secondpart.device_main(hal_msp_work_file, "SPI")
        data_list_dict = data_list_dict + spi_list_dict
        spi_dev_gen.maybe_main_func(main_work_file, hal_msp_work_file)

    print(data_list_dict)
    generation_powerbut_pins(data_list_dict)  # генерирование по шаблону gpio_pin
    return None


if __name__ == "__main__":
    main_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    hal_msp_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    file_inc = "D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h"
    maybe_main_gpiogen(main_work_file, hal_msp_work_file, file_inc)
