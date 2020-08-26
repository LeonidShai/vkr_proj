# генерирование PeriherialId.h

import jinja2
import clang.cindex
import os, shutil


def clang_starter(filename):
    """
    Запуск clang
    :param filename: str
    :return: clang.cindex.node
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    return node


def protocol_checker(node, filename):
    """
    Проверка наличия протоколов
    :param node: clang.cindex.node
    :param filename: str
    :return: list
    """
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


if __name__ == "__main__":
    # print("hey")

    first_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"

    usel = clang_starter(first_work_file)
    prot_ch_lst = protocol_checker(usel, first_work_file)
    create_skeleton(prot_ch_lst)
