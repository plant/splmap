# splmap

Create a heatmap of sound pressure levels given various SPL log formats and a GPX track.

# usage

	python splmap.py sample.csv sample.cpx

where `sample.csv` is your SPL data, which is currently of one specially-formatted CSV file with rows formatted as follows:
	
	YY:MM:DD,HH:MM:SS.MS,AVGSPL,PEAKSPL

Data will be modified such that each row of the SPL file will be assigned a latitude and longitude value, linearly interpolated from the times for each `<trkpt>` of the GPX file. Finally, rows with the same latitude and longitude are consolidated such that the `AVGSPL` and `PEAKSPL` are averaged across all rows of the same location.

# todo

- Get rid of hideous manual HTML output and have splmap.py generate a JSON file which is loaded by a single web page.
- Support a slider for time of day.
- Support more types of SPL data, especially those produced by commercial devices. Currently, these files are formatted according to those provided by the iPhone apps created by [Skypaw](http://www.skypaw.com/).
