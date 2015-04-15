# Overview

InfluxDB is an open-source, distributed, time series database.  This charm
is designed to act as a data source for the grafana charm: 
cs:~cherylj/trusty/grafana-0

This charm is a test and should not be used in production.

# Usage

Deploy the grafana charm, and the required influxDB charm with the following:

    juju deploy cs:~cherylj/trusty/grafana-0
    juju deploy cs:~cherylj/trusty/influx-0

Add the relation between the two charms:

    juju add-relation grafana:query influxdb:query

Expose the grafana charm:

    juju expose grafana

You can then access the grafana interface at the public interface shown
from juju status.

# Feeding data into influxDB

The influxDB charm currently has a static port for feeding data into grafana: 8217.
Data should be sent on this port to the influxDB host in the following format:

<metric path> <metric value> <metric timestamp>

The metric path is the series you will select in grafana to graph the data.
