from json import dumps
from bson import json_util
from geojson import crs, is_valid, loads
from pymongo import MongoClient


def postcode_search(postcode):
    """
    Returns GeoJson Feature for postcode coordinates
    :param postcode: Postcode string
    :return: Postcode geojson
    """
    postcode_clean = str(postcode).replace(' ', '')

    # Find the name of the postcode collection
    if postcode_clean[1].isdigit():
        mongo_collection = str(postcode_clean[:1])
    else:
        mongo_collection = str(postcode_clean[:2])
    # Build and return GeoJson
    geojson_obj = build_geojson(mongo_collection, postcode_clean)
    if validate_geojson(geojson_obj):
        return geojson_obj
    else:
        return None


def build_geojson(collection_name, postcode):
    """
    Create a GeoJson feature and validate
    :param collection_name:
    :param postcode: postcode string
    :return: GeoJson
    """
    feature = get_json_from_mongodb(collection_name, postcode)
    if feature is not None:
        coord_ref = crs.Named(properties={'name': 'urn:ogc:def:crs:EPSG::27700'})
        # Remove mongodb ID
        del feature['_id']
        # Add CRS
        feature['crs'] = coord_ref
        # Create json
        json_str = dumps(feature,
                         default=json_util.default,
                         indent=4,
                         separators=(',', ': '))
        return json_str


def validate_geojson(geojson):
    """
    Validate string is GeoJson.
    :param geojson: GeoJson string
    :return: bool
    """
    try:
        if is_valid(loads(geojson))['valid'].lower() == 'yes':
            return True
        else:
            return False
    except:
        return False


def get_json_from_mongodb(collection_name, postcode):
    """
    Query mongodb for postcode and create geojson response object.
    :param collection_name: Name of mongo collection
    :param postcode: postcode string
    :return: flask response json
    """
    client = MongoClient()
    db = client.postcodes
    collection = db[str(collection_name)]
    result = collection.find_one({"properties.postcode": postcode.upper()})
    print(result)
    return result
