
# Developing

<!-- TOC -->

- [Developing](#developing)
- [Tests](#tests)
- [Docker](#docker)
	- [Grafana](#grafana)
- [Dependency Management](#dependency-management)

<!-- /TOC -->

# Tests

Running tests:

```
$ pipenv run tests
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

# Docker

The docker environment is principally to supply an integrated Grafana, InfluxDB and Python environment. It's not required for core development.

To start containers: `docker-compose up -d`.

## Grafana

Grafana will be accessible on <http://localhost:3000/> with a default username and password of `admin/admin`.

Enter a shell in the python container with: `docker-compose exec python bash`.

Add a data source of type "InfluxDB" with:

 * URL: `http://influxdb:8086/`
 * Database: `selpi`

The example dashboard (`grafana/electricity.json`) can be imported as per <https://grafana.com/docs/grafana/latest/dashboards/export-import/#importing-a-dashboard>.

# Dependency Management

Install a production dependency with: `pipenv install <package>`.

See: [this Stack Overflow](https://stackoverflow.com/a/46020794/2066278)
