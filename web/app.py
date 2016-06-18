from flask import Flask
from flask_restful import Api

from api import PostcodeSearch

app = Flask(__name__)
api = Api(app)

api.add_resource(PostcodeSearch, '/postcode/<string:postcode>', endpoint='search')

if __name__ == '__main__':
    # handler = RotatingFileHandler('postcode_requests.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    app.run(debug=True)
