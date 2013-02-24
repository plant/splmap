from sys import argv

import numpy as np
import xml.dom.minidom as minidom
import time
import datetime
import dateutil.parser

def unique_rows(a):
    '''Return only unique rows from an array.
        a: np.array
            input array'''

    return np.array([np.array(x) for x in set(tuple(x) for x in a)])

def gpx2array(gpx):
	rows = []
	points = gpx.getElementsByTagName("trkpt")

	for point in points:
		lat = float(point.getAttribute('lat'))
		lon = float(point.getAttribute('lon'))
		ptime = point.getElementsByTagName("time")[0].firstChild.nodeValue
		ptime = time.mktime(dateutil.parser.parse(ptime).timetuple())
		ptime -= time.altzone

		rows.append([lat, lon, ptime])

	return np.array(rows)

def spl2array(spl):
	rows = []

	for row in spl[1:]:
		avg, peak = float(row[2]), float(row[3])
		year, month, day = [int(t) for t in row[0].split(':')]
		hour, minute, secondfloat = [float(t) for t in row[1].split(':')]
		
		second = int(secondfloat)
		microsecond = int((secondfloat - second) * 1E6)

		ptime = datetime.datetime(
			year, month, day, 
			int(hour), int(minute), second, microsecond,
		).isoformat()

		ptime = time.mktime(dateutil.parser.parse(ptime).timetuple())

		rows.append([avg, peak, ptime])

	return np.array(rows)

def splcoords(spl, gpx):
	# [avg, peak, ptime, lat, lon]

	newspl = np.zeros((spl.shape[0], spl.shape[1] + 2))
	newspl[:,:3] = spl

	newspl[:,3] = np.interp(spl[:,2], gpx[:,2], gpx[:,0])
	newspl[:,4] = np.interp(spl[:,2], gpx[:,2], gpx[:,1])
	
	return newspl

def consolidatespl(spl):
	# [avg, peak, lat, lon, "lat lon"]

	newspl = np.zeros(spl.shape, dtype=np.object_)
	newspl[:,:4] = spl[:,(0,1,3,4)]
	
	newspl[:,-1] = np.array(['%f %f' % (r[2], r[3]) for r in newspl], dtype=np.object_)
	uniquelatlon = np.unique(newspl[:,-1])

	for latlon in uniquelatlon:
		indices = newspl[:,-1] == latlon

		lat, lon = [float(l) for l in latlon.split(' ')]
		newspl[indices,2] = lat
		newspl[indices,3] = lon

		for i in [0, 1]:
			newspl[indices,i] = np.mean(newspl[indices,i])
	
	# [avg, peak, lat, lon]
	return unique_rows(np.array([[float(i) for i in row[:4]] for row in newspl]))

def heatmaphtml(spl):
	avglat, avglon = np.mean(spl[:,2]), np.mean(spl[:,3])

	print '	<html>'
	print '		<head>'
	print '			<title>SPL Heatmap</title>'
	print '			<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=visualization"></script>'
	print '			<script>'
	print '				var map, pointarray, heatmap;'
	print '				var spldata=['

	print ',\n'.join([
		'					{location: new google.maps.LatLng(%f, %f), weight: %f}' % (r[2], r[3], r[0])
	for r in spl])

	print '				];'

	print '				function initialize() {'
	print '					var mapOptions = {'
	print '						zoom: 13,'
	print '						center: new google.maps.LatLng(%f, %f),' % (avglat, avglon)
	print '						mapTypeId: google.maps.MapTypeId.SATELLITE'
	print '					};'

	print '					map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);'
	print '					heatmap = new google.maps.visualization.HeatmapLayer({data: spldata});'
	print '					heatmap.setMap(map);'
	print '				}'

	print '			</script>'
	print '		</head>'
	print '		<body onload="initialize()">'
	print '			<div id="map_canvas" style="height: 100%; width: 100%; margin: 0; padding: 0"></div>'
	print '		</body>'
	print '	</html>'

spl = spl2array(np.genfromtxt(argv[1], delimiter=',', dtype=str))
gpx = gpx2array(minidom.parse(argv[2]))

spl = splcoords(spl, gpx)
newspl = consolidatespl(spl)

heatmaphtml(newspl)

