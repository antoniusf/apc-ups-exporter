import re

line_regex = re.compile(r"([^:\s]*)\s*:\s*(.*)", re.ASCII)

def parse_float(unit):
    regex = re.compile(r"(\d+(\.\d+)?) {}".format(unit), re.ASCII)

    def do_parse(string):
        result = regex.fullmatch(string)
        if result:
            return float(result.groups()[0])

    return do_parse

def parse_status_flags(flags_hex_string):
    try:
        status_flags = int(flags_hex_string, 16)
    except ValueError:
        return None

    status = {}
    for bit_index, name in zip(range(3, 8),
            ["on_line", "on_battery", "overloaded_output",
             "battery_low", "replace_battery"]):

        status[name] = bool(status_flags & (1 << bit_index))

    return status

parsers = {
    "statflag": ("status", parse_status_flags),
    "linev": ("line_voltage", parse_float("Volts")),
    "loadpct": ("load_percentage", parse_float("Percent")),
    "bcharge": ("battery_charge", parse_float("Percent")),
    "timeleft": ("time_left", parse_float("Minutes")),
    "outputv": ("output_voltage", parse_float("Volts")),
    "battv": ("battery_voltage", parse_float("Volts")),
    "linefreq": ("line_frequency", parse_float("Hz")),
    "tonbatt": ("time_on_batteries", parse_float("Seconds"))
}



def parse_line(line):
    result = line_regex.fullmatch(line)
    if result:
        name, value = result.groups()
        name = name.lower()
        if name in parsers.keys():
            nice_name, parser = parsers[name]
            parsed_value = parser(value)
            if parsed_value is not None:
                return nice_name, parsed_value

def parse_lines(lines):

    values = {}
    for line in lines:
        result = parse_line(line)
        if result:
            name, value = result
            values[name] = value

    return values

def parse_file(filename):
    with open(filename) as f:
        return parse_lines(f.read().split("\n"))
