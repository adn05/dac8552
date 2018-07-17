# DAC8552
Python module for interfacing Texas Instruments DAC8552 digital to analog converter with the 
Raspberry Pi via SPI bus.
Default pin and settings configuration is for the Open Hardware "Waveshare High-Precision AD/DA Board"

Download: https://github.com/adn05/dac8552

Depends on PiGPIO library, see: http://abyz.me.uk/rpi/pigpio/python.html

Hardware: https://www.waveshare.com/wiki/High-Precision_AD/DA_Board

Code inspired from PiPyADC: https://github.com/ul-gh/PiPyADC

License: GNU LGPLv2.1, see: https://www.gnu.org/licenses/old-licenses/lgpl-2.1-standalone.html


## Run example on Raspbian:
+ Install PiGPIO 


    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make
    make install

+ Run PiGPIO deamon


	sudo pigpiod

+ Run example


    sudo python example.py


## DAC8552
```
class ADS1256(__builtin__.object)
    Python class for interfacing the DAC8552 digital to analog converters with the Raspberry Pi.

    Default pin and settings configuration is for the Open Hardware
    "Waveshare High-Precision AD/DA Board"
    See file DAC8552_default_config.py for configuration settings and description.

    Documentation source: Texas Instruments DAC8552
    datasheet SBAS288: http://www.ti.com/lit/ds/symlink/dac8552.pdf

| Methods defined here:

    __init__(self, conf=DAC8552_default_config, pi=None):
        Constructor for the DAC object
        Hardware pin configuration must be set up at initialization phase and can not be changed later.
        Default config is read from external file (module) import
        #conf: config file imported
        #pi: PiGPIO object

    power_down(self, channel, mode):
        Toggle the selected channel to Power Down Mode
        There are the three power-down modes. The supply current falls to 700nA at 5V (400nA at 3V).
        And the output stage is also internally switched from the output of the amplifier to a
        resistor network of known values. The output is connected internally to GND through a 1kΩ
        resistor, a 100kΩ resistor, or it is left open-circuited (High-Impedance).
        #channel: DAC_A or DAC_B , to select DAC A or DAC B
        #mode: MODE_POWER_DOWN_1K , MODE_POWER_DOWN_100K or MODE_POWER_DOWN_HI
        
    write_dac(self, channel, data):
        Write a 16 bit data to th selected channel
        The input coding for each device is unipolar straight binary, so the ideal output voltage
        is given by: V_out = V_ref * data / 65536
        #channel: DAC_A or DAC_B , to select DAC A or DAC B
        #data: 0 - 65535 , decimal equivalent of the binary code that is loaded to the DAC register
        

| Data descriptors defined here:
 
    digit_per_v(self):
        Get DAC numeric output digit per volts.
        Readonly: This is a convenience value calculated from v_ref.
        
    v_ref(self):
        Get/Set DAC analog reference input voltage differential.
        This is only for calculation of output value scale factor.
```

##  Extended Description: DAC8552 Input Shift Register
The input shift register of the DAC8552 is 24 bits wide and is made up of eight control 
bits (DB16–DB23) and 16 data bits (DB0–DB15). 

       DB23                                                                    DB16        DB15               DB0
    |    0    |    0    |   LDB   |   LDA   |    X    | Buf Sel |    PD1    |    PD0    |        D15 ... D0        | 
    
Logically OR all desired option values together to form a control byte.
Data bits are transferred to the specified Data Buffer or DAC Register, depending on the command 
issued by the control byte.

+ The first two control bits (DB22 and DB23) are reserved and must be '0' for proper operation.

+ LDA (DB20) and LDB (DB21) control the updating of each analog output with the specified
    16-bit data value or power-down command. 
    
    **LDA value definitions:**
    
        UPDATE_DAC_A = 0x10
        UPDATE_DAC_B = 0x20
    
+ Bit DB19 is a don't care bit that does not affect the operation of the DAC8552.
    
+ Buffer Select (DB18), controls the destination of the data (or power-down command)
    between DAC A and DAC B. 
    
    **Buffer select definitions:**
    
        BUFFER_A = 0x00
        BUFFER_B = 0x04
    
+ PD0 (DB16) and PD1 (DB17), select the power-down mode of one or both of the DAC
    channels. The four modes are normal mode or any one of three power-down modes. 
     
    In power-down modes, the supply current falls to 700nA at 5V (400nA at 3V).
    And the output stage is also internally switched from the output of the amplifier to a
    resistor network of known values. The output is connected internally to GND through a 1kΩ
    resistor, a 100kΩ resistor, or it is left open-circuited (High-Impedance).
    
               PD1         PD0        OPERATING MODE
                0           0           Normal Operation
                0           1           Output typically 1kΩ to GND
                1           0           Output typically 100kΩ to GND
                1           1           High impedance
    
    **Modes value definitions:**
    
        MODE_NORMAL           = 0x00
        MODE_POWER_DOWN_1K    = 0x01
        MODE_POWER_DOWN_100K  = 0x02
        MODE_POWER_DOWN_HI    = 0x03 