from flask_restful import Resource
from flask import Response
from search import postcode_search
from json import dumps


class PostcodeSearch(Resource):
    """
    /postcode/
    """

    def get(self, postcode):
        """
        Get GeoJson Feature for a UK postcode.
        :param postcode: UK postcode string
        :return: response
        """
        postcode_geojson = postcode_search(postcode)
        return create_response(postcode_geojson, postcode)


def create_response(geojson, postcode):
    """
    Create the response. Either a postcode or no match message.
    :param geojson: GeoJson object
    :param postcode: postcode string
    :return: Json object
    """
    if geojson is not None:

        # Create Json response if match exists

        resp = Response(geojson,
                        status=200,
                        mimetype='application/json')
    else:
        # Failed postcode match response
        js_no_match = dumps({postcode: "NO MATCH"})
        resp = Response(js_no_match,
                        status=200,
                        mimetype='application/json')
    return resp

