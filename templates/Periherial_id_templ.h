// Шаблон PeriherialID

#include <cstdint>
 
enum class PeriherialID : uint32_t {
	{% for DEVICE in DEVICES %}
	{{DEVICE}};{% endfor %}  
// генерация необходимого кол-ва кнопок PowerButton_1, PowerButton_2, ..., PowerButton_n
	
//  Примеры:
//  PowerButton
//  MemoryButton;


// получение названия со строки??это к примеру, если хотим добавить кнопку в уже сгенерированной проге?

	{% for DEVICE in DEVICES %}
	PeriherialID getPeriherialIDByString(const char* s) noexcept {
		if (0 == std::strcmp(s, "{{DEVICE}}")) {
			return PeriherialID::{{DEVICE}};
		}
    
		return PeriherialID::INVALID_ARG;
	}
	{% endfor %}

}
