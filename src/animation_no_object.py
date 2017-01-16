#!Users/elliottkrome/anaconda/bin/python
import logging
import os
import pickle
from BNO055 import *
import quaternion
import numpy as np
from pyquaternion import Quaternion


from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    global sample_count
    sample_count = 0
    visualization = True
    bno055 = BNO055("/dev/tty.usbserial-AH03F33K", 115200, timeout=0.4)

    ################################################################
    # from https://github.com/KieranWynn/pyquaternion/blob/master/demo/demo.py

    # initialization function:
    #   plot the background of each frame
    def get_quat_for_anim():
        t, x, y, z = [i * quat_scale_f for i in bno055.read_vector(count=4)]
        q1 = Quaternion(scalar=t, vector=[x, y, z])
        print "    t = {0:.7f}  x = {1:.7f}  y = {2:.7f} z = {3:.7f}".\
            format(t, x, y, z)
        return q1

    def anim_init():
        for line in lines:
            line.set_data([], [])
            line.set_3d_properties([])
        return lines

    # animation function:
    #   called sequentially with the frame number
    def animate(i):
        global sample_count
        global last
        q = get_quat_for_anim()
        for line, start, end in zip(lines, startpoints, endpoints):
            start = q.rotate(start)
            end = q.rotate(end)
            #
            line.set_data([start[0], end[0]], [start[1], end[1]])
            line.set_3d_properties([start[2], end[2]])
        fig.canvas.draw()
        sample_count += 1
        if sample_count % 50 is 0:
            print "*---------------------------------------------------*"
            print "    -\n    -         sampling frequency:",\
                50 / (time.time() - last), "Hz\n    -"
            bno055.last = time.time()
            #
            #  read calibration status
            sys, gyro, accel, mag = bno055.get_cal_status(verbose=True)
            #                             verbose to print inside function
            #                                         0 is uncalibrated
            #                                         3 is fully calibrated
            # calibration_data = bno055.get_calibration_info(verbose=True)
            # write calibration_data to file calib_data.txt
            # with open("calib_data.txt", 'wb') as calib_data_file_object:
            #    pickle.dump(calibration_data, calib_data_file_object)
            #
            print "*---------------------------------------------------*"
            bno055.enter_fused_data_mode()      # reenter imu mode
            # bno055.write_bytes([VECTOR_EULER])  # address for next read
            bno055.write_bytes([VECTOR_QUATERNION])
        return lines

    if visualization is True:
        # Set up figure & 3D axis for animation
        fig = plt.figure()
        ax = Axes3D(fig)  # changed from demo in git  Previous line was:
        #                   'ax = fig.add_axes([0, 0, 1, 1], projection='3d')'
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #
        # use a different color for each axis
        colors = ['r', 'g', 'b']
        #
        # set up lines and points
        lines = sum([ax.plot([], [], [], c=c)
                     for c in colors], [])
        startpoints = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        endpoints = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        #
        # prepare the axes limits
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)
        #
        # end from KiernanWynn github demo
    ################################################################

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
    config_data = pickle.load(open('calib_data.txt', 'rb'))
    bno055.set_calibration(config_data)
    bno055.get_cal_status(verbose=True)
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
        ################
        # animation stuff
        anim = animation.FuncAnimation(fig,
                                       animate,
                                       init_func=anim_init,
                                       frames=500,
                                       interval=1,
                                       blit=False)
        plt.show()
        # end animation stuff
        ################
        sample += 1
        ########
        # heading, roll, pitch = [i / 16 for i in bno055.read_vector()]
        # print "    heading: {0:5}   roll: {1:5}   yaw: {2:5}".\
        #     format(heading, roll, pitch)
        ########
        # s = mlab.mesh(heading, pitch, roll)
        # mlab.show()
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
        if sample % 50 is 0:
            print "*---------------------------------------------------------*"
            print q_array
            print "    -\n    -         sampling frequency:",\
                50 / (time.time() - last), "Hz\n    -"
            last = time.time()
            sys, gyro, accel, mag = bno055.get_cal_status(verbose=True)
            #                                         read calibration status
            #                                           0 is uncalibrated
            #                                           3 is fully calibrated
            # calibration_data = bno055.get_calibration_info(verbose=True)
            # write calibration_data to file calib_data.txt
            # with open("calib_data.txt", 'wb') as calib_data_file_object:
            #    pickle.dump(calibration_data, calib_data_file_object)
            #
            print "*---------------------------------------------------------*"
            bno055.enter_fused_data_mode()      # reenter imu mode
            # bno055.write_bytes([VECTOR_EULER])  # addres for next read
            bno055.write_bytes([VECTOR_QUATERNION])
    bno055.resetToTerm()
