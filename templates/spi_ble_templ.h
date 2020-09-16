

class STM32{{SPINAME}} : public ISpi {

	{% for PINNAME in PINNAMES %}stm32spi {{PINNAME}};
	{% endfor %}
	SPI_HandleTypeDef {{SPINUM}};

public:
	Status init() noexcept override {
		
		{% for PINNAME in PINNAMES %}{{PINNAME}}.init();
		{% endfor %}
		
		{% for INIT in INITS %}{{INIT}}
		{% endfor %}
		
		if (HAL_SPI_Init(&{{SPINUM}}) != HAL_OK)
			{
				mInit = true;
				return Status::SUCCESS;
			}
		}
		
	Status write(SPIChipSelect chipSelect, const uint8_t* buffer, size_t dataSize, size_t timeout) noexcept override {
		
		if (!mInit) {
			return Status::NOT_INIT;
		}
		
		if (dataSize > mBufferSize) {
			return Status::INVALID_ARG;
		}
		
		if (buffer==nullptr) {
			return Status::INVALID_ARG;
		}
		
		
		{% for I in range(CH) %}
			{% if I == 0 %}
				if (chipSelect == SPIChipSelect::{{SPIDEVS[I]}}) {
					m{{SPINUM}}CS{{SPIDEVS[I]}}.write(false);
					
					auto halStatus = HAL_SPI_Transmit(&{{SPINUM}}, mBufferuf, buffersize, timeout);
					
					m{{SPINUM}}CS{{SPIDEVS[I]}}.write(true);
					
					if (halStatus != HAL_OK) {
						return Status::Error;
					}
			{% else %}
				}else if (chipSelect == SPIChipSelect::{{SPIDEVS[I]}}) {
					m{{ISPINUM}}CS{{SPIDEVS[I]}}.write(false);
					
					auto halStatus = HAL_SPI_Transmit(&{{SPINUM}}, mBufferuf, buffersize, timeout);
					
					m{{SPINUM}}CS{{SPIDEVS[I]}}.write(true);
					
					if (halStatus != HAL_OK) {
						return Status::Error;
					}
			{% endif %}
		{% endfor %}	
		} else {
			
			return Status::INVALID_ARG;
		}
			
			
    	return Status::SUCCESS;
		}
					
	std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (dataSize > mBufferSize) {
            return { Status::InvalidArgument, nullptr, 0U };
        }
    
		auto halStatus = HAL_SPI_Receive(&{{SPINUM}}, mBuffer, bufferSize, timeout);
		return {Status::SUCCESS, mBuffer, bufferSize};
    }
		
    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return ISpi::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{CRCID}}U;
    };
    
    const char* getName() const noexcept override {
        return "STM32{{SPINAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN1}}", "{{PIN2}}", "{{PIN3}}";
    }

	bool mInit{false};	
}

