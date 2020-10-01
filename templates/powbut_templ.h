#ifndef {{PINNAME}}_{{PIN}}_H
#define {{PINNAME}}_{{PIN}}_H

#include "i_pin.h"
#include "main.h"

class STM32{{PINNAME}} : IPin {
	
private:
	GPIO_TypeDef* mGPIOx={{PORTNAME}};
	uint16_t mGPIO_Pin={{PINNAME}};

public:

    Status init() noexcept override {  
	
	  GPIO_InitTypeDef GPIO_InitStruct = {0};
	  
	  __HAL_RCC_{{CLCEN}}_CLK_ENABLE();
	  
	  GPIO_InitStruct.Pin = {{PINNAME}};
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
            HAL_GPIO_WritePin({{PORTNAME}}, {{PINNAME}}, pinState);
            return Status::SUCCESS;
        }
        return Status::NOT_INIT;
    }
    
    bool isPeripheralParent(PeripheralType peripheralType) const noexcept override {
        return IPin::isPeripheralParent(peripheralType);
    }

    PeripheralID getPeripheralID() const noexcept override {
        return {{IDKEY}}U;
    };
    
    const char* getName() const noexcept override {
        return "{{PINNAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN}}";
    }

bool mInit{false};
};

#endif