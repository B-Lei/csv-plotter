import os
import sys
import glob
import argparse
from src import CSV
from src import Plotter


def parse_arg_dirfile_list(dirfile_list):
    """
    Looks at either "--dir" or "--file" and determines what to use.
    Uses Unix-style matching (* instead of .*), thanks to glob.
    """
    dirfiles = []
    for dirfile in dirfile_list.split(','):
        found_files = glob.glob(dirfile)
        if not found_files:
            print("{} was not found. Please make certain that this is an existing file. Aborting.".format(dirfile))
            sys.exit(0)
        dirfiles += found_files
    # Make sure no duplicate entries, and in order for idempotency
    return sorted(list(set(dirfiles)))


def get_arguments():
    """
    Set up all options here.
    """
    parser = argparse.ArgumentParser()
    data = parser.add_mutually_exclusive_group(required=True)
    data.add_argument("-d", "--dir", help="directory containing .csv files. Accepts Unix-style wildcards.")
    data.add_argument("-f", "--file", help="comma-separated list of .csv files. Accepts Unix-style wildcards.")
    parser.add_argument("-c", "--cols", help="comma-separated list of columns to plot for each csv. Use semicolons "
                                             "to group columns - operations will be performed on each group. EXAMPLE: "
                                             "\"-c core-[0-9]+;*power -a -m\" will plot 4 lines per csv: min/avg of "
                                             "all cores, and min/avg of all fields ending with \"power.\" Note that "
                                             "you can use Unix-style wildcards and regular expressions (precedence "
                                             "given to Unix-style wildcards).", required=True)
    parser.add_argument("-s", "--sum", help="plot sum of comma-separated fields.", action="store_true")
    parser.add_argument("-a", "--avg", help="plot avg of comma-separated fields.", action="store_true")
    parser.add_argument("-m", "--min", help="plot min of comma-separated fields.", action="store_true")
    parser.add_argument("-M", "--max", help="plot max of comma-separated fields.", action="store_true")
    parser.add_argument("-i", "--indiv", help="generate individual plot for each .csv.", action="store_true")
    parser.add_argument("-o", "--offset", help="vertically shift all lines by integer value.", default=0)
    parser.add_argument("-S", "--scale", help="multiplies all y-values by this integer value.", default=1)
    parser.add_argument("-D", "--out_dir", help="output directory for plots. Default is \"plots.\"", default="plots")
    parser.add_argument("-p", "--prefix", help="prefix string used for all generated files, e.g. PREFIX_test.html")
    parser.add_argument("-n", "--name", help="filename of generated plot - only works when a single plot is generated, "
                                             "i.e. not using --indiv.")
    parser.add_argument("-t", "--title", help="title of plot.")
    parser.add_argument("-y", "--y_title", help="title of y-axis.")
    parser.add_argument("-x", "--x_title", help="title of x-axis.")
    parser.add_argument("-e", "--extend_disable", help="disable extension of shorter lines.", action="store_true")
    parser.add_argument("-b", "--autobar", help="display fourth and subsequent lines as bars. Useful when displaying "
                                                "many lines at once.", action="store_true")
    parser.add_argument("-B", "--bar", help="Display everything using bars.", action="store_true")
    parser.add_argument("-u", "--unique_colors", help="use unique colors for each line, even within the same CSV.",
                        action="store_true")
    parser.add_argument("-I", "--image", help="exports as PNG - REQUIRES INTERNET ACCESS. You may also manually export "
                                              "as PNG using the button in the HTML plot, but legend will be cut off if "
                                              "there are too many items.", action="store_true")
    parser.add_argument("--xmin", help="minimum x-value to use in plot.")
    parser.add_argument("--xmax", help="maximum x-value to use in plot.")
    parser.add_argument("--ymin", help="minimum y-value to use in plot.")
    parser.add_argument("--ymax", help="maximum y-value to use in plot.")
    parser.add_argument("--xaxis", help="col to use as x-axis.")
    return parser.parse_args()


def main():
    # STEP 1: Parse args
    args = get_arguments()

    # STEP 2: Get a list of CSV objects.
    csv_list = []
    if args.dir:
        for directory in parse_arg_dirfile_list(args.dir):
            for fname in os.listdir(directory):
                if fname.endswith(".csv"):
                    csv_list.append(CSV(os.path.join(directory, fname), args))
    else:
        for fname in parse_arg_dirfile_list(args.file):
            if fname.endswith(".csv"):
                csv_list.append(CSV(fname, args))
    if len(csv_list) == 0:
        print("CSV list is empty. Are you passing a valid directory with \"-d\" flag, or file with \"-f\" flag?")
        print("\nAborting.")
        return

    # STEP 3: Create a Plotter and generate plot(s)
    if args.indiv:
        args.dir = None
        xaxis = args.xaxis if args.xaxis else None
        xmin = Plotter.get_x_min(csv_list, xaxis)
        xmax = Plotter.get_x_max(csv_list, xaxis)
        ymin = Plotter.get_y_min(csv_list, xaxis) + args.offset
        ymax = Plotter.get_y_max(csv_list, xaxis) + args.offset
        for csv in csv_list:
            args.file = csv.fname
            plot = Plotter([csv], args, xmin, xmax, ymin, ymax)
            plot.generate_plot()
    else:
        plot = Plotter(csv_list, args)
        plot.generate_plot()


if __name__ == "__main__":
    main()
