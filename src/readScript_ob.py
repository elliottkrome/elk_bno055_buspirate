#!Users/elliottkrome/anaconda/bin/python
import logging
import os
# import matplotlib
from BNO055 import *
import pickle

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    bno055 = BNO055("/dev/tty.usbserial-AH03F33K", 115200, timeout=0.1)
    bno055.setup(verbose=False)     # Handles various setup tasks
    #                                   1) enters Bitbang mode
    #                                   2) enters I2C mode
    #                                   3) sets power and pull-ups
    #                                   4) sets I2C speed
    #                                 verbose is false
    #                                   (don't need affirmative messages)
    #
    bno055.begin()                  # Handles initialization tasks
    #                                   1) power mode normal
    #                                   2) use internal oscillator
    #                                   3) leaves chip in NDOF mode
    #
    status, self_test, error = bno055.get_system_status()
    print "status:    ", status
    print "self_test: ", self_test
    print "error:     ", error
    #
    ###########################################################################
    sample = 0                              # unnecessary, just for counting
    quaternion_scaling_factor = (1.0 / (1 << 14))  # see bottom of pg. 35
    # setup get data loop
    bno055.enter_fused_data_mode()          # Let the BNO055 do its nice thing
    #                                       # __set address to read from__
    bno055.write_bytes([PAGE_0.             # 1 of 2 BNO055 register pages
                        EULER_H_LSB_ADDR])  # register to read
    # bno055.write_bytes([PAGE_0.             # ||
    #                     QUATERNION_DATA_W_LSB_ADDR])
    #
    # loop to continuously get data
    last = time.time()
    while True:
        sample += 1
        ########
        heading, roll, pitch = [x / 16 for x in bno055.read_vector()]
        print "heading: {0:5}   roll: {1:5}   yaw: {2:5}".\
            format(heading, roll, pitch)
        ########
        # w, x, y, z = bno055.read_vector(count=4)
        # w *= quaternion_scaling_factor
        # x *= quaternion_scaling_factor
        # y *= quaternion_scaling_factor
        # z *= quaternion_scaling_factor
        # print "w = {0}  x = {1}  y = {2} z = {3}".\
        #     format(w, x, y, z)
        ########
        if sample % 100 is 0:
            print "\n         sampling frequency:", 100 / (time.time() - last),\
                "Hz\n"
            last = time.time()
            sys, gyro, accel, mag = bno055.get_cal_status(verbose=True)
            #                                         read calibration status
            #                                           0 is uncalibrated
            #                                           3 is fully calibrated
            calibration_data = bno055.get_calibration_info(verbose=True)
            with open('calib_data.txt', 'wb') as cal_data_file:
                pickle.dump(calibration_data, cal_data_file)
            ########
            bno055.enter_fused_data_mode()
            bno055.write_bytes([PAGE_0.EULER_H_LSB_ADDR])
            # bno055.write_bytes([PAGE_0.QUATERNION_DATA_W_LSB_ADDR])
    bno055.resetToTerm()
