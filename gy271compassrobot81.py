# 1.11.23 Modified Offsets to revalibrate compass for use with GPS-RTK functions
# 12.5.22 adding a drdy=0 count error trigger.  If count>50, raise an error flag and returning it to calling program.
# 11.11.22 commented out recursiveStopMotors because __init__ of CytronclassXX was running twice causing an error
# 11.11.22 Adding additional error handling code (soft_reset)
# 11.10.22 Added recursiveStopMotors to drdy exception handling.
# 11.8.22 Modified Try Except to catch Compass errors and force Motor Stops
# 9.16.22 updated offset values to account for new GPS mast on tread robotcompass
# 9.16.22 commented out declination addition to heading calculation
# 8.1.22 Cleaning up get_bearing() with .self and exception handling
# 7.29.22 Added try/exception to get_bearing
# 7.28.22 Modified X and Y offsets for Predator/Treaded robot calibration
# 7.25.22 Starting iteration of compass class with Cytron Motor Controller
# 4.4.22 Completed initial calibration.  Commenting out most prints.
# 4.1.22 DRDY Flag working, changed to an average of 25 measurements
# 3.31.22 Output data rate line 38 changed to 200Hz
# 3.31.22 magnetic field sensitivity line 38 changed to 8G

import smbus #was originally smbus2
# import Cytronclass52
from time import sleep
import math

# cytron=Cytronclass52.Cytronclass()

C_REG_A = 0x09 # Address of Configuration register A
C_REG_B = 0x0a # Address of configuration register B
DRDY_REG = 0x06 # Address of register containing Data Ready bit 0
SR_period_REG = 0x0b # Address of SER/RESET register

MODE_STBY = 0x00 # standby mode
MODE_CONT = 0x01 # continous mode

ODR_10Hz = 0x00 # output data rate 10Hz
ODR_50Hz = 0x01 # output data rate 50Hz
ODR_100Hz = 0x10 # output data rate 100Hz
ODR_200Hz = 0x11 # output data rate 200Hz

SENS_2G = 0x00 # magnetic field sensitivity 2G
SENS_8G = 0x01 # magnetic field sensitivity 8G

OSR_512 = 0x00 # oversampling rate 512
OSR_256 = 0x01 # oversampling rate 256
OSR_128 = 0x10 # oversampling rate 128
OSR_64 = 0x11 # oversampling rate 64

X_axis_H = 0x00 # Address of X-axis LSB data register
Z_axis_H = 0x04 # Address of Z-axis LSB data register
Y_axis_H = 0x02 # Address of Y-axis LSB data register
TEMP_REG = 0x07 # Address of Temperature LSB data register

# declination angle of location where measurement going to be done
CURR_DECL = -.225147 # updated 4.1.22 -12.9 degrees is -.225147
pi = 3.14159265359 # define pi value

class compass():
    def __init__(self, address=0x0d, mode=MODE_CONT, odr=ODR_200Hz, sens=SENS_8G, osr=OSR_512, d=CURR_DECL):
        # print ("__init__ starts here.....")
        self.bus = smbus.SMBus(1)
        self.device_address = address # magnetometer device i2c address
        self._declination = d
        self.magnetometer_init(mode, odr, sens, osr)
        # print ("__init__ ends here....")
        # sleep(1) 12.3.22 commented this sleep out while debugging cytron.spingo.py, I must have put this here while debugging the compass abends....

    def soft_reset(self):
        self.bus.write_byte_data(self.device_address, C_REG_B, 0x80)
        print ("Soft Reset!")
        # print ("soft reset was called here...")

    def __set_mode(self, mode, odr, sens, osr):
        value = mode | odr  | sens | osr
        # print ("set mode was called here....")
        return value

    def magnetometer_init(self, mode, odr, sens, osr):
        # self.soft_reset()
        # 11.13.22 Noticed repeated magnetometer_init errors due to soft_reset after a previous compass fail...commented out this soft_reset

        self._mode = self.__set_mode(mode, odr, sens, osr)

        # Write to Configuration Register B: normal 0x00, soft_reset: 0x80
        self.bus.write_byte_data(self.device_address, C_REG_B, 0x00)

        # SET/RESET period set to 0x01 (recommendation from datasheet)
        self.bus.write_byte_data(self.device_address, SR_period_REG, 0xff)
        # Period set to 0xff seems to be much more stable

        # write to Configuration Register A: mode
        self.bus.write_byte_data(self.device_address, C_REG_A, self._mode)

        # print ("magnetomere__init was called here....")

    def __read_raw_data(self, reg_address):
        # Read raw 16-bit value
        low_byte = self.bus.read_byte_data(self.device_address, reg_address)
        high_byte = self.bus.read_byte_data(self.device_address, reg_address + 1)

        # concatenate high_byte and low_byte into two_byte data
        value = (high_byte << 8) | low_byte

        if value > 32767:
            value = value - 65536

        return value

    def __read_raw_data_one_reg(self, reg_address):
        # 4.1.22 added this function to read Data Ready register 0x06
        # Read raw 8-bit value
        value = self.bus.read_byte_data(self.device_address, reg_address)
        return value



    def get_bearing(self):
        try:
            # Check Data Ready bit, Reg 0x06 bit 0
            self.drdy_flag=0
            self.drdy_not_ready_count=0
            self.compass_error_retry_count=0
            self.compass_exception_but_compass_recovered=0
            self.drdy_polling_error_flag=0
            while self.drdy_flag==0 and self.drdy_polling_error_flag==0:
