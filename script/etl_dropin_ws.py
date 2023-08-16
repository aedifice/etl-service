from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from etl_endpoints import RunCommand, GetHelp

# initialize web service!
if __name__ == '__main__':
    # Flask setup
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    # add service's endpoints; these are the routes that are surfaced for use
    api.add_resource(RunCommand, '/etl/<string:command>')
    api.add_resource(GetHelp, '/help')

    # start things up on localhost:3513
    app.run(host='0.0.0.0', port=3513)  
