#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Plant

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)


# Routes
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.get_or_404(id)
        data = request.get_json()

        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
        
        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)


# Add routes to API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
