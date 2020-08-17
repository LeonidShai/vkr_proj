#include <cstdint>

enum class SPIChipSelect : uint8_t {
	MEM, // всегда же будет?
	{{BLE}}  //устройство, например, блютус, возможны и другие...(например?)
}

SPIChipSelectID getSPIChipSelectIDByString(const char* s) noexcept {
    if (0 == std::strcmp(s, "{{BLE}}")) {
        return SPIChipSelectID::{{BLE}};
    }
    
    return SPIChipSelectID::Invalid;
}
