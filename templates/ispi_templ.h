#include "IPeriherial.h"

class ISpi : public IPeriherial{
	
public:
    //ISPI(uint8_t* buffer, size_t bufferSize) : mBuffer(buffer), mBufferSize(bufferSize){}
    
    virtual std::tuple<Status, uint8_t*, size_t> read(SPIChipSelect chipSelect, size_t dataSize, size_t timeout) noexcept = 0;  // 
       
    virtual Status write(SPIChipSelect chipSelect, const uint8_t* mBuffer, size_t mBufferSize, size_t timeout) noexcept = 0;
	//virtual Status write("указатель на шину, к которой подкл периферия", "указатель на данные (массив данных)", "размер массива (или пакета?) с данными", "время передачи нашей информации в массиве (или в пакете?)") 
    
    PeriherialType getPeriherialType() const noexcept override {  // тут ттоже будет переменная
        return 0xb2f3f848;
    }
    
    bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept override {
        if (0xb2f3f848 == periherialType) {
            return true;
        }
        return false;
    }
	
	const PeriherialType Type = 0xb2f3f848; // потом переименовать
}