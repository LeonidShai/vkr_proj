#include "IPeriherial.h"

class ISPI : public IPeriherial{  // где чchipselect используем?
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
    virtual Status write(const uint8_t* data, size_t dataSize) noexcept = 0;
    
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