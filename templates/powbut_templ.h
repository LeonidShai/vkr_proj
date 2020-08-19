// шаблон для PowerBut_1, PowerBut_2, ..., PowerBut_n

#include "IPin.h"

class STM32{{PowerButton}} : IPin {
	
private:
	GPIO_TypeDef* mGPIOx={{GPIOA}};
	uint16_t mGPIO_Pin={{PowerButton}};

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main  
	
	  GPIO_InitTypeDef GPIO_InitStruct = {0};
	  
	  __HAL_RCC_{{GPIOA}}_CLK_ENABLE();
	  
	  HAL_GPIO_WritePin({{GPIOA}}, {{PowerButton}}_Pin, {{GPIO_PIN_RESET}});  // а может это толь в метод write??
	  
	  GPIO_InitStruct.Pin = {{PowerButton}}_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init({{GPIOA}}, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }

    std::pair<Status, bool> read() noexcept override {
        if (mInit) {
            auto state = (GPIO_PIN_SET == HAL_GPIO_ReadPin({{GPIOA}}, {{PowerButton}});
            return {Status::SUCCESS, state};
        }    
        return {Status::NOT_INIT, false};
    }
    
    Status write(bool state) noexcept override {
        if (mInit) {
            auto pinState = state ? GPIO_PIN_SET : GPIO_PIN_RESET;
            HAL_GPIO_WritePin({{GPIOA}}, {{PowerButton}}, {{GPIO_PIN_RESET}});
            return Status::SUCCESS;
        }
        return Status::NOT_INIT;
    }
    
    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return IPin::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{0x1e2953f2U}}; 
    };
    
    const char* getName() const noexcept override {
        return "{{PowerButton}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PA1}}";  // откуда узнаём?
    }

bool mInit{false};
};
