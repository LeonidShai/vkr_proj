#ifndef IUART_H
#define IUART_H

#include "periherial.h"

class IUart : public IPeripheral {
	

public:

    virtual std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия

	
	virtual Status write(const uint8_t* mBuffer, size_t bufferSize, size_t timeout) noexcept = 0;
	//virtual Status write(массив данных передаваемый, размер массива данных, время передачи) noexcept = 0;

    PeripheralType getPeripheralType() const noexcept override {
        return 0x6c663df3U; 
    }
 
    bool isPeripheralTypeParent(PeripheralType peripheralType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if (0x6c663df3U == peripheralType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeripheralType peripheralType = 0x6c663df3U;
	
};

#endif  // IUART_H