#include "periherial.h"

class IUart : public IPeriherial {
	

public:

    virtual std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия

	
	virtual Status write(const uint8_t* mBuffer, size_t bufferSize, size_t timeout) noexcept = 0;
	//virtual Status write(массив данных передаваемый, размер массива данных, время передачи) noexcept = 0;

    PeriherialType getPeriherialType() const noexcept override {
        return 0x6c663df3U; 
    }
 
    bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if (0x6c663df3U == periherialType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeriherialType Type = 0x6c663df3U;
	
};