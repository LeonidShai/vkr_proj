# генерирование PeriherialId.h

import jinja2
import clang.cindex
import os, shutil


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
                            protocol_check_list.append(k.spelling[3:-5])

    return protocol_check_list
    
    
def parser_main(filename):
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
    
    
def parser_hal_msp(filename, param): # доработать

    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []

    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "HAL_"+param+"_MspDeInit":
                for i in c.get_children():
                    for k in i.get_tokens():
                        if k.spelling == "HAL_GPIO_DeInit":
                            num_str.append(k.location.line)

    return num_str


def extract_string(num_str, filename):

    data_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for i in num_str:
        if lines[i - 1][-1] != ";":
            data_str.append(lines[i - 1] + lines[i].lstrip())
        else:
            data_str.append(lines[i - 1])
    file.close()

    return data_str


def generation_data_dict(protocols):
    data_dict = {"PERIPS": dict()}
    for elem in protocols:
        if elem == "GPIO":
            data_dict["PERIPS"]["PIN"] = []
        elif "UART" in elem:
            key = "UART"+elem[5]
            data_dict["PERIPS"][key] = []
        else:
            data_dict["PERIPS"][elem] = []

    return data_dict


def defenition_presence(protocols):
    i2c_check = False
    uart_check = False
    i2c_prot = []
    uart_prot = []

    for elem in protocols:
        if "I2C" in elem:
            i2c_prot.append(elem)
            i2c_check = True
        elif "UART" in elem:
            uart_prot.append(elem[7:]+elem[5])
            uart_check = True

    return i2c_prot, uart_prot, i2c_check, uart_check


def works_with_main_str(mains_str, dop=None):
    # {"PERIPS": {"PIN": [pb1, pb2, pb3], "SPI": [ble, mem, miso, mosi, scl], "I2C": [sda, scl]}}
    data_dict = dict()
    count = 0
    for stroka in mains_str:
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

        for pin_name in a[1]:
            if "SPI" in pin_name:
                key = "SPI" + pin_name[3]
                if not key in data_dict:
                    data_dict[key] = [key+"_SCK", key+"_MISO", key+"_MOSI"]
                data_dict[key].append(pin_name)
            elif "I2C" in pin_name:
                key = dop[count]
                if not key in data_dict:
                    data_dict[key] = []
                data_dict[key].append(pin_name)
            elif "UART" in pin_name:
                key = dop[count]
                if not key in data_dict:
                    data_dict[key] = []
                data_dict[key].append(pin_name)
            else:
                if not "PIN" in data_dict:
                    data_dict["PIN"] = []
                data_dict["PIN"].append(pin_name)
        count += 1

    return data_dict


def create_skeleton(protocol_check_list):
    """
    Копирование нужных файлов из ./templates
    :param protocol_check_list: list
    :return: None
    """
    if not os.path.isdir("stm32_project"):
        os.mkdir("stm32_project")
        shutil.copyfile("./templates/periherial_templ.h", "./stm32_project/periherial.h")

    for name in protocol_check_list:
        if name == "GPIO":
            shutil.copyfile("./templates/ipin_templ.h", "./stm32_project/i_pin.h")

        elif "I2C" in name:
            shutil.copyfile("./templates/i_i2c_templ.h", "./stm32_project/i_i2c.h")

        elif "SPI" in name:
            shutil.copyfile("./templates/ispi_templ.h", "./stm32_project/i_spi.h")

        elif "USART" in name:
            shutil.copyfile("./templates/i_uart_templ.h", "./stm32_project/i_uart.h")

        else:
            ...  # это просто окончание

    return None


def generate_periherial_factory(protocol_list):
    """
    генерирование periherial_factory.h
    :param text_template: str
    :param protocol_list: list
    :return: None
    """
    main_protocol_list = []
    for i in protocol_list:
        if "I2C" in i and not "I2C" in main_protocol_list:
            main_protocol_list.append("I2C")
        elif "UART" in i and not "UART" in main_protocol_list:
            main_protocol_list.append("UART")
        elif "SPI" in i and not "SPI" in main_protocol_list:
            main_protocol_list.append("SPI")
        elif "GPIO" in i and not "GPIO" in main_protocol_list:
            main_protocol_list.append("PIN")

    text_template = "./templates/periherial_factory.h"
    text = open(text_template).read()
    template = jinja2.Template(text)
    model = {"PERIPS": main_protocol_list}
    temp = template.render(model)

    f = open("./stm32_project/periherial_factory.h", "w")
    f.writelines(temp)
    f.close()

    return None


def generation_myfactory_periph(model):
    text_template = "./templates/myfactory_peripherals.h"
    text = open(text_template).read()
    template = jinja2.Template(text)
    temp = template.render(model)

    f = open("./stm32_project/my_factory_peripherals.h", "w")
    f.writelines(temp)
    f.close()

    return None


def maybe_main_myfactory():
    """
    Как бы основная функция
    :return: None
    """
    main_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    halmsp_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"

    protocols = protocol_checker(main_work_file)  # какие протоколы использованы
    print(protocols)
    create_skeleton(protocols)  # создание основного скелета
    generate_periherial_factory(protocols)  # генерирование periherial_factory

    num_str_from_main = parser_main(main_work_file)  # парсим main.с на предмет строк
    list_str_main = extract_string(num_str_from_main, main_work_file)
    # получаем строки с HAL_GPIO_WritePin из main.c
    print(list_str_main)
    data_dict = generation_data_dict(protocols)
    main_data_dict = works_with_main_str(list_str_main)
    print(main_data_dict)
    all_data_dict = {"PERIPS": main_data_dict}

    i2c_prot, uart_prot, i2c_check, uart_check = defenition_presence(protocols)
    if i2c_check:
        num_str_i2c = parser_hal_msp(halmsp_work_file, "I2C")
        list_str_i2c = extract_string(num_str_i2c, halmsp_work_file)
        print(list_str_i2c)

        data_dict_i2c = works_with_main_str(list_str_i2c, i2c_prot)
        print(data_dict_i2c)

        for key in data_dict_i2c:
            all_data_dict["PERIPS"][key] = data_dict_i2c[key]

    if uart_check:
        num_str_uart = parser_hal_msp(halmsp_work_file, "UART")
        list_str_uart = extract_string(num_str_uart, halmsp_work_file)
        print(list_str_uart)

        data_dict_uart = works_with_main_str(list_str_uart, uart_prot)
        print(data_dict_uart)

        for key in data_dict_uart:
            all_data_dict["PERIPS"][key] = data_dict_uart[key]

    generation_myfactory_periph(all_data_dict)

    return None


if __name__ == "__main__":

    maybe_main_myfactory()
