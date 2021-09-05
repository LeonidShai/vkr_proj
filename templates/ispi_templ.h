#ifndef ISPI_H
#define ISPI_H

#include "periherial.h"
#include "spi_chipselect.h"

class ISpi : public IPeripheral{
	
public:
    
    virtual std::tuple<Status, uint8_t*, size_t> read(SPIChipSelect chipSelect, size_t dataSize, size_t timeout) noexcept = 0;  // 
       
    virtual Status write(SPIChipSelect chipSelect, const uint8_t* mBuffer, size_t mBufferSize, size_t timeout) noexcept = 0;
	//virtual Status write("указатель на шину, к которой подкл периферия", "указатель на данные (массив данных)", "размер массива (или пакета?) с данными", "время передачи нашей информации в массиве (или в пакете?)") 
    
    PeripheralType getPeripheralType() const noexcept override {  // тут ттоже будет переменная
        return 0xb2f3f848U;
    }
    
    bool isPeripheralTypeParent(PeripheralType peripheralType) const noexcept override {
        if (0xb2f3f848U == peripheralType) {
            return true;
        }
        return false;
    }
	
	const PeripheralType peripheralType = 0xb2f3f848U;
};

#endif  // ISPI_H