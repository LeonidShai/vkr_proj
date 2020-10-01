#ifndef PERIHERIALS_H
#define PERIHERIALS_H

#include "periherial.h"
#include "i_pin.h"

class Peripherals {
    
public:
  virtual IPeripheral* getPeripheral(PeripheralID peripheralID) noexcept = 0;  
  virtual Status resetPeripheral(IPeripheral* peripheral) noexcept = 0;
  
  {% for PERIP in PERIPS %}
  virtual I{{PERIP}}* get{{PERIP}}(PeripheralID peripheralID) noexcept = 0;  
  virtual Status reset{{PERIP}}(I{{PERIP}}* pin) noexcept = 0;
  {% endfor %}
    
  static Peripherals& getInstance() noexcept {
      return *mInstance;
  }
  
protected:
	bool isInit() {
	   return (mInstance != nullptr);
   }
   
   static Peripherals* mInstance;
   
};

#endif // PERIHERIALS_H
