// шаблон для периферии SPI

#include "ISPIPin.h"

class STM32{{SPI1}} : public ISPI {
	
private:
	SPI1_CS_BLE mSPI1CSBLE;
	SPI1_CS_MEM mSPI1CSMEM;
	SPI_HandleTypeDef hspi1;

public:
	Status init() noexcept override {
		
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
		
	Status write(SPIChipSelect chipSelect, const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	   	if (dataSize > mBufferSize){  // вот так вот?
		//if (chipSelect == SPIChipSelect::MEM) {
			//mSPI1CSBLE.write(false);
			
			// Запись из hal -- видимо надо ещё раз;
			HAL_SPI_Transmit({{mSPIx}}, {{mBufferuf}}, {{buffersize}}, {{timeout}});	// пример:
			//HAL_SPI_Transmit({{GPIOB}}, {{SPI_BLE}}, {{buffersize}}, {{timeout}});  ннепонятно, где берём buffersize и timeout
            return Status::SUCCESS; 								//
			
			//mSPI1CSBLE.write(true);
		}
		return Status::NOT_INIT;
	}
	
	std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (dataSize > mBufferSize) {
            return { Status::InvalidArgument, nullptr, 0U }
        }
    
		HAL_SPI_Receive(mSPIx, mBuffer, bufferSize, timeout);
		return {Status::SUCCESS; bufferSize, timeout}
    }
		
   }
}
