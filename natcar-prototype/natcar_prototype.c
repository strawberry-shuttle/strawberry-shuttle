#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_gpio.h"
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/pin_map.h"
#include "driverlib/gpio.h"
#include "driverlib/pwm.h"
#include "inc/tm4c123gh6pm.h"

#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "utils/cmdline.h"

int main(void){
	unsigned long ulPeriod;

	//Set the clock
	SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC | SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);

	//Configure PWM Clock to match system
	SysCtlPWMClockSet(SYSCTL_PWMDIV_16);

	// Enable the peripherals used by this program.
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
	SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
	ulPeriod = SysCtlClockGet() / 106; //PWM frequency 50HZ

	//Configure PD0 and PD1 Pins as PWM
	GPIOPinConfigure(GPIO_PD0_M1PWM0);
	GPIOPinConfigure(GPIO_PD1_M1PWM1);
	GPIOPinTypePWM(GPIO_PORTD_BASE, GPIO_PIN_0 | GPIO_PIN_1);

	//Configure PWM Options
	//PWM_GEN_0 Covers M1PWM0 and M1PWM1 See p.153 in the ROM User's Guide
	PWMGenConfigure(PWM1_BASE, PWM_GEN_0, PWM_GEN_MODE_UP_DOWN | PWM_GEN_MODE_NO_SYNC);

	//Set the Period (expressed in clock ticks)
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_0, ulPeriod);

	//Set PWM duty-50%
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,ulPeriod/125);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,ulPeriod/82);

	// Enable the PWM generator
	PWMGenEnable(PWM1_BASE, PWM_GEN_0);

	// Turn on the Output pins
	PWMOutputState(PWM1_BASE, PWM_OUT_0_BIT | PWM_OUT_1_BIT, true);

	//Do nothing
	while(1)
	{

	}

}
