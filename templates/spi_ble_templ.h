// шаблон для периферии SPI

#include "ISPIPin.h"

class STM32{{SPI1}} : public ISpi {
	
	SPI_TypeDef* mSPIx={{GPIOB}}; 

	SPI1_CS_BLE mSPI1CSBLE;
	SPI1_CS_MEM mSPI1CSMEM;
	SPI_HandleTypeDef hspi1;

public:
	Status init() noexcept override {
		
		mSPI1CSBLE.init();
		mSPI1CSMEM.init();
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
		if (HAL_SPI_Init(&hspi1) != HAL_OK)
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
		
		
		if (chipSelect == SPIChipSelect::MEM) {
			mSPI1CSMEM.write(false);
			
			auto halStatus = HAL_SPI_Transmit({{mSPIx}}, {{mBufferuf}}, {{buffersize}}, {{timeout}});
			
			mSPI1CSMEM.write(true);
			
			if (halStatus != HAL_OK) {
				// Все негативные ситуации
				return Status::Error;
			}
		} else if (chipSelect == SPIChipSelect::BLE) {
			mSPI1CSBLE.write(false);
			
			auto halStatus = HAL_SPI_Transmit({{mSPIx}}, {{mBufferuf}}, {{buffersize}}, {{timeout}});
			
			mSPI1CSBLE.write(true);
			
			if (halStatus != HAL_OK) {
				// Все негативные ситуации
				return Status::Error;
			}
			
			
		} else {
			
			return Status::INVALID_ARG;
		}
			
			
    	return Status::SUCCESS;
		}
		
		
	
	std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (dataSize > mBufferSize) {
            return { Status::InvalidArgument, nullptr, 0U };
        }
    
		auto halStatus = HAL_SPI_Receive(mSPIx, mBuffer, bufferSize, timeout);
		return {Status::SUCCESS, mBuffer, bufferSize};
    }
		
    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return ISpi::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{0xc50864f7}}; //STM32SPI1
    };
    
    const char* getName() const noexcept override {
        return "{{STM32SPI1}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PA1}}";  // откуда узнаём?
    }

	bool mInit{false};	
}

