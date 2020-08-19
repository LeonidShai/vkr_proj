// шаблон для периферии i2C_fan

#include "I_I2C.h"

class STM32{{FAN}} : public I_I2C {
	
private:
	//SPI1_CS_BLE mSPI1CSBLE;
	//SPI1_CS_MEM mSPI1CSMEM;
	//SPI_HandleTypeDef hspi1;

public:
	Status init() noexcept override {
		
		hi2c1.Instance = I2C1;
		hi2c1.Init.ClockSpeed = 100000;
		hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
		hi2c1.Init.OwnAddress1 = 0;
	    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
	    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
	    hi2c1.Init.OwnAddress2 = 0;
	    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
	    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
		if (HAL_I2C_Init(&hi2c1) != HAL_OK)  // не инициализировать
		{
			mInit = true;
			return Status::SUCCESS;
		}
	}
		
	Status write(I2CChipSelect chipSelect, const uint16_t* devaddress, const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	   	if (mInit){  // вот так вот?
			
			// Запись из hal 
			HAL_I2C_Master_Transmit({{mI2Cx}}, {{devaddress}}, {{FAN}}, {{buffersize}}, {{timeout}});
			//HAL_SPI_Transmit({{mSPIx}}, {{mBufferuf}}, {{buffersize}}, {{timeout}});	// пример:
			//HAL_SPI_Transmit({{GPIOB}}, {{SPI_BLE}}, {{buffersize}}, {{timeout}});  ннепонятно, где берём buffersize и timeout
            return Status::SUCCESS; 								//
			
		}
		return Status::NOT_INIT;
	}
	
	std::tuple<Status, uint16_t*, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (mInit) {
            return { Status::InvalidArgument, nullptr, nullptr, 0U }
        }
    
		HAL_I2C_Master_Receive({{mI2Cx}}, {{devaddress}}, {{FAN}}, {{buffersize}}, {{timeout}})
		return {Status::SUCCESS; bufferSize, timeout}
    }
		
   }
}
