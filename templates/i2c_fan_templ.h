

class STM32{{NAME}} : public II2c {
	
private:

	{% for PINNAME in PINNAMES %}stm32i2c {{PINNAME}};
	{% endfor %}

	I2C_HandleTypeDef {{I2CNUM}};

public:
	Status init() noexcept override {
		
		{% for PINNAME in PINNAMES %}{{PINNAME}}.init();
		{% endfor %}

		{% for INIT in INITS %}{{INIT}}
		{% endfor %}
		
		if (HAL_I2C_Init(&{{I2CNUM}}) != HAL_OK)
		{
			mInit = true;
			return Status::SUCCESS;
		}
	}
	
	Status deinit() noexcept override {
		if(hi2c->Instance==I2C1){
			return Status::SUCCESS;
		}
	}
		
	Status write(const uint16_t* devaddress, const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	
		if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
 
		auto halStatus = HAL_I2C_Master_Transmit(&{{I2CNUM}}, devaddress, mBuffer, buffersize, timeout);
		return Status::SUCCESS;

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
        return {{CRCID}}U;
    };
    
    const char* getName() const noexcept override {
        return "STM32{{NAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN1}}", "{{PIN2}}";
    }

	bool mInit{false};			
}
