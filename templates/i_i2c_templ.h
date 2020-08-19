// шаблон для I_I2С

#include "IPeriherial.h"

class I_I2C : public IPeriherial {

public:

    virtual std::tuple<Status, uint16_t*, uint8_t*, size_t> read(size_t dataSize, size_t timeout) noexcept = 0;  // чтение, если на какой-то пин подключена какя-либо периферия
    
    virtual Status write(const uint8_t* data, size_t dataSize) noexcept = 0;  // запись при инициализации какой-либо периферии GPIO_PIN, SPI, I2C, а не мало? может та:
	
	//virtual Status write(I2CChipSelect chipSelect, const uint16_t* devaddress, const uint8_t* buf, size_t size, size_t timeout) noexcept = 0;

    PeriherialType getPeriherialType() const noexcept override {
        return {{0xb5d17aaaU}};  // crc32 здесь будет переменная 
    }
 
    bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept override {  // является ли IPIN родителем PowerButton, или др периферии
        if ({{0xb5d17aaaU}} == periherialType) {
            return true;
        }
        return false;
    }
    
    virtual const char* getPortName() const noexcept = 0;  // метод для установки имени порта, на который подключается периферия
	
	const PeriherialType Type = {{0xb5d17aaaU}};
	
protected:
    
    //uint16_t* devaddress;
	uint8_t* mBuffer;
    size_t mBufferSize;
};


HAL_I2C_Master_Transmit(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *pData, uint16_t Size, uint32_t Timeout);
HAL_I2C_Master_Receive(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *pData, uint16_t Size, uint32_t Timeout);

HAL_SPI_Transmit(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size, uint32_t Timeout);