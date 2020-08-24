// Шаблон PeriherialID

#include <cstdint>
 
enum class PeriherialID : uint32_t {
    
	{{device}};  // генерация необходимого кол-ва кнопок PowerButton_1, PowerButton_2, ..., PowerButton_n
	
//  Примеры:
//  PowerButton
//  MemoryButton;


// получение названия со строки??это к примеру, если хотим добавить кнопку в уже сгенерированной проге?

	PeriherialID getPeriherialIDByString(const char* s) noexcept {
		if (0 == std::strcmp(s, "{{device}}")) {
			return PeriherialID::{{device}};
		}
    
		return PeriherialID::INVALID_ARG;
	}

}
