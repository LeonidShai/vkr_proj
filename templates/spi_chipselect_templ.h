#ifndef SPICHIPSELECT_H
#define SPICHIPSELECT_H
#include <cstdint>

enum class SPIChipSelect : uint8_t {
	{% for DEVICE in DEVICES %}
	{{DEVICE}},{% endfor %}
	INVALID_ARG
};

SPIChipSelectID getSPIChipSelectIDByString(const char* s) noexcept;
	
#endif // SPICHIPSELECT_H
