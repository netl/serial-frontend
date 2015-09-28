ls -all /dev/ttyAMA0
crw-rw---- 1 root tty 204, 64 Aug 27 10:27 /dev/ttyAMA0

Resources
raspberry serial: http://elinux.org/RPi_Serial_Connection
python serial: http://pyserial.sourceforge.net/
python graphics: http://effbot.org/tkinterbook/

http://www.waveshare.com/wiki/4inch_RPi_LCD_(A)
https://github.com/notro/fbtft/issues/215#issuecomment-71336679

rotation for touch screen
in /etc/modules
change 'rotate' from 90 to 0
and in init=[...] ...0x36,0x28... to ...0x36,0x48...

recalibrate touch screen
dpkg -i xinput_calibrator

in /etc/lightdm/lightdm.conf
under [SeatDefault]
add xserver-command=X -s 0 dpms
