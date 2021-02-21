 * add to grafana dashboard:
   * generator power
   * energy
     * generator daily
     * solar daily
     * load daily
   * time to go
   * battery
	 * doco soc cut out at 25% and how to change
   * more temperatures
   * try to use grafana variables to set soc cut out and battery kWh
 * get influxdb data aging working
 * try splitting things like StatOfChargeShutdownSoC to another influx measurement that updates slower (like hourly)
