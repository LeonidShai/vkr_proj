import clang.cindex
import binascii
import jinja2


def parser_main(filename):
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
            # print(c.spelling, c.location.line)  # for test
            if c.spelling == "MX_I2C1_Init":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling)  # for test
                        if k.spelling == "Instance":
                            num_str.append(k.location.line)
                        if k.spelling == "NoStretchMode":
                            num_str.append(k.location.line)

    return num_str


def parser_hal_msp(filename):
    """
    Парсит номерa строк начало и конец необходимого фрагмента
    :param node: str (filename)
    :return: list (string's numbers)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []  # список для номеров строк HAL_I2C_MspDeInit

    for c in node.get_children():
        if c.location.file.name == filename:
            # print(c.spelling, c.location.line)  # for test
            if c.spelling == "HAL_I2C_MspDeInit":
                for i in c.get_children():
                    for k in i.get_tokens():
                        # print("//", k.spelling, k.location.line)  # for test
                        if "Configuration" in k.spelling:
                            num_str.append(k.location.line)
                        if k.spelling == "HAL_GPIO_DeInit":
                            num_str.append(k.location.line)

    return num_str


def extract_main_string(filename, num_str):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    i = num_str[0]
    while i < num_str[1]:
        data_str.append(lines[i-1].lstrip())
        i += 1
    file.close()

    return data_str


def extract_halmsp_string(filename, num_str):
    """
    Извлекает строку/строки из файла
    :param filename: str (filename)
    :param num_str: list (string's numbers)
    :return: list (necessary strings)
    """
    data_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for i in range(len(num_str)):
        if i == 0:
            data_str.append(lines[num_str[i]].lstrip())
            data_str.append(lines[num_str[i]+1].lstrip())
        else:
            data_str.append(lines[num_str[i]-1].lstrip())

    file.close()

    return data_str


def work_halmsp_data(halmsp_data):
    halmsp_dict = {"PIN1": None, "PIN2": None, "PINNAMES": None, "NAME": None, "CRCID": None}
    halmsp_dict["PIN1"] = halmsp_data[0][:3]
    halmsp_dict["PIN2"] = halmsp_data[1][:3]

    s = int()
    e = int()
    for i in range(len(halmsp_data[2])):
        if halmsp_data[2][i] == "(":
            s = i+1
        elif halmsp_data[2][i] == ")":
            e = i

    # разделение полученной подстроки на параметры
    data = halmsp_data[2][s:e].split(", ")  # list of strings, with splitting
    data[1] = data[1].split("|")

    halmsp_dict["PINNAMES"] = data[1]
    halmsp_dict["NAME"] = data[1][0][:-4]
    halmsp_dict["CRCID"] = hex(binascii.crc32(str.encode("STM32"+data[1][0][:-4])))

    return halmsp_dict


def unification_data(halmsp_dict, data_main):
    halmsp_dict["I2CNUM"] = 'hi2c' + data_main[0][-2]
    halmsp_dict["INITS"] = data_main
    return halmsp_dict


def generation_i2c_dev(data):
    """
    Генерирует по шаблону powerbut_pins
    :param l_d: list (list of dicts with necessary data from strings)
    :return: None
    """
    text_template = "./templates/i2c_fan_templ.h"  # шаблон для автогенерации
    text = open(text_template).read()
    template = jinja2.Template(text)

    # генерация файла с классами для всех powerbuttons_pins
    f = open("./stm32_project/i2c_devs.h", "w")
    model = data
    temp = template.render(model)
    f.writelines(temp)
    f.close()

    return None


if __name__ == "__main__":
    first_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\main.c"
    second_work_file = "D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c"

    num_str = parser_main(first_work_file)
    # print(num_str)

    data_main = extract_main_string(first_work_file, num_str)
    #print(data_main)

    num_str = parser_hal_msp(second_work_file)
    #print(num_str)

    data_hal_msp = extract_halmsp_string(second_work_file, num_str)
    #print(data_hal_msp)

    hal_msp_dict = work_halmsp_data(data_hal_msp)
    #print(hal_msp_dict)

    data = unification_data(hal_msp_dict, data_main)
    print(data)

    generation_i2c_dev(data)
