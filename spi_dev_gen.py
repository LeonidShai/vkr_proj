# для генерации SPI_devices

import clang.cindex
import jinja2
import binascii


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


def spi_kind(protocols):
    """
    собирает названия всех SPI в один список (SPI1, SPI2..)
    :param protocols: list (with all protocols in program)
    :return: list (with SPI)
    """
    spis_list = []
    for elem in protocols:
        if "SPI" in elem:
            spis_list.append(elem)
    return spis_list


def parser_main(filename, spi_list):
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []  # список для номеров строк

    for c in node.get_children():
        if c.location.file.name == filename:
            for spi in spi_list:
                numstr_dict = {spi: []}
                if c.spelling == spi:
                    for i in c.get_children():
                        for k in i.get_tokens():
                            if k.spelling == "Instance":
                                numstr_dict[spi].append(k.location.line)
                            if k.spelling == "if":
                                numstr_dict[spi].append(k.location.line)
                                num_str.append(numstr_dict)

    return num_str


def parser_main_spidev(filename):
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    numstr_gpio = []

    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "MX_GPIO_Init":
                for i in c.get_children():
                    for k in i.get_tokens():
                        if k.spelling == "HAL_GPIO_WritePin":
                            numstr_gpio.append(k.location.line)

    return numstr_gpio


def parser_hal_msp(filename, spi_list):
    """
    Парсит номерa строк начало и конец необходимого фрагмента
    :param node: str (filename)
    :return: list (string's numbers)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str_list = []  # список для номеров строк HAL_I2C_MspDeInit
    sch = 0

    for c in node.get_children():
        if c.location.file.name == filename:
            # print(c.spelling, c.location.line)  # for test
            if c.spelling == "HAL_SPI_MspDeInit":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling, k.location.line)  # for test
                        if "Configuration" in k.spelling:
                            num_str = []
                            num_str.append(k.location.line)
                        elif k.spelling == "HAL_GPIO_DeInit":
                            num_str.append(k.location.line-2)
                            numstr_dict = {spi_list[sch]: num_str}
                            num_str_list.append(numstr_dict)
                            sch += 1

    return num_str_list


def extract_main_string(filename, num_str, spi_list):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str_list = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for e in range(len(spi_list)):
        data_str_dict = {spi_list[e]: []}
        i = num_str[e][spi_list[e]][0]
        while i < num_str[e][spi_list[e]][1]:
            data_str_dict[spi_list[e]].append(lines[i - 1].lstrip())
            i += 1
        data_str_list.append(data_str_dict)

    file.close()

    return data_str_list


def extract_spidevs(filename, numstr_gpio):
    spidev_list_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()

    for i in numstr_gpio:
        if lines[i - 1][-1] != ";":
            prom_str = lines[i - 1].rstrip() + lines[i].lstrip()
        else:
            prom_str = lines[i - 1].rstrip()

        spidev_list_str.append(prom_str)
    return spidev_list_str


def extract_halmsp_string(filename, num_str, spi_list):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str_list = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()

    for e in range(len(spi_list)):
        data_str_dict = {spi_list[e]: []}
        for i in range(len(num_str[e][spi_list[e]])):
            if i == 0:
                data_str_dict[spi_list[e]].append(lines[num_str[e][spi_list[e]][i]].lstrip()[:4].rstrip())
                data_str_dict[spi_list[e]].append(lines[num_str[e][spi_list[e]][i] + 1].lstrip()[:4].rstrip())
            else:
                data_str_dict[spi_list[e]].append(lines[num_str[e][spi_list[e]][i] - 1].lstrip()[:4].rstrip())
        data_str_list.append(data_str_dict)

    file.close()

    return data_str_list


def work_with_spidevs(spidev_list_str, spi_list):
    spidev_list = []
    for spi in spi_list:
        data_spidevs = {spi: []}
        for stroka in spidev_list_str:
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
                if spi[3:-5] in pin_name:
                    data_spidevs[spi].append(pin_name[:-4])
        spidev_list.append(data_spidevs)

    return spidev_list


def unification_data(inits, spi_devs, pins, spis_list):
    all_data = []

    count = 0
    for elem in spis_list:
        data_elem_dict = {"SPINAME": None, "SPINUM": None, "CRCID": None,
                          "PINNAMES": None, "SPIDEVS": None, "CH": None, "INITS": None,
                          "PIN1": None, "PIN2": None, "PIN3": None,}
        data_elem_dict["SPINAME"] = elem[3:-5]
        data_elem_dict["SPINUM"] = "h" + elem[3:-5].lower()
        data_elem_dict["CRCID"] = hex(binascii.crc32(str.encode("STM32"+elem[3:-5])))

        pinnames_list = [elem[3:-5]+"_SCK", elem[3:-5]+"_MISO", elem[3:-5]+"_MOSI"]
        pinnames_list = pinnames_list + spi_devs[count][elem]
        data_elem_dict["PINNAMES"] = pinnames_list

        data_elem_dict["SPIDEVS"] = spi_devs[count][elem]
        data_elem_dict["CH"] = len(spi_devs[count][elem])

        data_elem_dict["INITS"] = inits[count][elem]

        data_elem_dict["PIN1"] = pins[count][elem][0]
        data_elem_dict["PIN2"] = pins[count][elem][1]
        data_elem_dict["PIN3"] = pins[count][elem][2]

        all_data.append(data_elem_dict)
        count += 1

    return all_data


def gen_spidevs(filename, all_data):
    text_template = filename
    text = open(text_template).read()
    template = jinja2.Template(text)

    f = open("./stm_project/spi_devs.h", "w")
    for i in all_data:
        model = i
        temp = template.render(model)
        f.writelines(temp)
    f.close()

    return None


def maybe_main_func(first_work_file, second_work_file):
    template_spidev = "./templates/spi_ble_templ.h"

    protocols = protocol_checker(first_work_file)
    spis_list = spi_kind(protocols)  # получаем только SPI
    print(spis_list)
    numstr_main_init = parser_main(first_work_file, spis_list)  # номера строк с init
    print(numstr_main_init)
    data_list_init = extract_main_string(first_work_file, numstr_main_init, spis_list)  # init

    numstr_gpio = parser_main_spidev(first_work_file)  # номера строк для устройств
    spidev_list_str = extract_spidevs(first_work_file, numstr_gpio) # строки с устройствами все HalWritePin
    print(spidev_list_str)
    spidev_list = work_with_spidevs(spidev_list_str, spis_list)  # устройтсва spi
    print(spidev_list)

    numstr_pins = parser_hal_msp(second_work_file, spis_list)  # строки из hal_msp
    print(numstr_pins)
    pins_str = extract_halmsp_string(second_work_file, numstr_pins, spis_list)  # пины для scl, miso, mosi
    print(pins_str)

    all_data = unification_data(data_list_init, spidev_list, pins_str, spis_list)
    print(all_data)

    gen_spidevs(template_spidev, all_data)

    return None


if __name__ == "__main__":
    first_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    second_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    maybe_main_func(first_work_file, second_work_file)

