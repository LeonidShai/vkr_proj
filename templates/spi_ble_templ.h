// шаблон для периферии SPI

// #include "ISPIPin.h"

class STM32{{SPINAME}} : public ISpi {

	{% for PINNAME in PINNAMES %}stm32spi {{PINNAME}};
	{% endfor %}
	SPI_HandleTypeDef {{SPINUM}};  // hspi1, hspi2

public:
	Status init() noexcept override {
		
		{% for PINNAME in PINNAMES %}{{PINNAME}}.init();  // SPI1_SCK, SPI1_MISO, SPI1_MOSI, BLE, MEM
		{% endfor %}
		
		{% for INIT in INITS %}{{INIT}}
		{% endfor %}
		
		/*
		hspi1.Instance = SPI1;
		hspi1.Init.Mode = SPI_MODE_MASTER;
		hspi1.Init.Direction = SPI_DIRECTION_2LINES;
		hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
		hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
		hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
		hspi1.Init.NSS = SPI_NSS_SOFT;
		hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
		hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
		hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
		hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
		hspi1.Init.CRCPolynomial = 10;
		*/
		
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
						// Все негативные ситуации
						return Status::Error;
					}
			{% else %}
				}else if (chipSelect == SPIChipSelect::{{SPIDEVS[I]}}) {  // BLE
					m{{ISPINUM}}CS{{SPIDEVS[I]}}.write(false);
					
					auto halStatus = HAL_SPI_Transmit(&{{SPINUM}}, mBufferuf, buffersize, timeout);
					
					m{{SPINUM}}CS{{SPIDEVS[I]}}.write(true);
					
					if (halStatus != HAL_OK) {
						// Все негативные ситуации
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
        return {{CRCID}}U; //STM32SPI1
    };
    
    const char* getName() const noexcept override {
        return "STM32{{SPINAME}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PIN1}}", "{{PIN2}}", "{{PIN3}}";  // откуда узнаём?
    }

	bool mInit{false};	
}

