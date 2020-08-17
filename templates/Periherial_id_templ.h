// Шаблон PeriherialID

#include <cstdint>
 
enum class PeriherialID : uint32_t {
    
	{{PowerButton}};  // генерация необходимого кол-ва кнопок PowerButton_1, PowerButton_2, ..., PowerButton_n
	
    MemoryButton;


// получение названия со строки??это к примеру, если хотим добавить кнопку в уже сгенерированной проге?

PeriherialID getPeriherialIDByString(const char* s) noexcept {
    if (0 == std::strcmp(s, "{{PowerButton}}")) {
        return PeriherialID::{{PowerButton}};
    }
    
    return PeriherialID::Invalid;
}

};

