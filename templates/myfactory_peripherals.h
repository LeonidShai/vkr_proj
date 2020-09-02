#include "PeriherialFactory.h"
#include "STM32PowerButton.h"

class MyProjectPeripherals : public Peripherals {
    
public:
	{% for PERIP in PERIPS %}
	I{{PERIP}}* get{{PERIP}}(PeripheralID peripheralID) noexcept override {  // PERIP == Pin, SPI
        
        {% for PINNAME in PERIPS[PERIP] %}
		if (PeripheralID::{{PINNAME}} == peripheralID) {  // PINNAME == PowerButton
            if (mSTM32{{PINNAME}}Allocated) {
                return nullptr;
            }
            mSTM32{{PINNAME}}Allocated = true;
            return mSTM32{{PINNAME}};        
        }{% endfor %}
        
        return nullptr;
    }
    
   Status reset{{PERIP}}(I{{PERIP}}* pin) noexcept {
        if (nullptr == pin) {
            return Status::InvalidArgument;
        }
          
        {% for PINNAME in PERIPS[PERIP] %}
		if (PeripheralID::{{PINNAME}} == pin->getPeripheralID()) {
           mSTM32{{PINNAME}}Allocated = false;
           return Status::SUCCESS;
        }{% endfor %}
        
        return Status::InvalidArgument;
   }{% endfor %}
  
  IPeripheral* getPeripheral(PeripheralID peripheralID) noexcept override {
      
    {% for PERIP in PERIPS %}
	{% for PINNAME in PERIPS[PERIP] %}
	if (PeripheralID::{{PINNAME}} == peripheralID) {
        return get{{PERIP}}(peripheralID);
    }{% endfor %}{% endfor %}
  
    return nullptr;
  }
  
  Status resetPeriherial(IPeripheral* peripheral) noexcept override {
      
    if (nullptr == peripheral) {
        return Status::InvalidArgument;
    }
    
	{% for PERIP in PERIPS %}	
    {% for PINNAME in PERIPS[PERIP] %}
	if (PeripheralID::{{PINNAME}} == peripheral->getPeripheralID()) {
        return reset{{PERIP}}(static_cast<I{{PERIP}}*>(peripheral));
    }{% endfor %}{% endfor %}
    
    return Status::InvalidArgument; 
  }
  
  MyProjectPeripheralFactory& getInstance() noexcept {
    static MyProjectPeripheralFactory factory;
    if (mInstance == nullptr) {
        mInstance = &factory;
    }
    return factory;
  }
  
  Status init() noexcept {
    
	if (isInit()) {
	return Status::INIT_ALREADY;}
       
	{% for PERIP in PERIPS %}
	{% for PINNAME in PERIPS[PERIP] %}    
	static STM32{{PINNAME}} _STM32{{PINNAME}};
	mSTM32{{PINNAME}}Allocated = false;
	mSTM32{{PINNAME}} = &_STM32{{PINNAME}};
   
   
	mInstance = this;
	return Status::SUCCESS;
  
  {% endfor %}{% endfor %}
  }
  
private:
	{% for PERIP in PERIPS %}
	{% for PINNAME in PERIPS[PERIP] %}
    STM32{{PINNAME}}* mSTM32{{PINNAME}};
    bool mSTM32{{PINNAME}}Allocated;
	{% endfor %}{% endfor %}
  
};


// {"PERIPS": {"PIN": [pb1, pb2, pb3], "SPI": [ble, mem, miso, mosi, scl], "I2C": [sda, scl]}} --- get Pin, reset Pin, get SPI, reset SPI
