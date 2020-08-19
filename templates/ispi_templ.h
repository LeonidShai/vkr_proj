#include "IPeriherial.h"

class ISPI : public IPeriherial{
public:
    ISPI(uint8_t* buffer, size_t bufferSize) : mBuffer(buffer), mBufferSize(bufferSize) // здесь непонятно?
    
    virtual std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) noexcept = 0;  // может вот так нужно?
    
/*    
    }
	if (dataSize > mBufferSize) {
            return { Status::InvalidArgument, nullptr, 0U }
        }
    
    HAL_SPI_Receive(mSPIx, mBuffer, bufferSize, timeout);
    
    }
*/    
    virtual Status write(SPIChipSelect chipSelect, const uint8_t* mBuffer, size_t mBufferSize, size_t timeout) noexcept = 0;
	//virtual Status write("указатель на шину, к которой подкл периферия", "указатель на данные (массив данных)", "размер массива (или пакета?) с данными", "время передачи нашей информации в массиве (или в пакете?)") 
    
    PeriherialType getPeriherialType() const noexcept override {  // тут ттоже будет переменная
        return {{0xb5d17aaaU}};
    }
    
    bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept override {
        if ({{0xb5d17aaaU}} == periherialType) {
            return true;
        }
        return false;
    }
	
	const PeriherialType Type = {{0xb5d17aaaU}};  // а вот енто сюда не нужно??
      
protected:
    
    uint8_t* mBuffer;
    size_t mBufferSize;
      
}