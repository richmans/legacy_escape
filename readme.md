# LED Matrix
The following describes what is needed to get the led matri working on the raspi.

### first hook it up...
```
vcc + 5 -> 2
gnd -> 6
din -> mosi (19)
cs -> ce0 (24)
clk -> clk (23)
```

### install some stuff
we basically need python and pip `sudo apt-get install python3-dev python3-pip`
and spidev: `sudo pip3 install spidev`

Give your user access to spi: `sudo usermod -a -G spi pi` and also `sudo usermod -a -G dialout pi` 

# What can you do with this?
Test the led matrix: `python3 led_matrix.py -d`

Play tetris: `python3 tetris.py`

Hook up your digirule 2u, set it to debug mode, and watch the memory: `python3 digirule.py`

### bringup notes
Here's an example library that seems to work correctly
https://github.com/rm-hull/luma.led_matrix

check the spi module:
`ls -l /dev/spi*` if no result, install the module using raspi-config, under interfaces

Test functionality:
`sudo python3 examples/matrix_demo.py --cascaded 4 --block-orientation 90 --reverse-order 1`

Important lesson: the max-chip supports speeds up to 10mhz. we need to configure the spidev lib to set the speed to 8mhz or less!


# rotary encoder

Nice blog about setting up: https://blog.ploetzli.ch/2018/ky-040-rotary-encoder-linux-raspberry-pi/
