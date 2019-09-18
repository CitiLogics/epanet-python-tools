import pandas as pd

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


def load_calibration(path):
    """
    Loads data from an epanet calibration file
    :param path: the file path
    :return: dict of Pandas Series, each with time-step as index column
    """
    raw_data = {}
    series = {}

    with open(path) as fh:
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



