# работает для I2C и UART
import clang.cindex
import binascii


def parser_deinit(filename):
    """
    парсим номера строк HAL_GPIO_DeInit
    :param filename:
    :return: list (с номерами строк)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    num_str = []

    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "HAL_SPI_MspDeInit":  # I2C, UART
                for i in c.get_children():
                    for k in i.get_tokens():
                        if k.spelling == "HAL_GPIO_DeInit":
                            num_str.append(k.location.line)

    return num_str


def parser_init(filename):
    """
    Парсер номеров строк для INIT и для PIN (PB6, PB7 ..)
    :param filename:
    :return: list, list (два списка с номерами строк)
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    node = tu.cursor

    numstr_pins = []  # номера строк для pin
    numstr_init = []  # номера строк для init (список списков)

    for c in node.get_children():
        if c.location.file.name == filename:
            if c.spelling == "HAL_SPI_MspInit":  # I2C, UART
                for i in c.get_children():
                    for k in i.get_tokens():
                        if "Configuration" in k.spelling:
                            numstr_pins.append(k.location.line+1)
                        elif k.spelling == "Pin":
                            start_end = [k.location.line+1]
                        elif k.spelling == "HAL_GPIO_Init":
                            start_end.append(k.location.line-1)
                            numstr_init.append(start_end)

    return numstr_pins, numstr_init


def extract_str(filename, numstr):
    """
    Извлечение по номерам строк самих строк из файлов
    :param filename: str
    :param numstr: list список номеров строк
    :return: list список строк
    """
    deinit_str = []  # список требуемых строк
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for i in numstr:
        if lines[i - 1][-1] != ";":
            deinit_str.append(lines[i - 1].lstrip() + lines[i].lstrip())
        else:
            deinit_str.append(lines[i - 1].lstrip())
    file.close()

    return deinit_str


def special_extract(filename, numstrs, sticks):
    """
    С использованием extract_str() и образованием нужного количества списков строк
    :param filename: str
    :param numstrs: list of lists (с номерами строк)
    :param sticks: list (параметр, на который нужно увелчить количество списков строк) число повторений
    :return: list (список списков строк)
    """
    inits = []
    for i in range(len(numstrs)):
        init_str = extract_str(filename, numstrs[i])
        j = 1
        while j <= sticks[i]:
            inits.append(init_str)
            j += 1
    return inits


def work_with_deinit_str(deinit_str):
    """
    Образование списка словарей со словарями
    :param deinit_str: list список строк для парсинга
    :return: list
    """
    data_deinit = []
    for stroka in deinit_str:
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

        for j in range(len(a[1])):
            data_dict = {a[1][j][:-4]: {"PORTNAME": None, "PINNAME": None, "IDKEY": None,
                                        "PIN": None, "INITS": None}}
            data_dict[a[1][j][:-4]]["PORTNAME"] = a[0]
            data_dict[a[1][j][:-4]]["PINNAME"] = a[1][j][:-4]
            data_dict[a[1][j][:-4]]["IDKEY"] = hex(binascii.crc32(str.encode("STM32"+a[1][j][:-4])))
            data_deinit.append(data_dict)

    return data_deinit


def work_with_pins_str(pins_str):
    """
    Извлечение пинов PB6, PB7 ...
    :param pins_str: list список со строками
    :return: list список пинов
    """
    pins_list = []
    for i in pins_str:
        i = i.split("TX")  # SCL для I2C, TX для UART
        pins_list.append(i[0][:4].rstrip())
        pins_list.append(i[1][:4].rstrip())

    return pins_list


def unification(data, pins, inits):
    """
    Добавление к существующему словарю INIT и PIN
    :param data: list список словарей со словарями
    :param pins: list список пинов
    :param inits: list список списков строк для INIT
    :return: list обновлённый список словарей со словарями
    """
    count = 0
    for d in data:
        for key in d.keys():
            d[key]["PIN"] = pins[count]
            d[key]["INITS"] = inits[count]
        count += 1
    return data


def quant_test(filename, numstrs):
    """
    Количество пинов в строке, через подсчёт "|"
    :param filename: str
    :param numstrs: list список списков
    :return: list количество переменных (число повторений)
    """
    quant_sticks = []
    file = open(filename, 'r')
    lines = file.read().splitlines()
    for elem in numstrs:
        sch = lines[elem[0]-2].count("|")
        quant_sticks.append(sch+1)
    return quant_sticks


def i2c_main(hal_msp_work_file):
    """
    Как бы основная функция
    :param hal_msp_work_file: str (fiename)
    :return: list список словарей с основными параметрами для каждого пина
    """
    numstr_deinit = parser_deinit(hal_msp_work_file)  # парсим номера строк HAL_GPIO_DeInit
    # print(numstr_deinit)
    deinit_str = extract_str(hal_msp_work_file, numstr_deinit)  # вытаскиваем строки HAL_GPIO_DeInit
    print(deinit_str)
    data_deinit = work_with_deinit_str(deinit_str)  # собираем из HAL_GPIO_DeInit нужные параметры
    print(data_deinit)

    numstr_pins, numstr_init = parser_init(hal_msp_work_file)  # парсим номера строк Init
    print(numstr_pins, numstr_init)

    pins_str = extract_str(hal_msp_work_file, numstr_pins)  # извлечение строк с номерами пинов
    print(pins_str)
    pins_list = work_with_pins_str(pins_str)  # получение списка пинов
    print(pins_list)

    sticks = quant_test(hal_msp_work_file, numstr_init)  # количество разделителей для числа повторений
    # print(sticks)
    init_strs = special_extract(hal_msp_work_file, numstr_init, sticks)  # извлечение строк с INIT
    print(init_strs)

    data_all = unification(data_deinit, pins_list, init_strs)  # все данные в однин список словарей
    print(data_all)

    return data_all


if __name__ == "__main__":
    i2c_main("D:\python\cubemx\pbpin_spi_i2c\Core\Src\stm32f1xx_hal_msp.c")
