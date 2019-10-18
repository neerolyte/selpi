# Connecting to the SP Pro Series 2

<!-- TOC -->

- [Connecting to the SP Pro Series 2](#connecting-to-the-sp-pro-series-2)
- [USB](#usb)

<!-- /TOC -->

# USB

The USB plug found externally on a SP Pro Series 2 is a FTDI serial device that for whatever reason doesn't get recognised as one by current Linux kernels.

That means the appropriate FTDI module needs to be loaded.

The module can be checked for with:

```bash
root@rasp:~# lsmod | grep ^ftdi_sio
root@rasp:~#
```

The lack of output indicates it is not loaded, load it with:

```bash
root@rasp:~# modprobe ftdi_sio
root@rasp:~#
```

Now it should be loaded:

```bash
root@rasp:~# lsmod | grep ^ftdi_sio
ftdi_sio               32963  0 
```

When connecting the SP Pro dmesg will log something like:

```
[   69.587317] usb 1-1.3: new full-speed USB device number 4 using dwc_otg
[   69.748953] usb 1-1.3: New USB device found, idVendor=0403, idProduct=8508
[   69.748965] usb 1-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[   69.748972] usb 1-1.3: Product: Selectronic SP PRO
[   69.748980] usb 1-1.3: Manufacturer: Selectronic
[   69.748988] usb 1-1.3: SerialNumber: 1_234567
```

To enable the FTDI module to interact with it, tell it about the vendor/product ID like so:

```bash
root@rasp:~# echo 0403 8508 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
root@rasp:~#
```

The final lines in `dmesg` should now be like:

```
[  585.439423] ftdi_sio 1-1.3:1.0: FTDI USB Serial Device converter detected
[  585.439645] usb 1-1.3: Detected FT232RL
[  585.442042] usb 1-1.3: FTDI USB Serial Device converter now attached to ttyUSB0
```

In this case the final line indicates that a device is created at `/dev/ttyUSB0`:

```bash
root@rasp:~# ls -la /dev/ttyUSB0 
crw-rw---- 1 root dialout 188, 0 Oct 18 05:09 /dev/ttyUSB0
```