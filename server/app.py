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

class Plants(Resource):
    def get(self):
        plant_list= []
        for plant in Plant.query.all():
            plant_list.append(plant.to_dict())
        response = make_response(
            plant_list,
            200,
            {'Content-Type':'application/json'}
        )
        return response
    def post(self):
        if 'name' not in request.form or 'image' not in request.form or 'price' not in request.form:
           return {'message': 'Missing required fields'}, 400
        new_plant = Plant(
            name=request.form.get('name'),
            image=request.form.get('image'),
            price=request.form.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        
        response_body = Plant.query.filter_by(id=new_plant.name).first().to_dict()
        response = make_response(
            response_body,
            201,
            {'Content-Type':'application/json'}
        )
        return response
api.add_resource(Plants, '/plants')
        
        

class PlantByID(Resource):
    def get(self, id):
        response_body =Plant.query.filter_by(id=id).first().to_dict()
        
        response =  make_response(
            response_body,
            200,
            {'Content-Type':'application/json'}
        )
        return response
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run( host='localhost', port=5555, debug=True)
