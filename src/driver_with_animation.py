#!Users/elliottkrome/anaconda/bin/python
import logging
import os
import pickle
from BNO055 import *
# from BNO055_1 import *
import quaternion
import numpy as np
from pyquaternion import Quaternion


from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    visualization = True
    bno055 = BNO055("/dev/tty.usbserial-AH03F33K", 115200, timeout=0.4)

    bno055.setup(verbose=True)     # Handles various setup tasks
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
    # status, self_test, error = bno055.get_system_status()
    # print "status:    ", status
    # print "self_test: ", self_test
    # print "error:     ", error
    #
    # config_data = pickle.load(open('calib_data.pickle', 'rb'))
    # bno055.set_calibration(config_data)
    # bno055.get_cal_status(verbose=True)
    # bno055.get_calibration_info(verbose=True)
    ###########################################################################
    sample = 0                               # unnecessary, just for counting
    quat_scale_f = (1.0 / (1 << 14))         # see manual, bottom of pg. 35
    q_array = np.array([], dtype=np.quaternion)  # declare empty array
    max_array_size = 200                     # never need more than this
    # setup get data loop
    bno055.enter_fused_data_mode()           # Let the BNO055 do its nice thing
    #                                        # __set address to read from__
    # bno055.write_bytes([VECTOR_EULER])       # 1st byte of vector to read
    bno055.write_bytes([VECTOR_QUATERNION])  # 1st byte of vector to read
    #
    # loop to continuously get data
    last = time.time()
    while True:
        sample += 1
        ################
        # *~* animation stuff
        bno055.setup_anim()
        bno055.do_animate()
        # *~* end animation stuff
        ################

        ################
        # *~* euler reading stuff
        #        (if VECTOR_EULER previously written with write_bytes)
        # heading, roll, pitch = [i / 16 for i in bno055.read_vector()]
        # print "    heading: {0:5}   roll: {1:5}   yaw: {2:5}".\
        #     format(heading, roll, pitch)
        # *~* end euler reading stuff
        ################

        t, x, y, z = [i * quat_scale_f for i in bno055.read_vector(count=4)]
        print "    t = {0:.7f}  x = {1:.7f}  y = {2:.7f} z = {3:.7f}".\
            format(t, x, y, z)
        # print "norm = ", (t**2 + x**2 + y**2 + z**2)**0.5

        q = np.quaternion(t, x, y, z)
        q_array = np.append(q_array, q)  # append new quaternion to array
        #
        if sample > max_array_size:          # remove quaternions more than
            #                                    max_array_size samples in past
            q_array = np.delete(q_array, 0, axis=0)
        ########
        if sample % 100 is 0:
            print "*---------------------------------------------------------*"
            print q_array
            print "    -\n    -         sampling frequency:",\
                100 / (time.time() - last), "Hz\n    -"
            last = time.time()
            sys, gyro, accel, mag = bno055.get_cal_status(verbose=True)
            #                                         read calibration status
            #                                           0 is uncalibrated
            #                                           3 is fully calibrated
            #
            ################
            # *~* saving calibration data stuff
            # calibration_data = bno055.get_calibration_info(verbose=True)
            # write calibration_data to file calib_data.pickle
            # with open("calib_data.pickle", 'wb') as calib_data_file_object:
            #    pickle.dump(calibration_data, calib_data_file_object)
            # *~* end saving calibration data stuff
            ################
            print "*---------------------------------------------------------*"
            bno055.enter_fused_data_mode()      # reenter imu mode
            # bno055.write_bytes([VECTOR_EULER])  # address for next read
            bno055.write_bytes([VECTOR_QUATERNION])
    bno055.resetToTerm()
