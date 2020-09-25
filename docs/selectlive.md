# Select.live

Selectronic make a monitoring device that pairs with the SaaS service [select.live](https://select.live/).

[SPLink](http://www.selectronic.com.au/sppro/splink.htm) is able to use select.live to connect to a SP Pro. This is an attempt to figure out enough of that connection to try running selpi over select.live.

# Basic connection

SPLink connects to select.live on port 7528 via standard TLS so it's possible to use the `openssl` utility to establish a basic connection:

```
$ openssl s_client -connect select.live:7528
[...]
LOGIN
```

# Commands

## USER

select.live expects to receive credentials after printing `LOGIN`, they are supplied as `USER:<username>:<password>\r\n` e.g:

```
$ openssl s_client -connect select.live:7528
[...]
LOGIN
USER:somebody@example.com:thisIsMyRealPassword
OK
```

Bad credentials will get a response of `REJECTED`.

## LIST DEVICES

The `LIST DEVICES` command will list out available devices e.g:

```
LIST DEVICES
DEVICES:1
DEVICE:123456
```

The integer after `DEVICE:` will be the serial number of the SP Pro connected to the select.live device.

## CONNECT

```
CONNECT:123456
READY
```

I'm not yet sure if this is just a connectivity check or if it does something else as well. Responses of `REJECTED` and `OFFLINE` are also possible.
