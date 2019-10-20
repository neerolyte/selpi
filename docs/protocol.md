# Protocol

The communication protocol with the SP Pro appears to consist of requests for blocks of memory, with knowledge of the structures in that memory to be reimplemented by the requested.

<!-- TOC -->

- [Protocol](#protocol)
- [Memory space](#memory-space)
- [Messages](#messages)
	- [Query](#query)
	- [Example Messages](#example-messages)
		- [Hello](#hello)
- [Authentication](#authentication)

<!-- /TOC -->

# Memory space

Memory is addressed as 2 byte words.

Memory of interest appears to be within the 0xa000 - 0xafff range.

# Messages

## Query

A query consists of:

    TLAA??CC

Where:

 * T is the message type - Q for Query or W for Write
 * L is a byte indicating the number (length) of 2 byte words to return (0x00 will return 1 word).
 * AAAA is a little endian word address (shifting the address by 1 shifts by 2 bytes).
 * CC is a Cyclic Redundancy Check.

A response consists of:

 * TLAAAACC the exact bytes from the query (including CRC).
 * M the requested memory.
 * CC CRC of the query + memory.

It's possible to request between 0-255 bytes of memory, 

## Example Messages

### Hello

Prior to authentication SP LINK sends a request for 0 words from `0xa000` and the SP Pro will respond with the appropriate CRC calculation.

E.g:

```
Query:    0x510000a000009d4b
            TTLLAAAAAAAACCCC
Response: 0x510000a000009d4b0100d819
            TTLLAAAAAAAACCCCMMMMCCCC
```

# Authentication

TODO!

