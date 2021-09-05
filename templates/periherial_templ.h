#ifndef I_PERIHERIAL_H
#define I_PERIHERIAL_H

#include "id_periherial.h"

enum class Status : uint32_t {
	SUCCESS,
	FAILURE,
	BUSY,
	NOT_INIT,
	INVALID_ARG,
	INIT_ALREADY,
	ERROR
};

class IPeripheral {

public:
 
	using PeripheralType = uint32_t;
 
virtual ~IPeripheral() noexcept = default;
 
virtual Status init() noexcept = 0;

virtual Status deinit() noexcept = 0;

virtual PeripheralType getPeripheralType() const noexcept = 0;  // метод создания GPIO_PIN, SPI, I2C
 
virtual bool isPeripheralTypeParent(PeripheralType peripheralType) const noexcept = 0; // метод для проверки, чтобы убедиться, что PowerButton точно GPIO_PIN
 
virtual PeripheralID getPeripheralID() const noexcept = 0;
 
virtual const char* getName() const noexcept = 0;

};

#endif // I_PERIHERIAL_H
