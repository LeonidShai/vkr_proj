#include <cstdint>

enum class SPIChipSelect : uint8_t {
	{{device}};
	
//  Devices examples:
//  	BLE,
//  	MEM


	SPIChipSelectID getSPIChipSelectIDByString(const char* s) noexcept {
		if (0 == std::strcmp(s, "{{device}}")) {
			return SPIChipSelectID::{{device}};
		}
    
		return SPIChipSelectID::INVALID_ARG;
	}
}
