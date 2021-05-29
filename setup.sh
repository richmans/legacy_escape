#!/bin/bash
if lsmod | grep spi_ ; then
  echo "Spi module detected"
else 
  echo "SPI module not detected. You will need to reboot after this!"
  sudo bash -c 'echo "dtparam=spi=on" >> /boot/config.txt'
fi

sudo apt install -y python3-spidev
sudo usermod -a -G dialout pi
sudo usermod -a -G spi pi
