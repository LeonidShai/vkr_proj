// шаблон для периферии iuart_device

#include "I_UART.h"

class STM32{{UARTDEVICE}} : public IUart {
	
private:

	stm32UART device;
	UART_HandleTypeDef huart;

public:
	Status init() noexcept override {
		device.init();
		
		huart1.Instance = USART1;
		huart1.Init.BaudRate = 115200;
		huart1.Init.WordLength = UART_WORDLENGTH_8B;
		huart1.Init.StopBits = UART_STOPBITS_1;
		huart1.Init.Parity = UART_PARITY_NONE;
		huart1.Init.Mode = UART_MODE_TX_RX;
		huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
		huart1.Init.OverSampling = UART_OVERSAMPLING_16;
		if (HAL_UART_Init(&huart) != HAL_OK)
		{
			mInit = true;
			return Status::SUCCESS;
		}
	}
		
	Status write(const uint8_t* buf, size_t size, size_t timeout) noexcept override {
	
	if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
			
			// Запись из hal 
		auto halStatus = HAL_UART_Transmit(mUARTx, mBuffer, bufferSize, timeout);
        return Status::SUCCESS; 							

	}
	
	std::tuple<Status, uint8_t*, size_t> read(size_t dataSize, size_t timeout) {
		
		if (!mInit) {
            return { Status::InvalidArgument, nullptr, 0U}
        }
    
		auto halStatus = HAL_UART_Receive(mUARTx, mBuffer, bufferSize, timeout);
		return {Status::SUCCESS, mBuffer, bufferSize}
    }

    bool isPeriherialParent(PeriherialType periherialType) const noexcept override {
        return IUart::isPeriherialParent(periherialType);
    }

    PeriherialID getPeriherialID() const noexcept override {
        return {{0x81d89d2a}}; //STM32UARTDEVICE
    };
    
    const char* getName() const noexcept override {
        return "{{STM32UARTDEVICE}}";
    }
    
    const char* getPortName() const noexcept override {
        return "{{PA1}}";  // откуда узнаём?
    }

	bool mInit{false};		
}
