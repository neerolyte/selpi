# Protocol

The communication protocol with the SP Pro appears to consist of requests for blocks of memory, with knowledge of the structures in that memory to be reimplemented by the requested.

<!-- TOC -->

- [Protocol](#protocol)
- [Memory space](#memory-space)
- [Querying memory](#querying-memory)
- [Example Messages](#example-messages)
	- [Hello](#hello)
- [Authentication](#authentication)

<!-- /TOC -->

# Memory space

Memory is addressed as 2 byte words.

Memory of interest appears to be within the 0xa000 - 0xafff range.

# Querying memory

A query consists of:

    QLAARRCC

Where:

 * Q is a literal Q (0x51 in hex) - assumed to be for "query"
 * L is a byte indicating the number (length) of 2 byte words to return.
 * AA is a little endian word address (shifting the address by 1 shifts by 2 bytes).
 * RR appears to always be null (0x0000) and is assumed to be reserved.
 * CC is a Cyclic Redundancy Check.

A response consists of:

 * the exact bytes from the query (including CRC)
 * the requested memory
 * two unexplained bytes
 * CRC of the query+memory

It's possible to request between 0-255 bytes of memory, 

# Example Messages

## Hello

Prior to authentication SP LINK sends a request for 0 words from `0xa000` and the SP Pro will respond with the appropriate CRC calculation.

 * `Query:    0x510000a000009d4b`
 * `Response: 0x510000a000009d4b0100d819`

# Authentication

TODO!

