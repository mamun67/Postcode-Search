# Postcode-Search
A Dockerized [Flask-restful](http://flask-restful-cn.readthedocs.io/en/0.3.4/) application to serve postcode GeoJson from a [MongoDB](https://www.mongodb.com/) backend.

Endpoint:

> http://localhost/postcode/eh111at

returns:
```
{
    "crs": {
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::27700"
        },
        "type": "name"
    },
    "properties": {
        "postcode": "EH111AT"
    },
    "geometry": {
        "coordinates": [
            324079,
            672543
        ],
        "type": "Point"
    },
    "type": "Feature"
}
```


## Requirements
To run the application locally you will need to have installed both [Docker](https://docs.docker.com/engine/) and [Docker Compose](https://docs.docker.com/compose/). Compose is a tool for defining and running multi-container Docker applications. This is used to get the Python application, database and HTTP server configured and all talking to each other.

Python scripts have been written in Python 3.5.

## Setup

 1. **Code-Point Open CSV to GeoJson**

	To load this data into MongoDB it must first be convert from CSV to GeoJson format.
	1. Download the [OS Code-Point Open](https://www.ordnancesurvey.co.uk/business-and-government/products/code-point-open.html) zipfile and extract the CSV to a sensible location on your machine.
	2. Place the script `mongo/csv_to_geojson.py`in the same folder as the extracted CSV files and run `python csv_to_gejson.py`. This script requires the [python-geojson](https://github.com/frewsxcv/python-geojson) module installed.
	Once complete there should be a new folder within the CSV directory which contains a GeoJson file for each CSV that exists. e.g. tr.json.


 2. **Load GeoJson files to MongoDB**

	Now we have GeoJson representations for each postcode we are ready to load this data into MongoDB, a NoSQL database. Each file will be loaded as a seperate collection containing a [document for each postcode](http://petermcmillan.com/articles/importing-geojson-data-mongodb).
	1. Clone this repository on your machine.
	2. In the file docker-compose.yaml, change the path of the mapped volume to a folder on your machine. This allows us to access and run 
	3. From a terminal CD into the repo directory and run `docker-compose build`. This should pull down the various docker images required by the application.
	4. Right now we are only interested in the container named `postcodesearch_db`. Check this exists with `docker ps -a`. This command lists all docker containers.
	5. Enter the container with the command `docker exec -i -t <container name> /bin/bash` and use mongoshell to create a postcode database.
	6. Run the script `mongo/file-loop.sh` in the same folder as the GeoJson files. The script iterates over all files with a *.json extension and loads them into a collection of the same filename. 
