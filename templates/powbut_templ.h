// шаблон для PowerBut_1, PowerBut_2, ..., PowerBut_n

// #include "IPin.h"

class STM32{{PINNAME}} : IPin {
	
private:
	GPIO_TypeDef* mGPIOx={{PORTNAME}};
	uint16_t mGPIO_Pin={{PINNAME}};

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main  
	
	  GPIO_InitTypeDef GPIO_InitStruct = {0};
	  
	  __HAL_RCC_{{CLCEN}}_CLK_ENABLE();
	  
	  GPIO_InitStruct.Pin = {{PINNAME}}_Pin;
	  {% for INIT in INITS %}{{INIT}}
	  {% endfor %}HAL_GPIO_Init({{PORTNAME}}, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }

    std::pair<Status, bool> read() noexcept override {
        if (mInit) {
            auto state = HAL_GPIO_ReadPin({{PORTNAME}}, {{PINNAME}});
            return {Status::SUCCESS, state};
        }    
        return {Status::NOT_INIT, false};
    }
    
    Status write(bool state) noexcept override {
        if (mInit) {
            auto pinState = state ? GPIO_PIN_SET : GPIO_PIN_RESET;
            HAL_GPIO_WritePin({{PORTNAME}}, {{PINNAME}}, GPIO_PIN_RESET);
            return Status::SUCCESS;
        }
        return Status::NOT_INIT;
    }
    
    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return IPin::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{IDKEY}}U; //STM32PowerButton
    };
    
    const char* getName() const noexcept override {
        return "{{PINNAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN}}";
    }

bool mInit{false};
};
