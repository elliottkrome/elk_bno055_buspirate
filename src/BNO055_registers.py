# adapted from https://github.com/adafruit/Adafruit_BNO055

class Page_0:
    # page id register definition
    PAGE_ID_ADDR = 0X07  # reset value is 0x00

    # Info registers that are ALL FIXED-VALUE READ-ONLY
    CHIP_ID_ADDR = 0x00  # reset value is 0xA0        FIXED VALUE
    ACCEL_REV_ID_ADDR = 0x01  # reset value is 0xFB     ||
    MAG_REV_ID_ADDR = 0x02  # reset value is 0x32       ||
    GYRO_REV_ID_ADDR = 0x03  # reset value is 0x0F      ||
    SW_REV_ID_LSB_ADDR = 0x04  # reset value is 0x11    ||
    SW_REV_ID_MSB_ADDR = 0x05  # reset value is 0x03    ||
    BL_REV_ID_ADDR = 0X06  # reset value is 0x15 <- bootloader version

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~BEGIN-SENSOR-REGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Accel data register                                               ~~~~~~~
    ACCEL_DATA_X_LSB_ADDR = 0X08  # reset value is 0x00                 ~~~~~~~
    ACCEL_DATA_X_MSB_ADDR = 0X09  # reset value is 0x00                 ~~~~~~~
    ACCEL_DATA_Y_LSB_ADDR = 0X0A  # reset value is 0x00                 ~~~~~~~
    ACCEL_DATA_Y_MSB_ADDR = 0X0B  # reset value is 0x00                 ~~~~~~~
    ACCEL_DATA_Z_LSB_ADDR = 0X0C  # reset value is 0x00                 ~~~~~~~
    ACCEL_DATA_Z_MSB_ADDR = 0X0D  # reset value is 0x00                 ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Mag data register                                                 ~~~~~~~
    MAG_DATA_X_LSB_ADDR = 0X0E  # reset value is 0x00                   ~~~~~~~
    MAG_DATA_X_MSB_ADDR = 0X0F  # reset value is 0x00                   ~~~~~~~
    MAG_DATA_Y_LSB_ADDR = 0X10  # reset value is 0x00                   ~~~~~~~
    MAG_DATA_Y_MSB_ADDR = 0X11  # reset value is 0x00                   ~~~~~~~
    MAG_DATA_Z_LSB_ADDR = 0X12  # reset value is 0x00                   ~~~~~~~
    MAG_DATA_Z_MSB_ADDR = 0X13  # reset value is 0x00                   ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Gyro data registers                                               ~~~~~~~
    GYRO_DATA_X_LSB_ADDR = 0X14  # reset value is 0x00                  ~~~~~~~
    GYRO_DATA_X_MSB_ADDR = 0X15  # reset value is 0x00                  ~~~~~~~
    GYRO_DATA_Y_LSB_ADDR = 0X16  # reset value is 0x00                  ~~~~~~~
    GYRO_DATA_Y_MSB_ADDR = 0X17  # reset value is 0x00                  ~~~~~~~
    GYRO_DATA_Z_LSB_ADDR = 0X18  # reset value is 0x00                  ~~~~~~~
    GYRO_DATA_Z_MSB_ADDR = 0X19  # reset value is 0x00                  ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Euler data registe  # reset value is 0x00rs                       ~~~~~~~
    EULER_H_LSB_ADDR = 0X1A  # reset value is 0x00                      ~~~~~~~
    EULER_H_MSB_ADDR = 0X1B  # reset value is 0x00                      ~~~~~~~
    EULER_R_LSB_ADDR = 0X1C  # reset value is 0x00                      ~~~~~~~
    EULER_R_MSB_ADDR = 0X1D  # reset value is 0x00                      ~~~~~~~
    EULER_P_LSB_ADDR = 0X1E  # reset value is 0x00                      ~~~~~~~
    EULER_P_MSB_ADDR = 0X1F  # reset value is 0x00                      ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Quaternion data registers                                         ~~~~~~~
    QUATERNION_DATA_W_LSB_ADDR = 0x20  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_W_MSB_ADDR = 0X21  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_X_LSB_ADDR = 0X22  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_X_MSB_ADDR = 0X23  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_Y_LSB_ADDR = 0X24  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_Y_MSB_ADDR = 0X25  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_Z_LSB_ADDR = 0X26  # reset value is 0x00            ~~~~~~~
    QUATERNION_DATA_Z_MSB_ADDR = 0X27  # reset value is 0x00            ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Linear acceleration data registers                                ~~~~~~~
    LINEAR_ACCEL_DATA_X_LSB_ADDR = 0X28  # reset value is 0x00          ~~~~~~~
    LINEAR_ACCEL_DATA_X_MSB_ADDR = 0X29  # reset value is 0x00          ~~~~~~~
    LINEAR_ACCEL_DATA_Y_LSB_ADDR = 0X2A  # reset value is 0x00          ~~~~~~~
    LINEAR_ACCEL_DATA_Y_MSB_ADDR = 0X2B  # reset value is 0x00          ~~~~~~~
    LINEAR_ACCEL_DATA_Z_LSB_ADDR = 0X2C  # reset value is 0x00          ~~~~~~~
    LINEAR_ACCEL_DATA_Z_MSB_ADDR = 0X2D  # reset value is 0x00          ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Gravity data registers                                            ~~~~~~~
    GRAVITY_DATA_X_LSB_ADDR = 0X2E  # reset value is 0x00               ~~~~~~~
    GRAVITY_DATA_X_MSB_ADDR = 0X2F  # reset value is 0x00               ~~~~~~~
    GRAVITY_DATA_Y_LSB_ADDR = 0X30  # reset value is 0x00               ~~~~~~~
    GRAVITY_DATA_Y_MSB_ADDR = 0X31  # reset value is 0x00               ~~~~~~~
    GRAVITY_DATA_Z_LSB_ADDR = 0X32  # reset value is 0x00               ~~~~~~~
    GRAVITY_DATA_Z_MSB_ADDR = 0X33  # reset value is 0x00               ~~~~~~~
    #                                                                   ~~~~~~~
    # All registers in '~~~~~~~' block can be manipulated as follow:    ~~~~~~~
    #     Output units can be selected via the UNIT_SEL register (0x3B) ~~~~~~~
    #     Data output type can be changed by updating Operation Mode    ~~~~~~~
    #       in OPR_MODE register (0x3D)                                 ~~~~~~~
    #                                                                   ~~~~~~~
    # Temperature data register                                         ~~~~~~~
    TEMP_ADDR = 0X34  # reset value is 0x00                             ~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~END_SENSOR_REGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

    # Status registers
    CALIB_STAT_ADDR = 0X35  # reset value is 0x00
    """
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
    |-----+--------+------------------|
    """
    SELFTEST_RESULT_ADDR = 0X36  # reset value is 0x0F
    #                 if val not 0x0F some self-test failed
    #                    i.e. MCU_general, GYR, MAG, or ACC
    INTR_STAT_ADDR = 0X37  # reset value is 0x00
    #                 INTERRUPT REGISTER
    """
    |-----+--------+---------------|
    | bit | access | content       |
    |-----+--------+---------------|
    |   7 |   r    | ACC_NM        | accelerometer NO motion interrupt
    |-----+--------+---------------|
    |   6 |   r    | ACC_AM        | accelerometer ANY motion interrupt
    |-----+--------+---------------|
    |   5 |   r    | ACC_HIGH_G    | accelerometer HIGH-GRAVITY interrupt
    |-----+--------+---------------|
    |   4 |   r    | reserved      |
    |-----+--------+---------------|
    |   3 |   -    | GYR_HIGH_RATE | gyroscope HIGH RATE interrupt
    |-----+--------+---------------|
    |   2 |   r    | GYR_AM        | gyroscope ANY motion interrupt
    |-----+--------+---------------|
    |   1 |   -    | reserved      |
    |-----+--------+---------------|
    |   0 |   -    | reserved      |
    |-----+--------+---------------|
    """
    SYS_CLK_STAT_ADDR = 0X38  # reset value is 0x00
    #                 value of 0x00 inidicates it is Free to configure CLK SRC
    #                 value of 0X01 indicates clock in "Configuration State"
    SYS_STAT_ADDR = 0X39  # reset value is 0x00
    """
    System status codes:
        0 -> System idle,
        1 -> System Error,
        2 -> Initializing peripherals
        3 -> System Initialization
        4 -> Executing selftest,
        5 -> Sensor fusion algorithm running,
        6 -> System running without fusion algorithm
    """
    SYS_ERR_ADDR = 0X3A  # reset value is 0x00
    """
    System error codes:
        0 No error
        1 -> Peripheral initialization error
        2 -> System initialization error
        3 -> Self test result failed
        4 -> Register map value out of range
        5 -> Register map address out of range
        6 -> Register map write error
        7 -> BNO low power mode not available for selected operation mode
        8 -> Accelerometer power mode not available
        9 -> Fusion algorithm configuration error
        A -> Sensor configuration error
    """
    # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

    # Unit selection register
    UNIT_SEL_ADDR = 0X3B  # reset value is 0x80
    """
    |-----+--------+---------------------|
    | bit | access | content             | 0: Windows Orientation
    |-----+--------+---------------------| 1: Android Orinetation
    |   7 | r/w    | ORI_Android_Windows |
    |-----+--------+---------------------|
    |   6 | -      | reserved            |
    |-----+--------+---------------------|
    |   5 | -      | reserved            |
    |-----+--------+---------------------|
    |   4 | r/w    | TEMP_Unit           | 0: Celsius
    |-----+--------+---------------------| 1: Fahrenheit
    |   3 | -      | reserved            |
    |-----+--------+---------------------|
    |   2 | r/w    | EUL_Unit            | 0: Degrees
    |-----+--------+---------------------| 1: Radians
    |   1 | r/w    | GYR_Unit            | 0: Degrees per second
    |-----+--------+---------------------| 1: Radians per second
    |   0 | r/w    | ACC_Unit            | 0: m/(s^2)
    |-----+--------+---------------------| 1: mg
    """
    DATA_SELECT_ADDR = 0X3C  # reset value is 0xFF

    # Mode registers
    OPR_MODE_ADDR = 0X3D  # reset value is 0x10
    #                 see class "OPR_MODE" defined below
    PWR_MODE_ADDR = 0X3E  # reset value is 0x00

    SYS_TRIGGER_ADDR = 0X3F  # reset value is 0x00
    #                 bit 7: CLK_SEL   0-internal oscillator 1-external crystal
    #                 bit 6: RST_INT   set to reset all interrupt
    #                                    status bits and int output
    #                 bit 5: RST_SYS   set to reset system
    #                 bit 0: Self_Test set to trigger self test
    TEMP_SOURCE_ADDR = 0X40  # reset value is 0x00

    # Axis remap registers
    AXIS_MAP_CONFIG_ADDR = 0X41  # reset value is 0x24
    """
    |-----+--------+---------|
    | bit | access | content |
    |-----+--------+---------|
    |   7 |  -     |         | reserved
    |-----+--------+---------|
    |   6 |  -     |         | reserved
    |-----+--------+---------|
    |   5 |  r/w   |         | remapped Z axis value
    |-----+--------+---------|   ||
    |   4 |  r/w   |         |   ||
    |-----+--------+---------|   ||
    |   3 |  r/w   |         | remapped Y axis value
    |-----+--------+---------|   ||
    |   2 |  r/w   |         |   ||
    |-----+--------+---------|   ||
    |   1 |  r/w   |         | remapped X axis value
    |-----+--------+---------|   ||
    |   0 |  r/w   |         |   ||
    |-----+--------+---------|   ||
    """
    AXIS_MAP_SIGN_ADDR = 0X42  # reset value is 0x00
    #                 bit 2 - remapped X axis sign
    #                 bit 1 - remapped Y axis sign
    #                 bit 0 - remapped Z axis sign

    # SIC registers
    SIC_MATRIX_0_LSB_ADDR = 0X43  # reset value is 0x00
    SIC_MATRIX_0_MSB_ADDR = 0X44  # reset value is 0x40
    SIC_MATRIX_1_LSB_ADDR = 0X45  # reset value is 0x00
    SIC_MATRIX_1_MSB_ADDR = 0X46  # reset value is 0x00
    SIC_MATRIX_2_LSB_ADDR = 0X47  # reset value is 0x00
    SIC_MATRIX_2_MSB_ADDR = 0X48  # reset value is 0x00
    SIC_MATRIX_3_LSB_ADDR = 0X49  # reset value is 0x00
    SIC_MATRIX_3_MSB_ADDR = 0X4A  # reset value is 0x00
    SIC_MATRIX_4_LSB_ADDR = 0X4B  # reset value is 0x00
    SIC_MATRIX_4_MSB_ADDR = 0X4C  # reset value is 0x40
    SIC_MATRIX_5_LSB_ADDR = 0X4D  # reset value is 0x00
    SIC_MATRIX_5_MSB_ADDR = 0X4E  # reset value is 0x00
    SIC_MATRIX_6_LSB_ADDR = 0X4F  # reset value is 0x00
    SIC_MATRIX_6_MSB_ADDR = 0X50  # reset value is 0x00
    SIC_MATRIX_7_LSB_ADDR = 0X51  # reset value is 0x00
    SIC_MATRIX_7_MSB_ADDR = 0X52  # reset value is 0x00
    SIC_MATRIX_8_LSB_ADDR = 0X53  # reset value is 0x00
    SIC_MATRIX_8_MSB_ADDR = 0X54  # reset value is 0x40

    # Accelerometer Offset registers
    ACCEL_OFFSET_X_LSB_ADDR = 0X55  # reset value is 0x00
    ACCEL_OFFSET_X_MSB_ADDR = 0X56  # reset value is 0x00
    ACCEL_OFFSET_Y_LSB_ADDR = 0X57  # reset value is 0x00
    ACCEL_OFFSET_Y_MSB_ADDR = 0X58  # reset value is 0x00
    ACCEL_OFFSET_Z_LSB_ADDR = 0X59  # reset value is 0x00
    ACCEL_OFFSET_Z_MSB_ADDR = 0X5A  # reset value is 0x00

    # Magnetometer Offset registers
    MAG_OFFSET_X_LSB_ADDR = 0X5B  # reset value is 0x00
    MAG_OFFSET_X_MSB_ADDR = 0X5C  # reset value is 0x00
    MAG_OFFSET_Y_LSB_ADDR = 0X5D  # reset value is 0x00
    MAG_OFFSET_Y_MSB_ADDR = 0X5E  # reset value is 0x00
    MAG_OFFSET_Z_LSB_ADDR = 0X5F  # reset value is 0x00
    MAG_OFFSET_Z_MSB_ADDR = 0X60  # reset value is 0x00

    # Gyroscope Offset register
    GYRO_OFFSET_X_LSB_ADDR = 0X61  # reset value is 0x00
    GYRO_OFFSET_X_MSB_ADDR = 0X62  # reset value is 0x00
    GYRO_OFFSET_Y_LSB_ADDR = 0X63  # reset value is 0x00
    GYRO_OFFSET_Y_MSB_ADDR = 0X64  # reset value is 0x00
    GYRO_OFFSET_Z_LSB_ADDR = 0X65  # reset value is 0x00
    GYRO_OFFSET_Z_MSB_ADDR = 0X66  # reset value is 0x00

    # Radius registers
    ACCEL_RADIUS_LSB_ADDR = 0X67  # reset value is 0x00
    ACCEL_RADIUS_MSB_ADDR = 0X68  # reset value is 0x00
    MAG_RADIUS_LSB_ADDR = 0X69  # reset value is 0xE0
    MAG_RADIUS_MSB_ADDR = 0X6A  # reset value is 0x01


