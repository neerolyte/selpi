# Selectronic SP Pro 2 Serial Protocol

The querying side of the protocol appears to be based around querying for a number of bytes of memory.

The host will issue a query that begins with `Q` followed by the number words (2 bytes) wanted (encoded in a single byte) and an address. E.g `0xf101a028` is a `Q` followed by a 1 and is asking for one word at address `0xa028`.