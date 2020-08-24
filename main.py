import os
import periherialid_gen


def main():
    # os.mkdir("stm32_project")
    abc = "IPin"
    ch = str()
    for i in abc:
        ch += str(ord(i))
    ch = ch[::-1]
    print(hex(int(ch)))


if __name__ == "__main__":
    main()