class Page_1:
    PAGE_ID = 0x07  # reset value is 0x01

    ACC_CONFIG = 0x08  # reset value is 0x0D
    MAG_CONFIG = 0x09  # reset value is 0x6D
    GYR_CONFIG_0 = 0x0A  # reset value is 0x38
    GYR_CONFIG_1 = 0x0B  # reset value is 0x00

    GYR_SLEEP_CONFIG = 0x0D  # reset value is 0x00
    ACC_SLEEP_CONFIG = 0x0C  # reset value is 0x00

    INT_MSK = 0x0F  # reset value is 0x00
    INT_EN = 0x10  # reset value is 0x00

    ACC_AM_THRESHOLD = 0x11  # reset value is 0x14
    ACC_INT_SETTINGS = 0x12  # reset value is 0x03
    ACC_H_DURATION = 0x13  # reset value is 0x0F
    ACC_HG_THRESHOLD = 0x14  # reset value is 0xC0
    ACC_NM_THRESHOLD = 0x15  # reset value is 0x0A
    ACC_NM_SET = 0x16  # reset value is 0x0B

    GYR_INT_SETTINGS = 0x17  # reset value is 0x00
    GYR_HR_X_SET = 0x18  # reset value is 0x01
    GYR_DUR_X = 0x19  # reset value is 0x19
    GYR_HR_Y_SET = 0x1A  # reset value is 0x01
    GYR_DUR_Y = 0x1B  # reset value is 0x19
    GYR_HR_Z_SET = 0x1C  # reset value is 0x01
    GYR_DUR_Z = 0x1D  # reset value is 0x19
    GYR_AM_THRESHOLD = 0x1E  # reset value is 0x04
    GYR_AM_SET = 0x1F  # reset value is 0x0A

