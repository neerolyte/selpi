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

Selpi uses a sub command structure meaning the base `selpi` accepts multiple commands that run it in different modes.

See `selpi --help` for a full list of commands, some commands are documented below.

Additional logging output can be printed with `selpi --log=debug ...`.

## proxy

The `proxy` command is used to expose the Selectronic SP PRO over TCP.

The listening address and port can be controlled from `.env.local`.

To start the proxy run:

```
$ ./selpi proxy
```

TP LINK can then be configured to connect to the device `selpi` is started on.

## stat

The `stat` command displays the currently known stats from the SP PRO:

```bash
$ ./selpi stat
[
  {
    "description": "AC Solar Power",
    "name": "CombinedKacoAcPowerHiRes",
    "value": "572.894287109375W"
  },
  {
    "description": "Shunt 1 Name",
    "name": "Shunt1Name",
    "value": "Solar"
  },
  {
    "description": "Shunt 1 Power",
    "name": "Shunt1Power",
    "value": "-123.046875W"
  },
  {
    "description": "Shunt 2 Name",
    "name": "Shunt2Name",
    "value": "None"
  },
  {
    "description": "Shunt 2 Power",
    "name": "Shunt2Power",
    "value": "0.0W"
  },
  {
    "description": "Battery Volts",
    "name": "BatteryVolts",
    "value": "55.271759033203125V"
  },
  {
    "description": "Battery Temperature",
    "name": "BatteryTemperature",
    "value": "22.838134765625\u00b0C"
  },
  {
    "description": "AC Load Power",
    "name": "LoadAcPower",
    "value": "633.8310241699219W"
  },
  {
    "description": "Battery Power",
    "name": "DCBatteryPower",
    "value": "19.22607421875W"
  },
  {
    "description": "AC Lifetime Load Energy",
    "name": "ACLoadkWhTotalAcc",
    "value": "5143750.927734375Wh"
  },
  {
    "description": "Battery Out Energy Today",
    "name": "BattOutkWhPreviousAcc",
    "value": "3783.69140625Wh"
  },
  {
    "description": "Battery State of Charge",
    "name": "BattSocPercent",
    "value": "99.67578125%"
  }
]
```

# Acknowledgements

This repository is primarily maintained by [David Schoen](http://github.com/neerolyte).

Foundational code and inspirational advice provided by [Justin Stafford](https://www.linkedin.com/in/justin-stafford-blueshift/).
