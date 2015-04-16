# Overview

Use the influxDB injector to inject data into controlling influxDB service.
In its current form, it is used to demonstrate the relation between the
following charms:

	cs:~cherylj/trusty/grafana-0
	cs:~cherylj/trusty/influxdb-0

This charm is a test and should not be used in production.

# Usage

After installing the two charms in the overview and relating them, deploy
the influxdb-injecter and relate it with influxDB:

	juju deploy cs:~cherylj/trusty/influxdb-injecter-0
	juju add-relation influxdb influxdb-injecter

After the relation is added, information is being added to the grafana 
database.  The series name to query to graph the results is 
series-<public hostname for influxdb-injecter>

