# Selpi

Selpi is woefully incomplete, but in the long run it will hopefully be a collection of basic utilties to monitor a Selectronic SP Pro 2 from a RaspberryPi.

Additional docs:

 * [Connecting](docs/connecting.md)
 * [Protocol](docs/protocol.md)
 * [Developing](docs/developing.md)

# License / Warranty

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

For those unfamiliar please note that this means no warranty OF ANY KIND is granted with this code, further it is possible using this code may impact on any warranty from Selectronic.

# Getting Started

[Pipenv](https://github.com/pypa/pipenv) is used to control managed dependencies, if it's not already installed, install it:

```
$ pip install pipenv
[...]
Successfully installed certifi-2019.9.11 enum34-1.1.6 pip-19.3.1 pipenv-2018.11.26 setuptools-41.4.0 typing-3.7.4.1 virtualenv-16.7.6 virtualenv-clone-0.5.3
```

On the first execution of `./selpi`, `pipenv` should install requirements:

```
$ ./selpi
Creating a virtualenv for this project...
Pipfile: .../code/selpi/Pipfile
Using /usr/bin/python3 (3.6.8) to create virtualenv...
⠹ Creating virtual environment...Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in .../.local/share/virtualenvs/selpi-E1h07TTq/bin/python3
Also creating executable in .../.local/share/virtualenvs/selpi-E1h07TTq/bin/python
Installing setuptools, pip, wheel...
done.
Running virtualenv with interpreter /usr/bin/python3

✔ Successfully created virtual environment!
```

# pvo-sppro2.py

The Python script `pvo-sppro2.py` is designed to upload basic data from a SP Pro 2 to [pvoutput.org](https://pvoutput.org/).

Once [connected](docs/connecting.md) to a SP Pro, modify the script to include your PVO credentials and the appropriate `ttyUSB` device. Run it with `python pvo-sppro2.py`.

# Acknowledgements

This repository is primarily maintained by [David Schoen](http://github.com/neerolyte).

Foundational code and inspirational advice provided by [Justin Stafford](https://www.linkedin.com/in/justin-stafford-blueshift/).