# TODO

 * Try to make class structure that makes sense - https://app.diagrams.net/#G1ijbtordtl1b8AdnVeJv9wsaGD_S4Qpe6
 * rename `Data` to `Bytes`
 * Convert the portion of `Variable` that knows the memory range and raw value to use `Bytes`
 * Add `Metric` which converts a SP Pro memory `Variable` in to an exported metric
 * Add `exporter` command that runs forever updating metrics when required
