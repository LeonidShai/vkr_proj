import clang.cindex
import binascii
import jinja2


def quant_prot(protocols, who):
    """
    Разделение на отдельные списки протоколов
    :param protocols: list
    :return: list (names protocols)
    """
    quant_prot = []

    for elem in protocols:
        if who in elem:
            quant_prot.append(elem)

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


def work_with_nstr(data_str, data_init):
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
            data_dict = {a[1][j][:-4]: {"PORTNAME": None, "PINNAME": None, "FUNCNAME": None,
                                        "IDKEY": None, "PIN": None, "INITS": None}}
            data_dict[a[1][j][:-4]]["PORTNAME"] = a[0]
            data_dict[a[1][j][:-4]]["PINNAME"] = a[1][j][:-4]
            data_dict[a[1][j][:-4]]["FUNCNAME"] = a[2]
            data_dict[a[1][j][:-4]]["IDKEY"] = hex(binascii.crc32(str.encode("STM32"+a[1][j])))
            data_dict[a[1][j][:-4]]["PIN"] = "P" + a[0][-1::] + pin_find(a[1][j])
            data_dict[a[1][j][:-4]]["INITS"] = data_init[schet]["INITS"]
            data_list_dict.append(data_dict)

        schet += 1

    # file.close()

    return data_list_dict


def pin_find(pin_name):
    """
    Парсинг номера пина, к кот. подключено устройство
    :param pin_name: str
    :param file: str (уже открытый файл)
    :return: str
    """
    file = open("D:\python\cubemx\pbpin_spi_i2c\Core\Inc\main.h", "r")
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
    f = open("./stm32_project/gpio_pins.h", "w")
    for i in range(len(data)):
        model = data[i]
        temp = template.render(model)
        f.writelines(temp)
        f.writelines("\n\n\n")
    f.close()

    return None


def maybe_main_gpiogen():
    """
    Основная функция
    :return: None
    """
    main_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    hal_msp_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    template_gpiopin = "./templates/powbut_templ.h"

    protocols = protocol_checker(main_work_file)  # все имеющиеся протоколы
    print(protocols)

    num_hal_write, num_init = parser(main_work_file)  # номера строк HalWritePin и начало Init
    print(num_hal_write, num_init)

    data_str_main = extract_string(main_work_file, num_hal_write)  # строки HalWritePin
    print(data_str_main)
    data_init = extract_initstruct(main_work_file, num_init)  # строки Init
    print(data_init)

    if "I2C" in protocols:
        i2c_protocols = quant_prot(protocols, "I2C")
        i2c_list_dict = i2c_main(i2c_protocols, hal_msp_work_file)

    if "UART" in protocols:
        uart_protocols = quant_prot(protocols, "UART")
        uart_list_dict = uart_main(uart_protocols, hal_msp_work_file)

    if "SPI" in protocols:
        spi_protocols = quant_prot(protocols, "SPI")
        spi_list_dict = spi_main(spi_protocols, hal_msp_work_file)

    data_list_dict = work_with_nstr(data_str_main, data_init)  # соединение воедино всех данных
    print(data_list_dict)

    generation_powerbut_pins(data_list_dict)  # генерирование по шаблону gpio_pin
    return None


if __name__ == "__main__":
    maybe_main_gpiogen()
