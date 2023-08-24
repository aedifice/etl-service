import os
import json
import requests
from flask import request
from flask_restful import Resource
from dropin_parser import parse_dropin
from sources.web_parser import query_web

DROPIN_DIR = "dropins/"
DEFAULT_SINK = "http://host.docker.internal:3514/etl/"    # this is where we want to send our data

def dropin_list():
    dropins = []

    for dropin in os.listdir(DROPIN_DIR):
        dropins.append(dropin)

    return dropins

class GetHelp(Resource):
    # list available dropin commands
    # these can be used in conjunction with the /etl (RunCommand) endpoint
    def get(self):
        return {"commands": dropin_list()}

class RunCommand(Resource):
    def get(self, command):
        cmd_file = f"{DROPIN_DIR}{command}.txt"

        # check for dropin
        if not os.path.isfile(cmd_file):
            return {"error": f"No {command} dropin found."}

        parsed_cmd = parse_dropin(cmd_file)

        # where does our parsed command say we need to go?
        if "source" not in parsed_cmd:
            return {"error": f"No query source found in {command} dropin."}
        elif parsed_cmd["source"] == "sql":
            # TODO: implement db query
            query_result = ""
        elif parsed_cmd["source"] == "webservice":
            query_result = query_web(parsed_cmd["query"])
        else:
            return {"error": f"Unknown source '{parsed_cmd['source']}' in {command} dropin."}

        parsed_cmd["query_result"] = query_result

        #TODO: send to whatever sink command has set; for now, just use default sink
        filename = command
        if "append" in request.args:
            filename += f"-{request.args['append']}"
        parsed_cmd["filename"] = filename

        response = requests.post(DEFAULT_SINK + filename, json=query_result)
        parsed_cmd["sink_response"] = json.loads(response.content)

        return parsed_cmd
