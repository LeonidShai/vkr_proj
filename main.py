import os

import periherialid_gen  # для генерации скелета
import copiesss  # для генерации id_periherial, my_factory, spi_chipselect
import for_powerbut_gen  # для генерации powerbutton's


def finder_work_files():
    """
    Осуществляет поиск рабочих файлов в сгенерированном проекте CubeMX
    :return:
    """
    our_path = os.getcwd()
    src_path = our_path + "/Core/Src"
    inc_path = our_path + "/Core/Inc"
    if os.path.exists(src_path):
        for file in os.listdir(src_path):
            if "main" in file:
                src_main_work_file = src_path + "/" + file
            elif "hal_msp" in file:
                hal_msp_work_file = src_path + "/" + file

        for file in os.listdir(inc_path):
            if "main" in file:
                inc_main_work_file = inc_path + "/" + file

        return src_main_work_file, hal_msp_work_file, inc_main_work_file

    else:
        return None


if __name__ == "__main__":
    if not finder_work_files():
        print("Не существует файлов: main.c, main.h, hal_msp.c!")
    else:
        srcmain_work_file, halmsp_work_file, incmain_work_file = finder_work_files()
        print(srcmain_work_file, "\n", halmsp_work_file, "\n", incmain_work_file)

        periherialid_gen.maybe_main_myfactory(srcmain_work_file)  # основные файлы генерирует, skeleton

        copiesss.maybe_main(srcmain_work_file, incmain_work_file)  # для генерации id_periherial, my_factory, spi_chipselect

        for_powerbut_gen.maybe_main_gpiogen(srcmain_work_file, halmsp_work_file, incmain_work_file)  # для генерации powerbutton's
