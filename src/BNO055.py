# much taken from:
# https://github.com/adafruit/Adafruit_Python_BNO055/blob/master/Adafruit_BNO055/BNO055.py#L360

import sys
from bno055_registers import Page_0
from pyBusPirate.BinaryMode.I2C import *
import time
import numpy as np

from pyquaternion import Quaternion

from matplotlib import pyplot as plt
from matplotlib import animation as ani
from mpl_toolkits.mplot3d import Axes3D

import os

empty_cal_list = [0] * 22

# BNO sensor axes remap values.
#  These are the parameters to the BNO.set_axis_remap function.
#  Don't change these without consulting section 3.4 of the datasheet.
#  The default axes mapping below assumes the Adafruit BNO055 breakout
#  is flat on a table with
#    the row of SDA, SCL, GND, VIN, etc pins facing away from you.
BNO_AXIS_REMAP = {'x': AXIS_REMAP_X,
                  'y': AXIS_REMAP_Z,
                  'z': AXIS_REMAP_Y,
                  'x_sign': AXIS_REMAP_POSITIVE,
                  'y_sign': AXIS_REMAP_POSITIVE,
                  'z_sign': AXIS_REMAP_NEGATIVE}


class BNO055(I2C):
    I2C_READ_ADDRESS = 0x51   # in list form for sake of bulk_trans()
    I2C_WRITE_ADDRESS = 0x50  # in list form for sake of bulk_trans()
    max_array_size = 200

    def __init__(self, port='/dev/tty.usbserial-AH03F33K',
                 speed=115200, timeout=0.1):
        super(BNO055, self).__init__(port, speed)

    def setup(self, verbose=False):
        if self.BBmode(verbose=verbose):   # def of BBmode() is in BitBang.py
            if verbose is True:
                print "  bitbang mode OK"
        else:
            print "**> failed at bitbang mode"
            sys.exit()
        if self.enter_I2C():  # def of enter_I2C() is in BitBang.py
            if verbose is True:
                print "  raw I2C mode OK."
        else:
            print "**> failed to enter I2C mode"
            sys.exit()
        # def of cfg_pins() and set_speed() in BitBang.py
        if not self.cfg_pins(I2CPins.POWER | I2CPins.PULLUPS):
            # (I2CPins.POWER | I2CPins.PULLUPS) = (0x08 | 0x04) = d'12
            print "**> failed to set I2C peripherals."
            sys.exit()
        if not self.set_speed(I2CSpeed._5KHZ):
            print "**> failed to set I2C Speed."
            sys.exit()
        if verbose is True:
            print "  i2c power and pullups on\n  i2c speed set."
        self.timeout(0.1)  # NECESSARY

    def begin(self):
        self.enter_configuration_mode()          # ensure we are in config mode
        self.write_bytes([Page_0.PAGE_ID_ADDR])  # ensure we are on page 1
        # TODO: adafruit library does a reset here. Is this necessary?
        # use normal power mode
        self.write_bytes([Page_0.PWR_MODE_ADDR, POWER_MODE_NORMAL])
        # use internal clock
        self.write_bytes([Page_0.SYS_TRIGGER_ADDR, 0x00])
        self.set_mode(NDOF)

    def read_bytes(self, numbytes=1, doFormat=False, ret=True):
        data_out = []          # list to hold data if return is true
        byteNum = 0            # variable for pretty formatting, non-essential
        #
        self.send_start_bit()  # take control of the bus
        #                        bulk_trans() is defined in BitBang.py
        self.bulk_trans(1, [self.I2C_READ_ADDRESS])  # address BNO055
        while numbytes > 0:
            if(ret is False):
                byte = self.read_byte()
                if doFormat is True:
                    print "  byteNum {0:4} hex: {1:4}".\
                        format(byteNum, byteToHex(byte))
                else:
                    print byte
            else:
                data_out.append(ord(self.read_byte()))
            if numbytes > 1:   # only send acks up until the last byte
                self.send_ack()
            numbytes -= 1      # decrement for flow control (while statement)
            byteNum += 1       # increment for pretty formatting, non-essential
        self.send_stop_bit()   # over and out
        if ret is True:
            return data_out

    def write_bytes(self, data):
        data.insert(0, self.I2C_WRITE_ADDRESS)   # take care of I2C addressing
        self.send_start_bit()
        self.bulk_trans(len(data), data)  # bulk_trans() defined in BitBang.py
        self.send_stop_bit()

    def read_vector(self, count=3):
        """returns tuple of two byte data starting at BNO055 register address
           MUST setup BNO055 reg addr previously (presumably w/ write_bytes)
             adapted from adafruit lib"""
        data = self.read_bytes(count * 2)
        result = [0]*count
        for i in range(count):
            result[i] = ((data[(i * 2) + 1] << 8) | data[i * 2]) & 0xFFFF
            #             MSB                       LSB
            #                              * 256
            if result[i] > 32767:   # deal with two's-complement signage issues
                result[i] -= 65536  # ||
        return result

    def get_calibration_info(self, verbose=False):
        """Return the sensor's calibration data and return it as an array of
        22 bytes. Can be saved and then reloaded with set_calibration
        to quickly calibrate from a previously calculated set of data.
        """
        # Switch to configuration mode, (see section 3.10.4 of datasheet)
        self.enter_configuration_mode()
        # Read the 22 bytes of calibration data and convert it to a list (from
        #   a bytearray) so it's more easily serialized should the caller
        #   want to store it.
        self.write_bytes([Page_0.ACCEL_OFFSET_X_LSB_ADDR])
        cal_data = list(self.read_bytes(22))
        #
        #######################################################################
        result = [0] * 11          # only necessary for verbose formatting  # #
        i = 0                                                               # #
        while i < 11:                                                       # #
            result[i] = cal_data[(2 * i) + 0] + cal_data[(2 * i) + 1] << 8  # #
            if result[i] > 32767:  # deal with two's-complement             # #
                if i < 9:               # ||                                # #
                    result[i] -= 65536  # ||                                # #
            i += 1                                                          # #
        if verbose is True:                                                 # #
            print "    -       accelerometer offset:", result[0:3]          # #
            print "    -        magnetometer offset:", result[3:6]          # #
            print "    -           gyroscope offset:", result[6:9]          # #
            print "    -       accelerometer radius:", result[9]            # #
            print "    -        magnetometer radius:", result[10]           # #
            print "\n    -"                                                 # #
        #######################################################################
        #
        # Go back to normal operation mode.
        self.set_mode(IMUPLUS)
        return cal_data

    def set_calibration(self, data):
        """Set the sensor's calibration data using a list of 22 bytes that
        represent the sensor offsets and calibration data.  This data should be
        a value that was previously retrieved with get_calibration (and then
        perhaps persisted to disk or other location until needed again).
        """
        # Check that 22 bytes were passed in with calibration data.
        if data is None or len(data) != 22:
            print "**> calibration data length error"
            raise ValueError('Expected a list of 22 bytes for cal data.')
        self.enter_configuration_mode()
        data.insert(0, Page_0.ACCEL_OFFSET_X_LSB_ADDR)
        # Set the 22 bytes of calibration data.
        self.write_bytes(data)
        time.sleep(1.2)
        # Go back to normal operation mode.
        self.set_mode(IMUPLUS)

    def get_cal_status(self, verbose=False):
        """
        Read the calibration status of the sensors and return a 4 tuple with
        calibration status as follows:
          - System,        3=fully calibrated, 0=not calibrated
          - Gyroscope,     3=fully calibrated, 0=not calibrated
          - Accelerometer, 3=fully calibrated, 0=not calibrated
          - Magnetometer,  3=fully calibrated, 0=not calibrated
        |-----+--------+------------------|
        | bit | access | content          |
        |-----+--------+------------------|
        |   7 |  r     | SYS Calib Status | 3 -> fully calibrated
        |-----+--------+------------------| 0 -> not calibrated
        |   6 |  r     | SYS Calib Status |       ||
        |-----+--------+------------------|       ||
        |   5 |  r     | GYR Calib Status |       ||
        |-----+--------+------------------|       ||
        |   4 |  r     | GYR Calib Status |       ||
        |-----+--------+------------------|       ||
        |   3 |  r     | ACC Calib Status |       ||
        |-----+--------+------------------|       ||
        |   2 |  r     | ACC Calib Status |       ||
        |-----+--------+------------------|       ||
        |   1 |  r     | MAG Calib Status |       ||
        |-----+--------+------------------|       ||
        |   0 |  r     | MAG Calib Status |       ||
        |-----+--------+------------------|        """
        # Return the calibration status register value.
        self.write_bytes([Page_0.               # 1 of 2 BNO055 register pages
                          CALIB_STAT_ADDR])     # register to read
        cal_stts = self.read_bytes()            # do read register
        cal_stts_lst = [0] * 4                  # declare list of 0s
        cal_stts_lst[0] = (cal_stts[0] >> 6) & 0x03  # SYS see docstring tablec
        cal_stts_lst[1] = (cal_stts[0] >> 4) & 0x03  # GYR ||
        cal_stts_lst[2] = (cal_stts[0] >> 2) & 0x03  # ACC ||
        cal_stts_lst[3] = cal_stts[0] & 0x03         # MAG ||
        if verbose is True:
            print "    -         system calibration:", cal_stts_lst[0]
            print "    -      gyroscope calibration:", cal_stts_lst[1]
            print "    -  accelerometer calibration:", cal_stts_lst[2]
            print "    -   magnetometer calibration:", cal_stts_lst[3]
            print "    -"
            return cal_stts_lst          # return tuple of 4 values

    def get_system_status(self, run_self_test=True):
        """Return a tuple with status information.  Three values will be returned:
          - System status register value with the following meaning:
              0 = Idle
              1 = System Error
              2 = Initializing Peripherals
              3 = System Initialization
              4 = Executing Self-Test
              5 = Sensor fusion algorithm running
              6 = System running without fusion algorithms
          - Self test result register value with the following meaning:
              Bit value: 1 = test passed, 0 = test failed
              Bit 0 = Accelerometer self test
              Bit 1 = Magnetometer self test
              Bit 2 = Gyroscope self test
              Bit 3 = MCU self test
              Value of 0x0F = all good!
          - System error register value with the following meaning:
              0 = No error
              1 = Peripheral initialization error
              2 = System initialization error
              3 = Self test result failed
              4 = Register map value out of range
              5 = Register map address out of range
              6 = Register map write error
              7 = BNO low power mode not available for selected operation mode
              8 = Accelerometer power mode not available
              9 = Fusion algorithm configuration error
             10 = Sensor configuration error
        If run_self_test is passed in as False then no self test is performed
          and None will be returned for the self test result.
        Note that running a
          self test requires going into config mode which will stop the fusion
          engine from running.
        """
        self_test = None
        if run_self_test:
            # Switch to configuration mode if running self test.
            self.enter_configuration_mode()
            # Perform a self test.
            self.write_bytes([Page_0.             # 1 of 2 BNO055 reg pages
                              SYS_TRIGGER_ADDR])  # register to read
            sys_trigger = self.read_bytes()[0]       # do read register
            self.write_bytes([Page_0.              # 1 of 2 BNO055 reg pages
                             SYS_TRIGGER_ADDR,     # register to write
                             sys_trigger | 0x1])  # turn bit 0 high
            # Wait for self test to finish.
            time.sleep(1.0)
            # Read test result.
            self.write_bytes([Page_0.
                              SELFTEST_RESULT_ADDR])
            self_test = self.read_bytes()
            # Go back to operation mode.
            self.set_mode(IMUPLUS)
        # Now read status and error registers.
        self.write_bytes([Page_0.
                          SYS_STAT_ADDR])
        status = self.read_bytes()
        self.write_bytes([Page_0.
                         SYS_ERR_ADDR])
        error = self.read_bytes()
        # Return the results as a tuple of all 3 values.
        return (status, self_test, error)

    def set_axis_remap(self, x, y, z,
                       x_sign=AXIS_REMAP_POSITIVE, y_sign=AXIS_REMAP_POSITIVE,
                       z_sign=AXIS_REMAP_POSITIVE):
        """Set axis remap for each axis.  The x, y, z parameter values should
        be set to one of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z and will
        change the BNO's axis to represent another axis.  Note that two axises
        cannot be mapped to the same axis, so the x, y, z params should be a
        unique combination of AXIS_REMAP_X, AXIS_REMAP_Y, AXIS_REMAP_Z values.

        The x_sign, y_sign, z_sign values represent if the axis should be
        positive or negative (inverted).
        See the get_axis_remap documentation for information on the orientation
        of the axes on the chip, and consult section 3.4 of the datasheet.

        Note that by default the axis orientation of the BNO chip looks like
        the following (taken from section 3.4, page 24 of the datasheet).
        The dot in the corner corresponds to the dot on the BNO chip:

                           | Z axis
                           |
                           |   / X axis
                       ____|__/____
          Y axis     / *   | /    /|
          _________ /______|/    //
                   /___________ //
                  |____________|/
        """
        # Switch to configuration mode.
        self.enter_configuration_mode()
        # Set the axis remap register value.
        map_config = 0x00
        map_config |= (z & 0x03) << 4
        map_config |= (y & 0x03) << 2
        map_config |= x & 0x03
        self.write_bytes([Page_0.AXIS_MAP_CONFIG_ADDR, map_config & 0xFF])
        # Set the axis remap sign register value.
        sign_config = 0x00
        sign_config |= (x_sign & 0x01) << 2
        sign_config |= (y_sign & 0x01) << 1
        sign_config |= z_sign & 0x01
        self.write_bytes([Page_0.AXIS_MAP_SIGN_ADDR, sign_config & 0xFF])
        # Go back to normal operation
        self.set_mode(IMUPLUS)

    def print_settings(self):
        print "Settings Dictionary:"
        settingsD = self.port.get_settings()
        for setting in settingsD:
            print "  {0:20}: {1}".format(setting, settingsD[setting])

    def set_mode(self, mode):
        self.write_bytes([Page_0.OPR_MODE_ADDR, mode & 0xFF])
        time.sleep(0.2)

    def enter_configuration_mode(self):
        self.set_mode(CONFIG)

    def enter_fused_data_mode(self):
        self.set_mode(IMUPLUS)

    def resetToTerm(self, verbose=True):
        if verbose is True:
            print "Reset Bus Pirate to user terminal: "
        if self.resetBP():
            if verbose is True:
                print "OK"
            else:
                print "**> failed to reset bus pirate to user term"
                sys.exit()

    ################################################################
    # # # # # # # # BEGIN ANIMATION SECTION # # # # # # # # # # # #
    ################################################################
    def get_quat_for_anim(self):
        quat_scale_f = (1.0 / (1 << 14))         # see manual, bottom of pg. 35
        t, x, y, z = [i * quat_scale_f for i in self.read_vector(count=4)]
        if 1:
            if x > 0.5:
                os.system('say "Back"')
            if x < -0.5:
                os.system('say "For"')
            if y > 0.5:
                os.system('say "Right"')
            if y < -0.5:
                os.system('say "Left"')
            if z > 0.5:
                os.system('say "Twist"')
            if z < -0.5:
                os.system('say "Twist"')
        q = Quaternion(scalar=t, vector=[x, y, z])
        print "    t = {0:.7f}  x = {1:.7f}  y = {2:.7f} z = {3:.7f}".\
            format(t, x, y, z)
        return q

    def ani_init(self):
        for line in self.lines:
            line.set_data([], [])
            line.set_3d_properties([])
        return self.lines

    def setup_anim(self):
        self.fig = plt.figure()
        self.last = time.time()
        self.interrupt_after_n_samps = 50
        self.sample_count = 0
        self
        ax = Axes3D(self.fig)  # changed from demo in git
        #                      Previous line was:
        #                      ax = fig.add_axes([0, 0, 1, 1], projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #
        # use a different color for each axis
        colors = ['r', 'g', 'b']
        #
        # set up lines and points
        self.lines = sum([ax.plot([], [], [], c=c)
                          for c in colors], [])
        self.startpoints = np.array([[0, 0, 0],
                                     [0, 0, 0],
                                     [0, 0, 0]])
        self.endpoints = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])
        #
        # prepare the axes limits
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)

    # animation function
    def animate(self, args):
        conflag = 0
        try:
            q = self.get_quat_for_anim()
            for line, start, end in zip(self.lines,
                                        self.startpoints,
                                        self.endpoints):
                start = q.rotate(start)
                end = q.rotate(end)
                #
                line.set_data([start[0], end[0]], [start[1], end[1]])
                line.set_3d_properties([start[2], end[2]])
            self.fig.canvas.draw()
            self.sample_count += 1
            if self.sample_count % 50 is 0:
                print "*---------------------------------------------------*"
                print "    -\n    -         sampling frequency:",\
                    50 / (time.time() - self.last), "Hz\n    -"
                self.last = time.time()
                #
                #  read calibration status
                sys, gyro, accel, mag = self.get_cal_status(verbose=True)
                #                             verbose to print inside function
                #                                         0 is uncalibrated
                #                                         3 is fully calibrated
                # calibration_data = bno055.get_calibration_info(verbose=True)
                # write calibration_data to file calib_data.txt
                # with open("calib_data.txt", 'wb') as calib_data_file_object:
                #    pickle.dump(calibration_data, calib_data_file_object)
                #
                self.get_calibration_info(verbose=True)
                print "*---------------------------------------------------*"
                # self.set_calibration(empty_cal_list)
                if sys is 3 and gyro is 3 and accel is 3 and conflag is 0:
                    print "PUT IN CONFIGURATION POSITION"
                    print conflag
                    time.sleep(10)
                    self.set_axis_remap(**BNO_AXIS_REMAP)
                    time.sleep(10)
                    conflag = 1
                    print conflag
                    test_config = [0]*22
                    bno055.set_calibration(test_config)
                self.enter_fused_data_mode()      # reenter imu mode
                # bno055.write_bytes([VECTOR_EULER])  # addres for next read
                self.write_bytes([VECTOR_QUATERNION])
        except KeyboardInterrupt:
            os._exit(0)

    def do_animate(self):
        #         # ani is matplotlib.animation()
        self.anim = ani.FuncAnimation(self.fig,      # fig is matplotlib.figure
                                      self.animate,  # animate does update via
                                      #                  self.line.set_3d_properties
                                      init_func=self.ani_init,  # frame setup
                                      frames=500,    # ?
                                      interval=1,    # try to update every ms
                                      blit=False,    # ?
                                      repeat=False)  # do not repeate
        plt.show()


# Some helper functions--------------------------------------------------------
def byteToHex(byteStr):
    """Convert byte string to hex string representation (ie for output).
    from
    http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/
    """
    # Uses list comprehension which is slightly faster than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()
    return ''.join(["%02X " % ord(x) for x in byteStr]).strip()


def printSettings(BNO055):
    print "Settings Dictionary:"
    settingsD = BNO055.port.get_settings()
    for setting in settingsD:
        print "  {0:20}: {1}".format(setting, settingsD[setting])


