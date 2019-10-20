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

Ensure your device is [connecting](docs/connecting.md) to the SP Pro.

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

# Commands

## stat

The `stat` command displays the currently known stats from the SP PRO:

```bash
$ ./selpi stat
commonScaleForACVolts: 4804
commonScaleForACCurrent: 1997
commonScaleForDcVolts: 730
commonScaleForDCCurrent: 21560
commonScaleForTemperature: 482
Solar Power: 0.0W
Solar Energy: 0.0Wh
Load Power: 0.0W
Load Energy: 6149710.073349609Wh
Battery Volts: 24.84869384765625V
Battery Power: 0.0W
```

# Acknowledgements

This repository is primarily maintained by [David Schoen](http://github.com/neerolyte).

Foundational code and inspirational advice provided by [Justin Stafford](https://www.linkedin.com/in/justin-stafford-blueshift/).
