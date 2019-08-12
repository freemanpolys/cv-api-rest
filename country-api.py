from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

countryModel = api.model('Country', {
    'id': fields.Integer,
    'name': fields.String,
    'town': fields.String
})
class Country(object):
    def __init__(self,name,town):
        self.id = 1
        self.name = name
        self.town = town

countries = []
countries.append(Country("Senegal","Dakar"))

@api.route("/countries")
class CountryResoure(Resource):
    @api.marshal_with(countryModel, envelope='result')
    def get(self):
        return countries
    
    @api.expect(countryModel)
    @api.marshal_with(countryModel, envelope='result')
    def post(self):
        country = Country(api.payload["name"],api.payload["town"])
        country.id = len(countries) + 1
        countries.append(country)
        return country

@api.route("/countries/<int:id>")
class CountryWithIdResoure(Resource):
    @api.marshal_with(countryModel, envelope='result')
    def get(self,id):
        for country in countries:
            if country.id == id:
                return country
        api.abort(404, "Country {} doesn't exist".format(id))

    def delete(self,id):
        for country in countries:
            if country.id == id:
                countries.remove(country) 
        return '', 204

    @api.marshal_with(countryModel, envelope='result')
    def put(self,id):
        for country in countries:
            if country.id == id:
                #delete old country value 
                countries.remove(country)
                country.name = api.payload["name"]
                country.town = api.payload["town"]
                country.id = id
                #append new country value
                countries.append(country)
        return country        

if __name__ == '__main__':
    app.run(debug=True)