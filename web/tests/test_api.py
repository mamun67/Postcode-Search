import unittest
from web.api import create_response, Response
import os
from unittest.mock import patch, MagicMock


class TestPostcodeSearch(unittest.TestCase):

    def test_create_response_return_no_match_with_no_geojson_arg(self):
        # Act
        pcode = create_response(None, 'EH111AH')

        # Assert
        self.assertEqual(pcode.status_code, 200, 'Status code should be 200')
        self.assertEqual(pcode.data, b'{"EH111AH": "NO MATCH"}')

    @patch('web.api.Response', autospec=True)
    def test_create_response_returns_geojson(self, mock_response):
        # Act
        mock_response.return_value = MagicMock(mock_response)
        geojson = {
            "crs": {
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::27700"
                },
                "type": "name"
            },
            "properties": {
                "postcode": "FK79RA"
            },
            "geometry": {
                "coordinates": [
                    277531,
                    692837
                ],
                "type": "Point"
            },
            "type": "Feature"
        }
        os.environ["DB_PORT_27017_TCP_ADDR"] = "http://localhost"
        pcode = create_response(geojson, 'EH111AH')

        # Assert
        self.assertIsInstance(pcode, Response)
