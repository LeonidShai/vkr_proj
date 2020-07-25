import clang.cindex
import os


def parser(filename):
    """
    Парсер для файла на языке Си. Парсит названия функций, типы функций, передаваемые параметры и их типы.
    :param filename: str
    :return: list
    """
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    our_functions = []

    for c in tu.cursor.get_children():
        if c.location.file.name == filename:
            d = {"name": None, "type_func": None, "argv": [], "begin": None, 'end': None}
            type_func = c.type.spelling.split()
            d["name"] = c.spelling
            d["type_func"] = type_func[0]
            d["begin"] = c.extent.start.line
            d["end"] = c.extent.end.line

            for arg in c.get_children():
                argv_dict = {"name": None, "argv_type": None}
                if arg.spelling != "":
                    argv_dict["name"] = arg.spelling
                    argv_dict["argv_type"] = arg.type.spelling
                    d["argv"].append(argv_dict)

            our_functions.append(d)

    return our_functions

def for_files(mypath):
    """
    Для прохода по всем файлам в папке.
    :param mypath: str
    :return: None
    """
    files_list = os.listdir(mypath)
    for i in range(len(files_list)):
        files_list[i] = os.path.join(mypath, files_list[i])

    for file_c in files_list:
        if os.path.isfile(file_c):
            print(file_c)
            for func_data in parser(file_c):
                print(func_data)

    return None


if __name__ == "__main__":
    print("hello clang! let's parse!")

    # mypath = 'D:\python\demo_stm32\Core\Src'
    mypath = 'D:\python\demo_stm32\Drivers\STM32F4xx_HAL_Driver\Src'
    for_files(mypath)

    # file_c = 'D:\cplusplus\probnii_c\probnii_c\main.c'
    # file_c = 'D:\python\demo_stm32\Core\Src\main.c'
    # file_c = 'D:\python\demo_stm32\Core\Src\stm32f4xx_hal_msp.c'
    # file_c = 'D:\python\demo_stm32\Drivers\STM32F4xx_HAL_Driver\Src\stm32f4xx_hal_gpio.c'
    # file_c = 'D:\python\demo_stm32\Drivers\STM32F4xx_HAL_Driver\Src\stm32f4xx_hal_pwr.c'
    # for i in parser(file_c):
    #     print(file_c)
    #     print(i)
