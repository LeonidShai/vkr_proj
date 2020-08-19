#include <cstdint>

enum class I2CChipSelect : uint8_t {
	MEM, // всегда же будет?
	{{FAN}}
}

I2CChipSelectID getI2CChipSelectIDByString(const char* s) noexcept {
    if (0 == std::strcmp(s, "{{FAN}}")) {
        return I2CChipSelectID::{{FAN}};
    }
    
    return I2CChipSelectID::Invalid;
}
