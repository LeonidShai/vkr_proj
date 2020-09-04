import clang.cindex
import binascii
import jinja2


def parser_quant_i2c(filename, who):
    """
    Парсит количество i2c
    :param node: str (filename)
    :return: list (names I2C)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor
    
    quant_i2c = []
    
    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "main":
                for i in c.get_children():
                    for k in i.get_children():
                        if who in k.spelling:
                            quant_i2c.append(k.spelling)
    
    return quant_i2c


def parser_main(filename, quant_i2c):
    """
    Парсит номерa строк начало и конец необходимого фрагмента
    :param node: str (filename)
    :return: list (string's numbers)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []  # список для номеров строк MX_I2C1_Init

    for c in node.get_children():
        if c.location.file.name == filename:
            for i2c in quant_i2c:
                numstr_dict = {i2c: []}
                if c.spelling == i2c:
                    for i in c.get_children():
                        for k in i.get_tokens():
                            if k.spelling == "Instance":
                                numstr_dict[i2c].append(k.location.line)
                            if k.spelling == "if":
                                numstr_dict[i2c].append(k.location.line)
                                num_str.append(numstr_dict)

    return num_str


def parser_hal_msp(filename, quant_i2c, who):
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
            if c.spelling == "HAL_"+who+"_MspDeInit":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling, k.location.line)  # for test
                        if "Configuration" in k.spelling:
                            num_str = []
                            num_str.append(k.location.line)
                        elif k.spelling == "HAL_GPIO_DeInit":
                            num_str.append(k.location.line)
                            numstr_dict = {quant_i2c[sch]: num_str}
                            num_str_list.append(numstr_dict)
                            sch += 1 

    return num_str_list


def extract_main_string(filename, num_str, quant_i2c):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str_list = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for e in range(len(quant_i2c)):
        data_str_dict = {quant_i2c[e]: []}
        i = num_str[e][quant_i2c[e]][0]
        while i < num_str[e][quant_i2c[e]][1]:
            data_str_dict[quant_i2c[e]].append(lines[i-1].lstrip())
            i += 1
        data_str_list.append(data_str_dict)
    
    file.close()

    return data_str_list


def extract_halmsp_string(filename, num_str, quant_i2c):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str_list = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    
    for e in range(len(quant_i2c)):
        data_str_dict = {quant_i2c[e]: []}
        for i in range(len(num_str[e][quant_i2c[e]])):
            if i == 0:
                data_str_dict[quant_i2c[e]].append(lines[num_str[e][quant_i2c[e]][i]].lstrip())
                data_str_dict[quant_i2c[e]].append(lines[num_str[e][quant_i2c[e]][i]+1].lstrip())
            else:
                data_str_dict[quant_i2c[e]].append(lines[num_str[e][quant_i2c[e]][i]-1].lstrip())
        data_str_list.append(data_str_dict)

    file.close()

    return data_str_list


def work_halmsp_data(halmsp_data, quant_i2c, who):
    halmsp_list = []
    for e in range(len(quant_i2c)):
        halmsp_dict = {quant_i2c[e]: {"PIN1": None, "PIN2": None, "PINNAMES": None, "NAME": None, "CRCID": None}}
        halmsp_dict[quant_i2c[e]]["PIN1"] = halmsp_data[e][quant_i2c[e]][0][:5].rstrip()
        halmsp_dict[quant_i2c[e]]["PIN2"] = halmsp_data[e][quant_i2c[e]][1][:5].rstrip()

        s = int()
        k = int()
        for i in range(len(halmsp_data[e][quant_i2c[e]][2])):
            if halmsp_data[e][quant_i2c[e]][2][i] == "(":
                s = i+1
            elif halmsp_data[e][quant_i2c[e]][2][i] == ")":
                k = i

    # разделение полученной подстроки на параметры
        data = halmsp_data[e][quant_i2c[e]][2][s:k].split(", ")  # list of strings, with splitting
        data[1] = data[1].split("|")

        halmsp_dict[quant_i2c[e]]["PINNAMES"] = data[1]
        halmsp_dict[quant_i2c[e]]["NAME"] = who + str(e+1)  #data[1][0][:-4]
        halmsp_dict[quant_i2c[e]]["CRCID"] = hex(binascii.crc32(str.encode("STM32"+data[1][0][:-4])))
        halmsp_list.append(halmsp_dict)

    return halmsp_list


def unification_data(halmsp_list, data_main, quant_i2c, who):
    for e in range(len(quant_i2c)):
        halmsp_list[e][quant_i2c[e]]["I2CNUM"] = 'h' + who.lower() + data_main[e][quant_i2c[e]][0][-2]
        halmsp_list[e][quant_i2c[e]]["INITS"] = data_main[e][quant_i2c[e]]
    return halmsp_list


def generation_i2c_dev(data, quant_i2c, who):
    """
    Генерирует по шаблону powerbut_pins
    :param l_d: list (list of dicts with necessary data from strings)
    :return: None
    """
    if who == "I2C":
        text_template = "./templates/i2c_fan_templ.h"  # шаблон для автогенерации
    elif who == "UART":
        text_template = "./templates/uart_device_templ.h"
    text = open(text_template).read()
    template = jinja2.Template(text)

    # генерация файла с классами для всех powerbuttons_pins
    f = open("./stm32_project/"+who+"_devs.h", "w")
    for e in range(len(quant_i2c)):
        model = data[e][quant_i2c[e]]
        temp = template.render(model)
        f.writelines(temp)
    f.close()

    return None


if __name__ == "__main__":
    first_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    second_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"
    who = "I2C"

    quant_i2c = parser_quant_i2c(first_work_file, who)
    print(quant_i2c)
    print()
    
    num_str = parser_main(first_work_file, quant_i2c)
    print(num_str)
    print()

    data_main = extract_main_string(first_work_file, num_str, quant_i2c)
    print(data_main)
    print()

    num_str = parser_hal_msp(second_work_file, quant_i2c, who)
    print(num_str)
    print()

    data_hal_msp = extract_halmsp_string(second_work_file, num_str, quant_i2c)
    print(data_hal_msp)
    print()

    hal_msp_list = work_halmsp_data(data_hal_msp, quant_i2c, who)
    print(hal_msp_list)
    print()

    data = unification_data(hal_msp_list, data_main, quant_i2c, who)
    print(data)

    generation_i2c_dev(data, quant_i2c, who)