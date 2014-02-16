//*****************************************************************************
//
// qs-rgb.c - Quickstart for the EK-TM4C123GXL.
//
// Copyright (c) 2012-2013 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.0.1.11577 of the EK-TM4C123GXL Firmware Package.
//
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "inc/hw_hibernate.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/hibernate.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/systick.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"
#include "utils/cmdline.h"
#include "drivers/rgb.h"
#include "drivers/buttons.h"
#include "uart_commands.h"
#include "natcar-prototype.h"

#include "driverlib/pwm.h"

//*****************************************************************************
//
//! \addtogroup example_list
//! <h1>EK-TM4C123GXL Quickstart Application (qs-rgb)</h1>
//!
//! A demonstration of the Tiva C Series LaunchPad (EK-TM4C123GXL)
//! capabilities.
//!
//! Press and/or hold the left button to traverse towards the red end of the
//! ROYGBIV color spectrum.  Press and/or hold the right button to traverse
//! toward the violet end of the ROYGBIV color spectrum.
//!
//! If no input is received for 5 seconds, the application will start
//! automatically changing the color displayed.
//!
//! Press and hold both left and right buttons for 3 seconds to enter
//! hibernation.  During hibernation, the last color displayed will blink
//! for 0.5 seconds every 3 seconds.
//!
//! The system can also be controlled via a command line provided via the UART.
//! Configure your host terminal emulator for 115200, 8-N-1 to access this
//! feature.
//!
//! - Command 'help' generates a list of commands and helpful information.
//! - Command 'hib' will place the device into hibernation mode.
//! - Command 'rand' will initiate the pseudo-random color sequence.
//! - Command 'intensity' followed by a number between 0 and 100 will set the
//! brightness of the LED as a percentage of maximum brightness.
//! - Command 'rgb' followed by a six character hex value will set the color.
//! For example 'rgb FF0000' will produce a red color.
//
//*****************************************************************************

//*****************************************************************************
//
// Entry counter to track how int32_t to stay in certain staging states before
// making transition into hibernate.
//
//*****************************************************************************
static volatile uint32_t ui32HibModeEntryCount;

//*****************************************************************************
//
// Input buffer for the command line interpreter.
//
//*****************************************************************************
static char g_cInput[APP_INPUT_BUF_SIZE];

//*****************************************************************************
//
// Application state structure.  Gets stored to hibernate memory for
// preservation across hibernate events.
//
//*****************************************************************************
volatile tAppState g_sAppState;

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif


//*****************************************************************************
//
// Configure the UART and its pins.  This must be called before UARTprintf().
//
//*****************************************************************************
void
ConfigureUART(void)
{
    //
    // Enable the GPIO Peripheral used by the UART.
    //
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

    //
    // Enable UART0
    //
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    //
    // Configure GPIO Pins for UART mode.
    //
    ROM_GPIOPinConfigure(GPIO_PA0_U0RX);
    ROM_GPIOPinConfigure(GPIO_PA1_U0TX);
    ROM_GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    //
    // Use the internal 16MHz oscillator as the UART clock source.
    //
    UARTClockSourceSet(UART0_BASE, UART_CLOCK_PIOSC);

    //
    // Initialize the UART for console I/O.
    //
    UARTStdioConfig(0, 115200, 16000000);
}

unsigned long ulPeriod;

void SetPWMAngle(int angle){
	volatile double periodDivider;
	double pulseWidth;
	angle = (angle * -1) + 100;
	periodDivider = 0.1 * angle + 41; //(61 - 41) / 200
	pulseWidth = (double) ulPeriod / periodDivider;
	UARTprintf("%f", pulseWidth);
	//Set PWM duty cycle - ulPeriod/61 to ulPeriod/41
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0, pulseWidth);

}
void SetPWMSpeed(int speed){
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,ulPeriod/2);
}

void ConfigurePWM(){

	//Configure PWM Clock to match system
	SysCtlPWMClockSet(SYSCTL_PWMDIV_8);

	// Enable the peripherals used by this program.
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
	SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
	ulPeriod = SysCtlClockGet() / 110; //PWM frequency 50HZ

	//Configure PD0 and PD1 Pins as PWM
	GPIOPinConfigure(GPIO_PD0_M1PWM0);
	GPIOPinConfigure(GPIO_PD1_M1PWM1);
	GPIOPinTypePWM(GPIO_PORTD_BASE, GPIO_PIN_0 | GPIO_PIN_1);

	//Configure PWM Options
	//PWM_GEN_0 Covers M1PWM0 and M1PWM1 See p.153 in the ROM User's Guide
	PWMGenConfigure(PWM1_BASE, PWM_GEN_0, PWM_GEN_MODE_UP_DOWN | PWM_GEN_MODE_NO_SYNC);

	//Set the Period (expressed in clock ticks)
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_0, ulPeriod);

	SetPWMAngle(0);
	SetPWMSpeed(0);

	// Enable the PWM generator
	PWMGenEnable(PWM1_BASE, PWM_GEN_0);

	// Turn on the Output pins
	PWMOutputState(PWM1_BASE, PWM_OUT_0_BIT | PWM_OUT_1_BIT, true);
}

//*****************************************************************************
//
// Main function performs init and manages system.
//
// Called automatically after the system and compiler pre-init sequences.
// Performs system init calls, restores state from hibernate if needed and
// then manages the application context duties of the system.
//
//*****************************************************************************
int main(void){
    int32_t i32CommandStatus;

    //
    // Enable stacking for interrupt handlers.  This allows floating-point
    // instructions to be used within interrupt handlers, but at the expense of
    // extra stack usage.
    //
    ROM_FPUEnable();
    ROM_FPUStackingEnable();

    //
    // Set the system clock to run at 40Mhz off PLL with external crystal as
    // reference.
    //
    ROM_SysCtlClockSet(SYSCTL_SYSDIV_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);

    ConfigurePWM();

    //
    // Enable and Initialize the UART.
    //
    ConfigureUART();

    UARTprintf("Welcome to the Tiva C Series TM4C123G LaunchPad!\n");
    UARTprintf("Type 'help' for a list of commands\n");
    UARTprintf("> ");


    //
    // spin forever and wait for carriage returns or state changes.
    //
    while(1)
    {

        UARTprintf("\n>");


        //
        // Peek to see if a full command is ready for processing
        //
        while(UARTPeek('\r') == -1)
        {
            //
            // millisecond delay.  A SysCtlSleep() here would also be OK.
            //
            SysCtlDelay(SysCtlClockGet() / (1000 / 3));
        }

        //
        // a '\r' was detected get the line of text from the user.
        //
        UARTgets(g_cInput,sizeof(g_cInput));

        //
        // Pass the line from the user to the command processor.
        // It will be parsed and valid commands executed.
        //
        i32CommandStatus = CmdLineProcess(g_cInput);

        //
        // Handle the case of bad command.
        //
        if(i32CommandStatus == CMDLINE_BAD_CMD)
        {
            UARTprintf("Bad command!\n");
        }

        //
        // Handle the case of too many arguments.
        //
        else if(i32CommandStatus == CMDLINE_TOO_MANY_ARGS)
        {
            UARTprintf("Too many arguments for command processor!\n");
        }
    }
}
