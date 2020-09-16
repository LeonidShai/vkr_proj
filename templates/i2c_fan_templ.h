// шаблон для периферии i2C_fan

// #include "I_I2C.h"

class STM32{{NAME}} : public II2c {
	
private:

	{% for PINNAME in PINNAMES %}stm32i2c {{PINNAME}};
	{% endfor %}
	// I2C1_Dev_SCL;
	// I2C1_Dev_SDA;
	I2C_HandleTypeDef {{I2CNUM}};  // hi2c1

public:
	Status init() noexcept override {
		
		{% for PINNAME in PINNAMES %}{{PINNAME}}.init();
		{% endfor %}
		// I2C1_Dev_SCL.init();
		// I2C1_Dev_SDA.init();
		{% for INIT in INITS %}{{INIT}}
		{% endfor %}
		/*
		hi2c1.Instance = I2C1;
		hi2c1.Init.ClockSpeed = 100000;
		hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
		hi2c1.Init.OwnAddress1 = 0;
	    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
	    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
	    hi2c1.Init.OwnAddress2 = 0;
	    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
	    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
		*/
		if (HAL_I2C_Init(&{{I2CNUM}}) != HAL_OK)  // не инициализировать
		{
			mInit = true;
			return Status::SUCCESS;
		}
	}
	
	Status deinit() noexcept override {// так вот будет:
		if(hi2c->Instance==I2C1){
			return Status::SUCCESS;
		}
	}
		
	Status write(const uint16_t* devaddress, const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	
	if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
			
			// Запись из hal 
		auto halStatus = HAL_I2C_Master_Transmit(&{{I2CNUM}}, devaddress, mBuffer, buffersize, timeout);
			//HAL_SPI_Transmit({{mSPIx}}, {{mBufferuf}}, {{buffersize}}, {{timeout}});	// пример:
			//HAL_SPI_Transmit({{GPIOB}}, {{SPI_BLE}}, {{buffersize}}, {{timeout}});  ннепонятно, где берём buffersize и timeout
        return Status::SUCCESS; 								//

	}
	
	std::tuple<Status, uint8_t*, size_t> read(uint16_t* devadress, size_t dataSize, size_t timeout) {
		
		if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
    
		auto halStatus = HAL_I2C_Master_Receive(&{{I2CNUM}}, devaddress, mBuffer, buffersize, timeout)
		return {Status::SUCCESS, mBuffer, bufferSize}
    }
	
    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return II2c::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{CRCID}}U; //STM32FAN
    };
    
    const char* getName() const noexcept override {
        return "STM32{{NAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN1}}", "{{PIN2}}";
    }

	bool mInit{false};			
}
