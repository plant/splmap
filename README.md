# splmap

Create a heatmap of sound pressure levels given various SPL log formats and a GPX track.

# usage

(requires [numpy](http://www.numpy.org/))

	$ python splmap.py sample.csv sample.gpx > sample.html

where `sample.csv` is your SPL data, which is currently of one specially-formatted CSV file with rows formatted as follows (in local time):
	
	YY:MM:DD,HH:MM:SS.MS,AVGSPL,PEAKSPL

Data will be modified such that each row of the SPL file will be assigned a latitude and longitude value, linearly interpolated from the times for each `<trkpt>` of the GPX file. Finally, rows with the same latitude and longitude are consolidated such that the `AVGSPL` and `PEAKSPL` are averaged across all rows of the same location.

Hint: I am currently using [GPX Master+](https://itunes.apple.com/us/app/gpx-master+/id414297402?mt=8) and [Multi Measures](https://itunes.apple.com/us/app/multi-measures-all-in-1-measuring/id354112909?mt=8) on my iPhone.
# bug(s)

1. I think the Heatmap Layer of the Google Maps API adds the weights of nearby points as you zoom out, which means these heatmaps are sort of useless as of yet. I need to find a way to average rather than add.

# todo

1. A legend. Derp.
2. Get rid of hideous manual HTML output and have splmap.py generate a JSON file which is loaded by a single web page.
3. Support a slider for time of day.
4. Support more types of SPL data, especially those produced by commercial devices.
5. Different, more ecolically relevant noise metrics.
6. Fancy interface tools, e.g. being able to select a region and see a timeline of the various noise metrics over time, averaged over all points in the region.
7. Web service.
