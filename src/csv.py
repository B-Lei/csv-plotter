import os
import re
import sys
import fnmatch


class CSV:
    """
    Represents a SINGLE csv file as a dictionary of values for each column.
    EXAMPLE USAGE: test_csv.data["core-0"]
    """
    def __init__(self, fname, args):
        self.fname = fname
        self.data = self.parse_csv(fname, args.cols, args.xaxis)
        # Get the number of rows for first arbitrary value
        self.numrows = len(next(iter(self.data.values())))
        self.handle_col_ops(args)

    def parse_csv(self, fname, cols, xaxis):
        """
        Parses relevant and unique columns into data structure. Does NOT account for column operations.
        EXAMPLE: In "-c core.* --sum," this would store all cols beginning with "core," NOT a single col of their sum.
        """
        def valid_row(split_row):
            return split_row[0] and not split_row[0].startswith('#')
        if not os.path.exists(fname) or not os.path.isfile(fname):
            print("{} does not exist or is not a file. Aborting.".format(fname))
            sys.exit(0)
        data = dict()
        with open(fname) as file:
            # Get header. Skip comments and whitespace.
            line_num = 1
            header = [x.strip() for x in file.readline().split(',')]
            while not valid_row(header):
                header = [x.strip() for x in file.readline().split(',')]
                line_num += 1
            fields_to_use = self.parse_arg_cols_list(cols, header)
            if xaxis:
                fields_to_use.append(xaxis)
            for field in fields_to_use:
                data[field] = []
            # Parse data into dictionary. Only parse columns that were specified.
            for row in file:
                line_num += 1
                split = row.split(',')
                if len(split) != len(header) or not valid_row(split):  # Skip rows that don't match with header
                    print("{}: skipping row at line {}".format(fname, line_num))
                    continue
                row_data = [float(x.strip()) for x in split]
                for num, value in enumerate(row_data):
                    if header[num] in fields_to_use:
                        data[header[num]].append(value)
            return data

    @staticmethod
    def parse_arg_cols_list(cols, search_list):
        """
        Looks at "--cols" argument to determine what cols to save.
        Supports both Unix-style and regex matching.
        """
        fields = re.split('[;,]', cols)
        fields_to_use = []
        for field in fields:
            regex = fnmatch.translate(field)
            matching_fields = list(filter(re.compile(regex).match, search_list))
            # If Unix-style matching doesn't work, try regex
            if len(matching_fields) == 0:
                matching_fields = list(filter(re.compile("^{}$".format(field)).match, search_list))
            if len(matching_fields) == 0:
                print("\"{}\" not found in CSV headers. Aborting.".format(field))
                sys.exit(0)
            fields_to_use += matching_fields
        # Make sure no duplicate entries, and in order for idempotency
        return sorted(list(set(fields_to_use)))

    def handle_col_ops(self, args):
        """
        Converts saved columns to "combined" columns based on col operations (sum, avg, min, max).
        EXAMPLE: In "-c core.* -s," this would take existing cols and combine them into a single col of their sums.
        """
        # Returns a dictionary key for operated columns
        def name(operation, fields):
            return "{}_{}".format(operation, "/".join(fields))
        # If there are no operations, then data is already good to go. Semicolons don't matter.
        if not args.sum and not args.avg and not args.min and not args.max:
            return
        stored_field_names = [name for name, vals in self.data.items()]
        # For each colgroup (separated by semicolon);
        colgroups = args.cols.split(';')
        for colgroup in colgroups:
            cols = []
            raw_cols = colgroup.split(',')
            matching_fields = self.parse_arg_cols_list(colgroup, stored_field_names)
            cols += [self.data[x] for x in matching_fields]
            # No need to operate on single columns
            if len(cols) == 1:
                continue
            # Now, perform operation on cols
            for i in range(0, len(cols[0])):
                row_vals = [x[i] for x in cols]
                if args.sum:
                    if name('sum', raw_cols) not in self.data:
                        self.data[name('sum', raw_cols)] = []
                    self.data[name('sum', raw_cols)].append(sum(row_vals))
                if args.avg:
                    if name('avg', raw_cols) not in self.data:
                        self.data[name('avg', raw_cols)] = []
                    self.data[name('avg', raw_cols)].append(sum(row_vals) / float(len(row_vals)))
                if args.min:
                    if name('min', raw_cols) not in self.data:
                        self.data[name('min', raw_cols)] = []
                    self.data[name('min', raw_cols)].append(min(row_vals))
                if args.max:
                    if name('max', raw_cols) not in self.data:
                        self.data[name('max', raw_cols)] = []
                    self.data[name('max', raw_cols)].append(max(row_vals))
        # Update data - add operated columns, remove individual columns
        filtered_data = dict()
        for key, value in self.data.items():
            used_individually = (len([x for x in args.cols.split(';') if x == key]) != 0) or key == args.xaxis
            if used_individually or key.startswith(("sum", "avg", "min", "max")):
                filtered_data[key] = value
        self.data = filtered_data
