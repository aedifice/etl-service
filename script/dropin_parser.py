
import re

PARAM = "-- @"
SOURCE = "-- @source "
SINK = "-- @sink "
COMMENT = "-- "

# perform text parsing to transform a dropin txt file into a runnable command
def parse_dropin(file_path):
    desc = ""
    source = None
    sink = None
    parameters = {}
    query = ""
    errors = []

    # read dropin line by line to break apart into usable command
    with open(file_path) as dropin:
        for line in dropin:
            line = line.strip()

            # skip empty lines
            if len(line) == 0:
                continue

            # check for special lines
            if line.startswith(SOURCE):
                source = line.replace(SOURCE, '', 1)
            elif line.startswith(SINK):
                sink = line.replace(SINK, '', 1)
            elif line.startswith(PARAM):
                # we need extra checking on parameters to ensure line is formatted as
                # "-- @parameterName parameterValue"
                param_line = line.replace(PARAM, '', 1)
                param_args = param_line.split(' ', 1)

                if len(param_args) == 2:
                    parameters[param_args[0]] = param_args[1]
                else:
                    errors.append(f"Malformed parameter line. Attempting to exclude '{line}'.")
            elif line.startswith(COMMENT):
                desc += line.replace(COMMENT, '', 1)


            else:
                # check for parameters in the line
                # parameters can currently only be used in regular lines (not source, sink, etc)
                # and will likely be more useful once sql queries become a thing
                for key in parameters.keys():
                    pattern = rf'(\s+|\.|\b|^){key}(\s+|\.|\b|$)'

                    matches = re.finditer(pattern, line)
                    matchlist = []

                    for match in matches:
                        matchlist.append(match)

                    # changing the line will change indices; we must work backward
                    for i in range(len(matchlist)-1, -1, -1):
                        match = matchlist[i]
                        line = line[:match.start()] + \
                            line[match.start():match.end()].replace(key, parameters[key]) + \
                            line[match.end():]
                    

                # what we do with the leftover lines depends on where we are in the dropin
                if (source is not None and sink is None):
                    query = query + line + " "
                elif (source is not None and sink is not None):
                    # TODO: implement sink
                    sink = sink
                else:
                    errors.append(f"Malformed dropin command. Don't know what to do with line '{line}'.")

    # format final parsed command
    command = {"description": desc, "parameters": parameters, "query": query}

    if len(errors) > 0:
        command["errors"] = errors
    if source is not None:
        command["source"] = source
    if sink is not None:
        command["sink"] = sink

    return command