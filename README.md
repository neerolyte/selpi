# Selpi

Selpi is woefully incomplete, but in the long run it will hopefully be a collection of basic utilties to monitor a Selectronic SP Pro 2 from a RaspberryPi.

Additional docs:

 * [Connecting](docs/connecting.md)
 * [Protocol](docs/protocol.md)
 * [Developing](docs/developing.md)

# License / Warranty

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

For those unfamiliar please note that this means no warranty OF ANY KIND is granted with this code, further it is possible using this code may impact on any warranty from Selectronic.

# pvo-sppro2.py

The Python script `pvo-sppro2.py` is designed to upload basic data from a SP Pro 2 to [pvoutput.org](https://pvoutput.org/).

Once [connected](docs/connecting.md) to a SP Pro, modify the script to include your PVO credentials and the appropriate `ttyUSB` device. Run it with `python pvo-sppro2.py`.