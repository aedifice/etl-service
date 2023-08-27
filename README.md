# ETL Dropin Service

This Python Flask web service offers simple ETL functionality to parse and run dropin commands. Results are then sent over to a sink location.

## Dropin commands

Dropin commands are meant to make it easy for anyone to add queries without needing to understand the underlying mechanism for running them. Users will, however, need to format dropin commands correctly. Example usage is as follows.

**Retrieve data from APIs**
```
-- Description of command
-- @source webservice
GET https://www.example.com/api?filter=someFilter&sort=field
header-name header-value
```

**Retrieve data from a MySQL database**
```
-- Description of command
-- @source mysql
SELECT *
FROM table;
```

## Sources

In true ETL spirit, data should be able to be retrieved from multiple sources. The initial version of this service is able to parse simple web queries and connect with a MySQL database. Future iterations may add more complex web queries, or other additional sources.

Each source will have its own dropin command format and its own command parser that takes over where the general dropin parser leaves off.

## Using the service

Note that this service is currently configured to send results to another web service instead of a true data warehouse and will post its results to a path starting with the `DEFAULT_SINK` constant. See associated [example data sink](https://github.com/aedifice/etl-sink).

To utilize the MySQL connection option, make sure to update the `config/etlsql.env.template` file with your configuration details and save without the `.template` extension.

### Running the service

This service encapsulates its requirements in a Docker container. So, while you don't need to install Python requirements directly, you at least need to be able to run [Docker](https://www.docker.com/) commands.

To build the Docker image, execute:
`./build-container.sh`

To start a container based on the image, execute:
`./run-container.sh`

Alternatively, you can copy the Docker commands from the Shell scripts and run them from the Dockerfile's base directory.

Starting the container will start up the web service on `127.0.0.1:3513`

### Using Docker Compose

For testing purposes, there is also the option to start up the service with an attached MySQL instance using Docker compose. To do so, run: `docker compose up -d`

And run `docker compose down` when done.

### Using the service's endpoints

Once the service is running, use the "Help" endpoint to retrieve a list of available dropin commands.
```
GET localhost:3513/help
```

The "Run Command" endpoint will parse the specified dropin command and attempt to run it, sending any results to the default data sink location.
```
GET localhost:3513/etl/web_example
```

An "append" argument can be added to this request to modify the "file name" that gets sent to the data sink along with the results. For example, the request `localhost:3513/etl/web_example?append=extra-extension` will suggest storing results under a file name of "web_example-extra-extension" to the data sink.

## Future work

Lots more fun features could be added to this service. Some ideas include:
* Add a NoSQL source and dropin type
* Focus more on the transform step: allow dropin commands to specify a default format for returned data (currently assumes JSON) or allow a request parameter to override the format
* Allow the dropin to specify its own data sink location
* Allow a wider variety of web requests (currently assumes a basic REST GET request)
* Generally make parsing more forgiving
