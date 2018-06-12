# csv-plotter
## Prerequisites

This program is intended to be used as a command line tool. First, you need to install Plotly.
```
sudo apt install python3-pip
sudo pip3 install plotly
```
If you want to generate plots as .png directly, rename `config/config.json.dist` to `config/config.json` and add credentials for your Plotly account. Plotly currently does not support offline image export.
```
{
    "plotly": {
        "username": "TheSecurityExpert",
        "password": "password123"
    }
}
```
Now, let's get plotting! To see a list of options, try the following.
```
python3 runme.py -h
```

## Example Commands

Below are example commands (more complex).

For all directories whose names contains "auto," graph the sum of all fields whose names contain "power" on the same html graph with defined titles, y-axes, and offset.
```
python3 runme.py -d *auto* -c *power* --sum -t "Power Sum Comparison" -y Power -p POWER -o 7 --ymin 20 --ymax 100
```

For all directories whose names contain "ospm," graph "temperature" field on the same html graph with defined titles and y-axes.
```
python3 runme.py -d *ospm* -c temperature -t "Temperature Comparison" -y Temperature -p TEMP --ymin 20 --ymax 100
```

For all directories whose names contain "ospm," graph "core-0" field for all files on the same html graph with defined titles and y-axes.
```
python3 runme.py -d *ospm* -c core-0 -t "Core 0 Frequencies" -y Frequency -p FREQ --ymin 1000 --ymax 2600
```

For all directories whose names contain "ospm," graph "temperature" field for each file as an individual png and output to a custom directory.
```
python3 runme.py -d *ospm* -c temperature -t Temperature -y Temperature -p TEMP -i -I -D plots/TEMP_ospm_drupal
```

For all directories whose names contain "ospm" and all files inside of it whose names contain "drupal," graph the averages of "core0" and "core1," and "core2" and "core3" on the same html plot with defined titles.
```
python3 runme.py -f "*ospm*/*drupal*" -c core-0,core-1;core-2,core-3 --avg -t "Average Core Frequencies" -y Frequency -p FREQ
```

## Plotly HTML Capabilities
These are various useful functions you can do in the generated HTML plots.

**Hide all lines except one:** Double-click the line you want to isolate in the legend.

**Show a line:** Click on a hidden line in the legend.

**Show all lines**: Double click the legend.

**Export as png:** Click the camera icon in the upper right. It will save a PNG of the current state, including hidden lines. NOTE: The legend will be cut off if there are too many items; this is a known bug in Plotly.

**Compare lines on hover:** Click "compare data on hover" in the upper right. This will show data for all lines on hover, as opposed to just one.

**Zoom:** Click and drag diagonally on the graph.

**Limit x-axis:** Click and drag horizontally on the graph.

**Reset zoom/axes:** Double-click the graph or click "reset axes" in the upper right.
