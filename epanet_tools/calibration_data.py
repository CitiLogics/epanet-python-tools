import pandas as pd
import io

class CalibrationLine:
    def __init__(self, line, default_location):
        """
        parse the line, and construct the object
        :param line: a line of text from a calibration file
        """
        self.value = None
        self.time = None
        self.location = default_location
        self.valid = False
        # check for line type: may be string or binary encoding...
        if isinstance(line, bytes):
            line = line.decode('utf8')
        fragments = line.partition(';')
        self.has_comment =  len(fragments) > 2
        self.comment = fragments[2] if self.has_comment else ''
        data = fragments[0]
        components = data.split()
        count = len(components)
        if count == 3:
            self.location = components[0]
            self.time = float(components[1]) * 3600  # we want seconds
            self.value = float(components[2])
            self.valid = True
        elif count == 2:
            self.time = float(components[0]) * 3600
            self.value = float(components[1])
            self.valid = (self.location is not None)


def load_calibration(file):
    """
    Loads data from an epanet calibration file
    :param file: the file path or a readable stream
    :return: dict of Pandas Series, each with time-step as index column
    """
    raw_data = {}
    series = {}
    fh = None

    if isinstance(file, str):
        fh = open(file)
    elif isinstance(file, io.IOBase):
        fh = file

    if fh:
        this_location = None
        for cnt, line in enumerate(fh):
            # parse the line
            data = CalibrationLine(line, this_location)
            this_location = data.location
            if data.valid:
                if data.location not in raw_data:
                    raw_data[data.location] = []
                raw_data[data.location].append((data.time, data.value))
        # done parsing
        for location, data in raw_data.items():
            series[location] = pd.Series([i[1] for i in data], index=[i[0] for i in data])

    return series



