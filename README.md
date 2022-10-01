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

Install dependencies with:

```
$ pipenv install
```

The `./selpi` will try to launch `selpi` within the pipenv, so just run:

```
$ ./selpi
Loading .env environment variables...
usage: selpi.py [-h] [--log {info,debug,warning,error,critical}] {command} ...

positional arguments:
  {command}             command to run
    dump                dump memory to stdout
    http                start http server
    http-select         select.live http emulation
    proxy               expose SP PRO over TCP proxy
    scan                scan known addresses
    stat                show known stats

options:
  -h, --help            show this help message and exit
  --log {info,debug,warning,error,critical}
                        log level
```

# Commands

Selpi uses a sub command structure meaning the base `selpi` accepts multiple commands that run it in different modes.

See `selpi --help` for a full list of commands, some commands are documented below.

Additional logging output can be printed with `selpi --log=debug ...`.

## http-select

```
$ ./selpi http-select
Loading .env environment variables...
Starting server on port 8000
```

Once running it will respond to all HTTP requests with a payload similar to the point API on select.live devices, e.g:

```
$ curl -s http://localhost:8000/cgi-bin/solarmonweb/devices/SOMEDEVICE/point
{
  "device":{
    "name":"Selectronic SP-PRO"
  },
  "item_count":19,
  "items":{
    "battery_in_wh_today":11.443359375,
    "battery_in_wh_total":6813.32080078125,
    "battery_out_wh_today":8.21337890625,
    "battery_out_wh_total":6789.603515625,
    "battery_soc":99.0859375,
    "battery_w":707.51953125,
    "grid_in_wh_today":0.3416015625,
    "grid_in_wh_total":43.810400390625,
    "grid_out_wh_today":0.0,
    "grid_out_wh_total":0.0,
    "grid_w":-3.558349609375,
    "load_w":678.3103942871094,
    "load_wh_today":22410.514306640624,
    "load_wh_total":15489.325048828125,
    "shunt_w":23.0712890625,
    "solar_wh_today":27.761865234375,
    "solar_wh_total":17579.099853515625,
    "solarinverter_w":56.93359375,
    "timestamp":1664611058
  },
  "comment":"energies are actually in kWh, not Wh",
  "now":1664611058
}
```

Note: `fault_code`, `fault_ts` and `gen_status` are missing.

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
    "value": 4707.696533203125,
    "units": "W"
  },
  {
    "description": "Shunt 1 Name",
    "name": "Shunt1Name",
    "value": "Solar",
    "units": ""
  },
...
  {
    "description": "Battery Out Energy Today",
    "name": "BattOutkWhPreviousAcc",
    "value": 5998.53515625,
    "units": "Wh"
  },
  {
    "description": "Battery State of Charge",
    "name": "BattSocPercent",
    "value": 87.55859375,
    "units": "%"
  }
]
```

# Acknowledgements

This repository is primarily maintained by [David Schoen](http://github.com/neerolyte).

Foundational code and inspirational advice provided by [Justin Stafford](https://www.linkedin.com/in/justin-stafford-blueshift/).
