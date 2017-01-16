# elk_bno055_buspirate

## What is this?
This is a Python project that allows for the use of the bus pirate's i2c capabilities to interface with a Bosch BNO055 chip. This allows for real time gestural interaction. Real time animation of movement via matplotlib is included as well.

This was originally developed as part of [A Temple University student group, IdeasX](https://hackaday.io/project/12850-ideasx).

There are two basic parts to this.

#### 1. An I2C interface to the Bosch BNO055 chip
It uses the [I2C protocol](https://en.wikipedia.org/wiki/I%C2%B2C) capabilities of the [Bus Pirate](https://en.wikipedia.org/wiki/Bus_Pirate) to stream [quaternion](http://mathworld.wolfram.com/Quaternion.html) data from a *beautiful* 9DOF sensor, the [BNOO55](https://www.bosch-sensortec.com/bst/products/all_products/bno055) from Bosch Sensortec. I used (and altered) the [audiohacked/pyBusPirate](https://github.com/audiohacked/pyBusPirate/tree/d6de9f90cb6373aa5fe0779a831cf496364fb01d) library for some of this.

In effect, very well conditioned quaternion data streams to `stdout` in real time.

I took extensive notes (located under the notes directory) on all aspects of this part of the project. This should help anybody who comes later get this rolling pretty quickly.

#### 2. A real-time animation of the incoming data.
Any number of interesting libraries could be built on top of this.

Using the [KieranWynn/pyquaternion](https://github.com/KieranWynn/pyquaternion/tree/d7bf1d6a6e5a755ef6c54f80bf07855cafcda6b7) library in conjunction with the [http://matplotlib.org/](matplotlib) library, I built a real time animation of the streaming quaternion data. I did this in part to demonstrate that the I2C interface piece actually was working, and in part because it was very cool to see a 3d animation of the user's motion. A slightly fancier version of a similar project can be viewed at the [Adafruit website](https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/overview).

### Usage:
follow the notes in notes/notes_regarding_bus_pirate_and_bno055.org to get setup.
once setup:

    python driver_with_animation.py

should do the trick