# 11.8.22 This try except continue code added due to repeated drdy_flag exceptions
                try:
                    self.drdy = self.__read_raw_data_one_reg(DRDY_REG)
                    self.drdy_flag = self.drdy & 1
                    self.drdy_not_ready_count=self.drdy_not_ready_count+1 # keep track of how many drdy=0 inbetween drdy=1
                    # print("Data Ready Flag: ",self.drdy_flag)
                    sleep(.01) # 11.9.22 Reduces number of drdy=0 reads from 220 to 10 inbetween drdy=1 reads.
# 12.5.22 Adding error check if drdy=o count equals 50
                    if self.drdy_not_ready_count==50:
                        print("Error: Compass drdy polling has exceeded count threshold.")
                        print("Setting flag to break out of drdy polling while loop")
                        self.drdy_polling_error_flag=1


                except KeyboardInterrupt:
                    print("KeyboardInterrupt detected during compass drdy polling.")
                    print("While running: gy271compassrobotXX.py")
                    # cytron.recursiveStopMotors()
                    print("about to execute QUIT")
                    quit()
                except:
                    self.compass_error_retry_count=self.compass_error_retry_count+1
                    print("Compass drdy error!!  Retry number:",self.compass_error_retry_count)
                    print("as of 4.2.23 no longer forcing DRDY error quit() with new Watchdog restart")
                    # quit()

                    # print("Attempting a Soft Reset now...")
                    # self.soft_reset()

                    # print("DRDY exception Stopping Motors! ")
                    # cytron.recursiveStopMotors()
                    self.compass_exception_but_compass_recovered=1
                    if self.compass_error_retry_count<5:
                        continue
                    else:
                        print("Compass Error likely detected reading drdy_flag!")
                        print("While running: gy271compassrobotXX.py")
                        # cytron.recursiveStopMotors()
                        print("as of 4.2.23 no longer forcing DRDY error quit() with new Watchdog restart")
                        # quit()

            self.drdy_flag = 0
            # End of data ready flag check

            # 1.11.23 New offsets for tread robot while fune tuning GPS motion code
            self.x_offset=-495  # original with new GPS mast: -380 pre new GPS mast: -400 old mantis offset 0
            self.y_offset=-835  # original with new GPS mast: -1123 pre new GPS mast: -23 old mantis offset 507

            # Read Accelerometer raw value
            self.x = self.__read_raw_data(X_axis_H) + self.x_offset
            self.y = self.__read_raw_data(Y_axis_H) + self.y_offset
            self.z = self.__read_raw_data(Z_axis_H)

            # 9.16.22 commented out addition of declination
            self.heading = math.atan2(self.y, self.x) # + self._declination
            self.temp_atan=math.atan2(self.y,self.x)

            if(self.heading > 2.0 * pi):
                self.heading = self.heading - 2.0 * pi

            # check for sign
            if(self.heading < 0.0):
                self.heading = self.heading + 2.0 * pi
            # convert into angle
            self.heading_angle = int(self.heading * 180.0 / pi)
            # print("get_bearing returned angle:",self.heading_angle)
            # print("Number of drdy=0 reads",self.drdy_not_ready_count)
            if self.compass_exception_but_compass_recovered==1:
                print("drdy exception forced Stop Motors but compass recovered....")
            return self.heading_angle, self.x, self.y, self.drdy_polling_error_flag

        except OSError:
            print("Compass Error likely detected during main heading_angle calculation!")
            print("While running: gy271compassrobotXX.py")
            print("Returning to calling program.")
            # cytron.recursiveStopMotors()
            # print("about to execute QUIT")
            # quit()

        except:
           print("Non-OSError Exception detected during main heading_angle calculation!")
           print("While running: gy271compassrobotXX.py")
           print("Returning to calling program.")
           # print("Recursive Motor Stop:")
           # cytron.recursiveStopMotors()
           # print("about to execute QUIT")
           # quit()




    def read_temp(self):
        low_byte = self.bus.read_byte_data(self.device_address, TEMP_REG)
        high_byte = self.bus.read_byte_data(self.device_address, TEMP_REG + 1)

        # concatenate higher and lower value
        value = (high_byte << 8) | low_byte # signed int (-32766 : 32767)
        value = value & 0x3fff # to get only positive numbers (first bit, sign bit)
        value = value / 520.0 # around: 125 (temp range) times 100 LSB/*C ~ 520
        return value

    def set_declination(self, value):
        self._declination = value