# POWER_MODE:
POWER_MODE_NORMAL = 0X00
POWER_MODE_LOWPOWER = 0X01
POWER_MODE_SUSPEND = 0X02


# OPR_MODE:
# Operation mode settings
CONFIG = 0X00        # configuration mode
ACCONLY = 0X01       # non-fusion mode
MAGONLY = 0X02       # ||
GYRONLY = 0X03       # ||
ACCMAG = 0X04        # ||
ACCGYRO = 0X05       # ||
MAGGYRO = 0X06       # ||
AMG = 0X07           # ||
IMUPLUS = 0X08       # fusion mode
COMPASS = 0X09       # ||
M4G = 0X0A           # ||
NDOF_FMC_OFF = 0X0B  # ||
NDOF = 0X0C          # ||


# AXIS_REMAP_CONFIG:
REMAP_CONFIG_P0 = 0x21
REMAP_CONFIG_P1 = 0x24  # default
REMAP_CONFIG_P2 = 0x24
REMAP_CONFIG_P3 = 0x21
REMAP_CONFIG_P4 = 0x24
REMAP_CONFIG_P5 = 0x21
REMAP_CONFIG_P6 = 0x21
REMAP_CONFIG_P7 = 0x24


# AXIS_REMAP_SIGN:
REMAP_SIGN_P0 = 0x04
REMAP_SIGN_P1 = 0x00  # default
REMAP_SIGN_P2 = 0x06
REMAP_SIGN_P3 = 0x02
REMAP_SIGN_P4 = 0x03
REMAP_SIGN_P5 = 0x01
REMAP_SIGN_P6 = 0x07
REMAP_SIGN_P7 = 0x05

