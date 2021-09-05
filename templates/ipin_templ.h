#ifndef IPIN_H
#define IPIN_H

#include "periherial.h"
#include <tuple>

class IPin : public IPeripheral {

public:

    virtual std::pair<Status, bool> read() noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия
    
    virtual Status write(bool state) noexcept = 0;  // запись при инициализации какой-либо периферии GPIO_PIN, SPI, I2C

    PeripheralType getPeripheralType() const noexcept override {
        return 0xb5d17aaaU; 
    }
 
    bool isPeripheralTypeParent(PeripheralType peripheralType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if (0xb5d17aaaU == peripheralType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeripheralType peripheralType = 0xb5d17aaaU;
};

#endif // I_PIN
