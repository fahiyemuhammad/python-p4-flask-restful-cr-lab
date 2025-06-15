#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):

        return {"Success": "Hello Welcome to the plant REST API"},200
    
api.add_resource(Home, '/')    
    

class Plants(Resource):
    def get(self):
        plants_dict = [ plant.to_dict() for plant in Plant.query.all()]

        if plants_dict:
            return plants_dict,200
        else:
            return {"error": "Plant not found"}, 404
        
    def post(self):

        data = request.get_json()
        try:
            new_plant = Plant(
                name=data["name"],
                image=data["image"],
                price= float(data["price"]),
            )
        except (KeyError, TypeError, ValueError):
            return {"error": "Invalid input"}, 400    

        db.session.add(new_plant)
        db.session.commit()

        return new_plant.to_dict(), 201

api.add_resource(Plants, '/plants')    

        


class PlantByID(Resource):
    def get(self,id):
        plant = Plant.query.filter_by(id=id).first()

        if plant:
            return plant.to_dict(),200
        else:
            return {"error": "Plant not found"}, 404

        
    
api.add_resource(PlantByID, '/plants/<int:id>') 

       

if __name__ == '__main__':
    app.run(port=5555, debug=True)
