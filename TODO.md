<!-- TOC -->

- [Query command](#query-command)
- [Switcher?](#switcher)
- [Reimplement PVO](#reimplement-pvo)
- [Explore OpenEnergyMonitor integration](#explore-openenergymonitor-integration)
- [Logging ... with levels](#logging--with-levels)

<!-- /TOC -->

# Query command

Command to do a raw query, provide an address and length on the CLI and get it back.

# Switcher?

Try writing something that talks to the SP Pro directly over ttyUSB and then listens on a unix socket and allows multiple other programs to talk at once. If we write one that can expose that unix socket over tcp, then SP Link should be able to talk to it, meaning we can run SP Link at the same time as our own monitoring (not possible with select.live).

# Reimplement PVO

# Explore OpenEnergyMonitor integration

OEM looks like a promising place to dump data from the SP PRO (more usable than select.live anyway).

https://openenergymonitor.org

# Logging ... with levels

So I can spam debug statements out to see what's going on.
