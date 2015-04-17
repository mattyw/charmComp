# Overview

Use the influxDB injector to inject data into controlling influxDB service.
In its current form, it is used to demonstrate the relation between the
following charms:

	cs:~cherylj/trusty/grafana
	cs:~cherylj/trusty/influxdb

This charm is a test and should not be used in production.

# Usage

After installing the two charms in the overview and relating them, deploy
the influxdb-injecter and relate it with influxDB:

	juju deploy cs:~cherylj/trusty/influxdb-injecter
	juju add-relation influxdb influxdb-injecter

After the relation is added, information is being added to the grafana 
database.  The series name to query to graph the results is 
series-<public hostname for influxdb-injecter>

The following video shows how to generate the graph of the data:
https://youtu.be/7HdwuOWiOEo

