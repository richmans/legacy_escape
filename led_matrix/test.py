import spidev
from time import sleep

def send(spi, cmd):
    print(cmd)
    spi.xfer(list(cmd))



bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 8000000
# turn it on
send(spi, [0xb, 7]*4)
send(spi, [0x9, 0]*4)
send(spi, [0xc, 1]*4)
send(spi, [0xa, 0x1]*4)
send(spi, [0xf, 0]*4)

while True:
    send(spi, [0x1, 0xf0]*4)
    send(spi, [0x2, 0xf0]*4)
    send(spi, [0x3, 0xf0]*4)
    send(spi, [0x4, 0xf0]*4)
    send(spi, [0x5, 0x00]*4)
    send(spi, [0x6, 0x00]*4)
    send(spi, [0x7, 0x00]*4)
    send(spi, [0x8, 0x00]*4)
    sleep(0.2)
    send(spi, [0x1, 0x00]*4)
    send(spi, [0x2, 0x00]*4)
    send(spi, [0x3, 0x00]*4)
    send(spi, [0x4, 0x00]*4)
    send(spi, [0x5, 0x0f]*4)
    send(spi, [0x6, 0x0f]*4)
    send(spi, [0x7, 0x0f]*4)
    send(spi, [0x8, 0x0f]*4)
    sleep(0.2)