# Axis remap values
AXIS_REMAP_X = 0x00
AXIS_REMAP_Y = 0x01
AXIS_REMAP_Z = 0x02
AXIS_REMAP_POSITIVE = 0x00
AXIS_REMAP_NEGATIVE = 0x01

# VECTOR:
VECTOR_ACCELEROMETER = PAGE_0.ACCEL_DATA_X_LSB_ADDR
VECTOR_MAGNETOMETER = PAGE_0.MAG_DATA_X_LSB_ADDR
VECTOR_GYROSCOPE = PAGE_0.GYRO_DATA_X_LSB_ADDR
VECTOR_EULER = PAGE_0.EULER_H_LSB_ADDR
VECTOR_LINEARACCEL = PAGE_0.LINEAR_ACCEL_DATA_X_LSB_ADDR
VECTOR_GRAVITY = PAGE_0.GRAVITY_DATA_X_LSB_ADDR
VECTOR_QUATERNION = PAGE_0.QUATERNION_DATA_W_LSB_ADDR

"""
    |-----+--------+---------|
    | bit | access | content |
    |-----+--------+---------|
    |   7 |        |         |
    |-----+--------+---------|
    |   6 |        |         |
    |-----+--------+---------|
    |   5 |        |         |
    |-----+--------+---------|
    |   4 |        |         |
    |-----+--------+---------|
    |   3 |        |         |
    |-----+--------+---------|
    |   2 |        |         |
    |-----+--------+---------|
    |   1 |        |         |
    |-----+--------+---------|
    |   0 |        |         |
    |-----+--------+---------|
    """
