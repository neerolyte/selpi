<!-- TOC -->

- [Switcher?](#switcher)
- [Lock deps](#lock-deps)
- [Stats](#stats)

<!-- /TOC -->

# Switcher?

Try writing something that talks to the SP Pro directly over ttyUSB and then listens on a unix socket and allows multiple other programs to talk at once. If we write one that can expose that unix socket over tcp, then SP Link should be able to talk to it, meaning we can run SP Link at the same time as our own monitoring (not possible with select.live).

# Lock deps

How do we lock deps correctly with python3 composer/npm style (virtual envs?)?

# Stats

Write basic utiltiy to dump all known stats to stdout and exit.