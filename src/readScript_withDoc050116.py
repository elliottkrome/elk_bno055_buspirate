#!Users/elliottkrome/anaconda/bin/python
import sys
from pyBusPirate.BinaryMode.I2C import *
from BNO055 import PAGE_1
from BNO055_helpers import *


def i2c_write_data(data):
    i2c.send_start_bit()
    # i2c.bulk_trans() is defined in BitBang.py
    i2c.bulk_trans(len(data), data)
    i2c.send_stop_bit()


def i2c_read_bytes(address, numbytes, ret=False):
    """ i2c.read_byte() is definied in I2C.py as follows:
        def read_byte(self):
                self.port.write(b"\x04")
                self.timeout(0.1)
                return self.response(1, True)"""
    data_out = []
    i2c.send_start_bit()
    # i2c.bulk_trans() is defined in BitBang.py
    i2c.bulk_trans(len(address), address)
    byteNum = 0
    while numbytes > 0:
        if(ret is False):
            byte = i2c.read_byte()
            print "  byteNum {0:4} hex: {1:4}".format(byteNum, byteToHex(byte))
        else:
            data_out.append(i2c.read_byte())
        if numbytes > 1:    # !! CHANGED FROM PROVIDED TEST FILE !!!!!!!!!!
            i2c.send_ack()  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        numbytes -= 1
        byteNum += 1
    i2c.send_stop_bit()
    if ret is True:
        return data_out

"""
timeout uses select.select([], [], [], timeout_arg)
definition of select.select() follows:

select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)

Wait until one or more file descriptors are ready for some kind of I/O.
The first three arguments are sequences of file descriptors to be waited for:
rlist -- wait until ready for reading
wlist -- wait until ready for writing
xlist -- wait for an ``exceptional condition''
If only one kind of condition is required, pass [] for the other lists.
A file descriptor is either a socket or file object, or a small integer
gotten from a fileno() method call on one of those.

The optional 4th argument specifies a timeout in seconds; it may be
a floating point number to specify fractions of seconds.  If it is absent
or None, the call will never time out.

The return value is a tuple of three lists corresponding to the first three
arguments; each contains the subset of the corresponding file descriptors
that are ready.

"""

if __name__ == '__main__':
    file = open('/Users/elliottkrome/BNO055/testfile', 'wb')
#################################################################
    """
    I2C derives from BBIO class                            <---------------
    I2C __init__ function follows:
        def __init__(self, port='/dev/tty.usbserial-AH03F33K',
                     speed=115200, timeout=1):
                super(I2C, self).__init__(port, speed, timeout)
    BIBO derives from object (a "new style" of class - aka later than 2.2)
    BIBO __init__ function follows:
        def __init__(self, p="/dev/bus_pirate", s=115200, t=1):
                self.port = serial.Serial(p, s, timeout=t) <---------------
    """
    i2c = I2C("/dev/tty.usbserial-AH03F33K", 115200, 0.1)
#################################################################
    """ def of BBmode() is in BitBang.py, and follows:
    def BBmode(self):
        self.resetBP()
        for i in range(20):
            self.reset()
            self.port.flushInput()
            self.reset()
            if self.response(5) == b"BBIO1":               <--------------
                return 1
        else:
            return 0
    ''' definition of self.response() from BitBang.py:
    def response(self, byte_count=1, return_data=False):
                data = self.port.read(byte_count)
                if byte_count == 1 and return_data is False:
                        if data == b"\x01":
                                return 1
                        else:
                                return 0
                else:
                        return data
"""
    if i2c.BBmode():
        print "  bitbang mode OK"
    else:
        print "**> failed at bitbang mode"
        sys.exit()
#################################################################
    print "Entering raw I2C mode:\n",
    """
    def of enter_I2C() is in BitBang.py, and follows:
    def enter_I2C(self):
            self.port.write(b"\x02")
            self.timeout(0.1)
            if self.response(4) == b"I2C1":
                    return 1
            else:
                    return 0
    """
    if i2c.enter_I2C():
        print "  raw I2C mode OK."
    else:
        print "**> failed to enter I2C mode"
        sys.exit()
#################################################################
    print "Configuring I2C."
    if not i2c.cfg_pins(I2CPins.POWER | I2CPins.PULLUPS):
        # (I2CPins.POWER | I2CPins.PULLUPS) = (0x08 | 0x04) = d'12
        print "**> failed to set I2C peripherals."
        sys.exit()
    if not i2c.set_speed(I2CSpeed._5KHZ):
        print "**> failed to set I2C Speed."
        sys.exit()
    print "  i2c power and pullups on\n  i2c speed set."
    i2c.timeout(0.1)  # NECESSARY
    # printSettings(i2c)
#################################################################
#################################################################
#################################################################
    print "Reading EEPROM."
    """" CHANGED THIS FROM LIBRARY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    0x50 is write address for BNO055 in I2C address space
    0x51 is read  address for BNO055 in I2C address space
    0xA0 -> 0x50
    0xA1 -> 0x51
    """
    """             0x50 is address of writable BNO055 in I2C address space
                      0x28 is 7-bit address which is shifted left one bit
                      ((0x28 << 1) | 0x00) = 0x50
                                     where the 0x00 indicates '!read'
                          Second entry selects address in BNO055 address space
                            to start read from """
    """             0x51 is address of readable BNO055 in I2c address space
                      0x28 is 7-bit address which is shifted left one bit
                      ((0x28 << 1) | 0x01) = 0x51
                                     where the 0x01 indicates 'read'
                           second entry says how many bytes to read """
    # see functions at top of file
    print "1) Printing from address", PAGE_1.SELFTEST_RESULT_ADDR
    i2c_write_data([0x50, PAGE_1.SELFTEST_RESULT_ADDR])
    i2c_read_bytes([0x51], 7)
    print "2) Printing from address", PAGE_1.TEMP_ADDR
    i2c_write_data([0x50, PAGE_1.TEMP_ADDR])
    i2c_read_bytes([0x51], 7)
    print "3) Printing from address", PAGE_1.SELFTEST_RESULT_ADDR
    i2c_write_data([0x50, PAGE_1.SELFTEST_RESULT_ADDR])
    i2c_read_bytes([0x51], 7)
    print "4) Printing from address", PAGE_1.SELFTEST_RESULT_ADDR
    i2c_write_data([0x50, PAGE_1.SELFTEST_RESULT_ADDR])
    i2c_read_bytes([0x51], 7)
    print "5) Printing from address", PAGE_1.CHIP_ID_ADDR
    i2c_write_data([0x50, PAGE_1.CHIP_ID_ADDR])
    i2c_read_bytes([0x51], 7)
    print "6) Printing from address", PAGE_1.SELFTEST_RESULT_ADDR
    i2c_write_data([0x50, PAGE_1.SELFTEST_RESULT_ADDR])
    i2c_read_bytes([0x51], 7)
#################################################################
    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "**> failed to reset bus pirate to user term"
        sys.exit()
#################################################################
