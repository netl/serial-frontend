#!/bin/bash
sudo adduser pi tty
wget http://netl.fi/file/LCD-show-150602.tar.gz
gunzip LCD-show-150602.tar.gz
tar -xvf LCD-show-150602.tar
sudo dpkg -i LCD-show/xinput-calibrator_0.7.5-1_armhf.deb
cp ./config/99-calibration.conf ./LCD-show/etc/X11/xorg.conf.d/99-calibration.conf-4
cp ./config/modules ./LCD-show/etc/modules-4
cd LCD-show
sudo ./LCD4-show
