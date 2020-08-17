// создание переферии GPIO_PIN, SPI, I2C
#include "PeriherialID.h"
#include "SPIChipSelectID.h"

class IPeriherial {

public:
 
 using PeriherialType = uint32_t;

 enum class Status : uint32_t {
    SUCCESS,
    FAILURE,
    BUSY,
    NOT_INIT
 };
 
 virtual ~IPeriherial() noexcept = default;
 
 virtual Status init() noexcept = 0;

 virtual Status deinit() noexcept = 0;

 virtual PeriherialType getPeriherialType() const noexcept = 0;  // метод создания GPIO_PIN, SPI, I2C
 
 virtual bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept = 0; // метод для проверки, чтобы убедиться, что PowerButton точно GPIO_PIN
 
 virtual PeriherialID getPeriherialID() const noexcept = 0;
 
 virtual SPIChipSelect getSPIChipSelect() const noexcept = 0;  // наверное, эту строку нужно добавить, не будет ли чего-то похожего для I2C?
 
 virtual const char* getName() const noexcept = 0;

};
