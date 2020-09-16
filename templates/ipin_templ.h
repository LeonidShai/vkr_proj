#include "periherial.h"

class IPin : public IPeriherial {

public:

    virtual std::pair<Status, bool> read() noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия
    
    virtual Status write(bool state) noexcept = 0;  // запись при инициализации какой-либо периферии GPIO_PIN, SPI, I2C

    PeriherialType getPeriherialType() const noexcept override {
        return 0xb5d17aaaU; 
    }
 
    bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if (0xb5d17aaaU == periherialType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeriherialType Type = {{0xb5d17aaaU}};
};
