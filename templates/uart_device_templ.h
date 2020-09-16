

class STM32{{NAME}} : public IUart {
	
private:

	{% for PINNAME in PINNAMES %}stm32uart {{PINNAME}};
	{% endfor %}
	UART_HandleTypeDef {{I2CNUM}};

public:
	Status init() noexcept override {
		{% for PINNAME in PINNAMES %}{{PINNAME}}.init();
		{% endfor %}
		
		{% for INIT in INITS %}{{INIT}}
		{% endfor %}

		if (HAL_UART_Init(&{{I2CNUM}}) != HAL_OK)
		{
			mInit = true;
			return Status::SUCCESS;
		}
	}
		
	Status write(const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	
	if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }

		auto halStatus = HAL_UART_Transmit(&{{I2CNUM}}, mBuffer, bufferSize, timeout);
        return Status::SUCCESS; 							

	}
	
	std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
    
		auto halStatus = HAL_UART_Receive(&{{I2CNUM}}, mBuffer, bufferSize, timeout);
		return {Status::SUCCESS, mBuffer, bufferSize}
    }

    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return IUart::isPeriherialParent(periherialType);
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
