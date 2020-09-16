#include <cstdint>
 
enum class PeriherialID : uint32_t {
	{% for DEVICE in DEVICES %}
	{{DEVICE}};{% endfor %}

	{% for DEVICE in DEVICES %}
	PeriherialID getPeriherialIDByString(const char* s) noexcept {
		if (0 == std::strcmp(s, "{{DEVICE}}")) {
			return PeriherialID::{{DEVICE}};
		}
    
		return PeriherialID::INVALID_ARG;
	}
	{% endfor %}
}
