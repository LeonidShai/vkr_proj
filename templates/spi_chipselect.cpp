#include "spi_chipselect.h"
#include <cstdint>
#include <cstring>

SPIChipSelect getSPIChipSelectIDByString(const char* s) noexcept {
	{% for I in range(CH) %}
		{% if I == 0 %}
		if (0 == std::strcmp(s, "{{DEVICES[I]}}")) {
			return SPIChipSelect::"{{DEVICES[I]}}";
		}{% else %}
		else if (0 == std::strcmp(s, "{{DEVICES[I]}}")) {
			return SPIChipSelect::"{{DEVICES[I]}}";
		}{% endif %}{% endfor %}

		return SPIChipSelect::INVALID_ARG;
	}
