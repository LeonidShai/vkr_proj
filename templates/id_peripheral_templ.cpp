#include "id_periherial.h"

	PeripheralID getPeripheralIDByString(const char* s) noexcept {
	{% for I in range(CH) %}
		{% if I == 0 %}	
		if (0 == std::strcmp(s, "{{DEVICES[I]}}")) {
			return PeripheralID::{{DEVICES[I]}};
		}{% else %}
		else if (0 == std::strcmp(s, "{{DEVICES[I]}}")){
			return PeripheralID::{{DEVICES[I]}};
		}{% endif %}{% endfor %}
    
		return PeripheralID::INVALID_ARG;
	}
