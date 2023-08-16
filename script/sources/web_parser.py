import requests
import json

# Webservice queries should follow the basic format:
# ACTION URL header-name header-value header-name header-value...
def query_web(query):
    headers = {}
    errors = []
    response = None

    # break up query by spaces and iterate through the list
    query_list = query.split()

    # TODO: this assumes correct dropin format; check that indices exist before accessing them
    action = query_list[0].upper()
    url = query_list[1]

    if len(query_list) > 2:
        for i in range(2, len(query_list), 2):
            # would the expected pair be out of bounds?
            if i+1 >= len(query_list):
                errors.append(f"Expected a header value for {query_list[i]}. Attempting to continue without header.")
                continue
            
            headers[query_list[i]] = query_list[i+1]
    
    # currently only supports get and post actions, and only if the post is simple:
    # we currently read the rest of the command as header data, nothing for a body
    if action == "GET":
        response = requests.get(url, headers=headers)
    elif action == "POST":
        response = requests.post(url, headers=headers)
    else:
        errors.append(f"Unknown action {action}. Unable to proceed with request.")

    result = {}

    if response is not None:
        result["response"] = json.loads(response.content)
    if len(errors) > 0:
        result["errors"] = errors

    return result
