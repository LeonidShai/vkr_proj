#ifndef I2C_H
#define I2C_H

#include "periherial.h"

class II2c : public IPeripheral {
	

public:

    virtual std::tuple<Status, uint8_t*, size_t> read(uint16_t devaddress, size_t dataSize, size_t timeout) noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия

	
	virtual Status write(uint16_t devaddress, const uint8_t* mBuffer, size_t bufferSize, size_t timeout) noexcept = 0;
	//virtual Status write(идентификатор устройства, адрес устройства, массив данных передаваемый, размер массива данных, время передачи) noexcept = 0;

    PeripheralType getPeripheralType() const noexcept override {
        return 0x81d81a77U; 
    }
 
    bool isPeripheralTypeParent(PeripheralType peripheralType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if (0x81d81a77U == peripheralType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeripheralType peripheralType = 0x81d81a77U;
	
};

#endif  // I2C_H