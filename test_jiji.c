
class STM32pinbut_1_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOA_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOA, pinbut_1_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_1_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_2_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOA_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOA, pinbut_2_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_2_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_3_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOA_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOA, pinbut_3_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_3_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_7_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOA_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOA, pinbut_7_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_7_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_8_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOA_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOA, pinbut_8_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_8_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_9_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOB_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOB, pinbut_9_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_9_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_10_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOB_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOB, pinbut_10_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_10_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_12_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOB_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOB, pinbut_12_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_12_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_11_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOB_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOB, pinbut_11_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_11_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_13_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOB_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOB, pinbut_13_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_13_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_4_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOC_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOC, pinbut_4_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_4_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_5_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOC_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOC, pinbut_5_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_5_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}



class STM32pinbut_6_Pin : IPin {

public:

    Status init() noexcept override {
      // Нужно скопировать всё, что CubeMX сгенирировал в init блоке в начале функции main
	  
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  /* GPIO Ports Clock Enable */
	  __HAL_RCC_GPIOC_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOC, pinbut_6_Pin, GPIO_PIN_RESET);

	  /*Configure GPIO pin : powerbut1_Pin */
	  GPIO_InitStruct.Pin = pinbut_6_Pin;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
      
      mInit = true;
      return Status::SUCCESS;
    }
}


