[PREREQUISITES]

In order to use this program, we need to install Plotly.
1. sudo apt install python3-pip
2. sudo pip3 install plotly

Now, you can invoke the program. To see a list of options, try:
python3 runme.py -h


[EXAMPLE COMMANDS]

Below are example commands (more complex).

1. For each file in directory whose name contains "auto":
   Sum all fields containing "power" and plot on the same html graph, with defined titles, y-axes and offset of +7.
python3 runme.py -d *auto* -c *power* --sum -t "Power Sum Comparison" -y Power -p POWER -o 7 --ymin 20 --ymax 100

2. For each file in directory whose name contains "ospm":
   Plot Temperature on the same html graph with defined titles and y-axes.
python3 runme.py -d *ospm* -c temperature -t "Temperature Comparison" -y Temperature -p TEMP --ymin 20 --ymax 100

3. For each file in directory whose name contains "ospm":
   Plot Core-0 on the same html graph with defined titles and y-axes.
python3 runme.py -d *ospm* -c core-0 -t "Core 0 Frequencies" -y Frequency -p FREQ --ymin 1000 --ymax 2600

4. For each file in directory whose name contains "ospm":
   Plot Temperature on individual png graph with defined titles, output to custom dir.
python3 runme.py -d *ospm* -c temperature -t Temperature -y Temperature -p TEMP -i -I -D plots/TEMP_ospm_drupal

5. For each file whose name contains "drupal" in the directory whose name contains "ospm":
   Plot Avg Freq of core0+core1 and core2+core3 on same html plot with defined titles.
python3 runme.py -f "*ospm*/*drupal*" -c core-0,core-1;core-2,core-3 --avg -t "Average Core Frequencies" -y Frequency -p FREQ


[HTML PLOT CAPABILITIES]

These are various useful functions you can do in the generated HTML plots.

1. HIDE ALL LINES EXCEPT ONE
Double-click the line you want to isolate in the legend.

2. SHOW A LINE
Click on a hidden line in the legend.

2. SHOW ALL LINES
Double click the legend.

3. EXPORT PNG
Click the camera icon in the upper right. It will save a PNG of the current state, including hidden lines.
NOTE: The legend will be cut off if there are too many items; this is a known bug in Plotly.

4. COMPARE LINES ON HOVER
Click "compare data on hover" in the upper right. This will show data for all lines on hover, as opposed to just one.

5. ZOOM
Click and drag diagonally on the graph.

6. LIMIT X-AXIS
Click and drag horizontally on the graph.

7. RESET ZOOM / AXES
Double-click the graph or click "reset axes" in the upper right.