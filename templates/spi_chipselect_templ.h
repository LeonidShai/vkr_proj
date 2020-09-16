#include <cstdint>

enum class SPIChipSelect : uint8_t {
	{% for DEVICE in DEVICES %}
	{{DEVICE}};{% endfor %}

	{% for DEVICE in DEVICES %}
	SPIChipSelectID getSPIChipSelectIDByString(const char* s) noexcept {
		if (0 == std::strcmp(s, "{{DEVICE}}")) {
			return SPIChipSelectID::{{DEVICE}};
		}
    
		return SPIChipSelectID::INVALID_ARG;
	}
	{% endfor %}
}
