#include "id_periherial.h"
#include "spi_chipselect.h"

class IPeriherial {

public:
 
	using PeriherialType = uint32_t;

	enum class Status : uint32_t {
		SUCCESS,
		FAILURE,
		BUSY,
		NOT_INIT,
		INVALID_ARG,
		ERROR;
	}
 
virtual ~IPeriherial() noexcept = default;
 
virtual Status init() noexcept = 0;

virtual Status deinit() noexcept = 0;

virtual PeriherialType getPeriherialType() const noexcept = 0;  // метод создания GPIO_PIN, SPI, I2C
 
virtual bool isPeriherialTypeParent(PeriherialType periherialType) const noexcept = 0; // метод для проверки, чтобы убедиться, что PowerButton точно GPIO_PIN
 
virtual PeriherialID getPeriherialID() const noexcept = 0;
 
virtual const char* getName() const noexcept = 0;

}
