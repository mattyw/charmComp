# Overview

Grafana is a general purpose dashboard and graph composer.  It can be used to
visualize monitoring data for your environment.

This charm is a test and should not be used in production.

# Usage

Deploy the grafana charm, and the required influxDB charm with the following:

    juju deploy cs:~cherylj/trusty/grafana
    juju deploy cs:~cherylj/trusty/influx

Add the relation between the two charms:

    juju add-relation grafana influxdb

Expose the grafana charm:

    juju expose grafana

You can then access the grafana interface at the public interface shown
from juju status.  The following video shows how to generate the graph of
the data: https://youtu.be/7HdwuOWiOEo

# Feeding data into influxDB

The influxDB charm currently has a static port for feeding data into grafana: 8217.
Data should be sent on this port to the influxDB host in the following format:

<metric path> <metric value> <metric timestamp>

The metric path is the series you will select in grafana to graph the data.
