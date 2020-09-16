# генерирование PeriherialId.h и основного скелета программы

import jinja2
import clang.cindex
import os, shutil


def protocol_checker(filename):
    """
    Получение протоколов GPIO, I2C, SPI, UART
    :param filename: str (имя файла)
    :return: list (список протоколов)
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


def create_skeleton(protocol_check_list):
    """
    Копирование нужных файлов из ./templates, создание основного скелета
    :param protocol_check_list: list (список протоколов)
    :return: None
    """
    if not os.path.isdir("stm_project"):
        os.mkdir("stm_project")
        shutil.copyfile("./templates/periherial_templ.h", "./stm_project/periherial.h")

    for name in protocol_check_list:
        if name == "GPIO":
            shutil.copyfile("./templates/ipin_templ.h", "./stm_project/i_pin.h")

        elif "I2C" in name:
            shutil.copyfile("./templates/i_i2c_templ.h", "./stm_project/i_i2c.h")

        elif "SPI" in name:
            shutil.copyfile("./templates/ispi_templ.h", "./stm_project/i_spi.h")

        elif "USART" in name:
            shutil.copyfile("./templates/i_uart_templ.h", "./stm_project/i_uart.h")

        else:
            ...  # это просто окончание

    return None


def generate_periherial_factory(protocol_list):
    """
    генерирование periherial_factory.h
    :param text_template: str (имя шаблона)
    :param protocol_list: list (список протоколов)
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
            main_protocol_list.append("Pin")

    text_template = "./templates/periherial_factory.h"
    text = open(text_template).read()
    template = jinja2.Template(text)
    model = {"PERIPS": main_protocol_list}
    temp = template.render(model)

    # f = open("./stm32_project/periherial_factory.h", "w")
    f = open("./stm_project/periherial_factory.h", "w")
    f.writelines(temp)
    f.close()

    return None


def maybe_main_myfactory(main_work_file):
    """
    Основная функция, генерирование основного скелета программы
    :return: None
    """

    protocols = protocol_checker(main_work_file)  # какие протоколы использованы
    # print(protocols)
    create_skeleton(protocols)  # создание основного скелета: i_i2c.h, i_pin.h, i_spi.h, i_uart.h
    generate_periherial_factory(protocols)  # генерирование periherial_factory

    return None


if __name__ == "__main__":

    main_work_file = "D:\python\my_pin\Core\Src\main.c"
    halmsp_work_file = "D:\python\my_pin\Core\Src\stm32f1xx_hal_msp.c"
    # our_path = "D:\python\my_pin"
    maybe_main_myfactory(main_work_file)
