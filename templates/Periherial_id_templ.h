#ifndef ID_PERIHERIAL_H
#define ID_PERIHERIAL_H

#include <cstdint>
#include <cstring>
 
enum class PeripheralID : uint32_t {
	{% for DEVICE in DEVICES %}
	{{DEVICE}},{% endfor %}
	INVALID_ARG
};

PeripheralID getPeripheralIDByString(const char* s) noexcept;

#endif // ID_PERIHERIAL_H
