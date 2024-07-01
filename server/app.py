# #!/usr/bin/env python3
# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, make_response, jsonify
# from flask_restful import Api, Resource
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)


# @app.route("/")
# def home():
#     return 'PIZZAS, RESTURANTS, RESTURANT_PIZZAS'

# @app.route("/restaurants", methods=["GET"])
# def get_restaurants():
#     allrestaurants = Restaurant.query.all()
#     restaurants = []
#     for restaurant in allrestaurants:
#         restaurant.dict={
#             'id': restaurant.id,
#             'name': restaurant.name,
#             'address': restaurant.address,
#             'pizzas': [pizza.name for pizza in restaurant.pizzas]
#         }
#         restaurants.append(restaurant.dict)
#     return make_response(jsonify(restaurants), 200)

# @app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
# def restaurants_operations():
#     restaurant = Restaurant.query.filter_by(id=id).first()
#     if request.method == 'GET':
#         if restaurant:
#             pizzas = []
#             for restaurant_pizza in RestaurantPizza.query.filter_by(restaurant_id = id).all():
#                 for pizza in pizza.query.filter(id=restaurant_pizza.pizza_id):
#                     pizza_dict = {
#                         'id': pizza.id,
#                         'name': pizza.name,
#                         'ingredients': pizza.ingredients,
#                     }
#                 pizzas.append(pizza_dict)
#             if request.method == 'GET':
#                 restaurant.dict = {
#                     'id': restaurant.id,
#                     'name': restaurant.name,
#                     'address': restaurant.address,
#                     'pizzas': pizzas
#                 }
#             return make_response(jsonify(restaurant.dict), 200)
#         else:
#             return make_response(jsonify({'error': 'Restaurant not found'}), 404)
#     elif request.method == 'DELETE':
#         if restaurant:
#             restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id = id).all()
#             for restaurant_pizza in restaurant_pizzas:
#                 db.session.delete(restaurant_pizza)
#             db.session.delete(restaurant)
#             db.session.commit()
#             response = {"":""}
#             return make_response(response)
#         else:
#             return make_response(jsonify({'error': 'Restaurant not found'}), 404)

# @app.route('/pizzas', methods=['GET'])
# def get_pizzas():
#     allpizzas = Pizza.query.all()
#     pizzas = []
#     for pizza in allpizzas:
#         pizza.dict = {
#             'id': pizza.id,
#             'name': pizza.name,
#             'ingredients': pizza.ingredients,
#         }
#         pizzas.append(pizza.dict)
#     return make_response(jsonify(pizzas), 200)

# @app.route('/restaurant_pizzas', methods=['POST'])
# def add():
#     try:
#         data = request.get_json()
#         new_rp = RestaurantPizza(
#             price = data['price'],
#             restaurant_id = data['restaurant_id'],
#             pizza_id = data['pizza_id']
#         )
#         db.session.add(new_rp)
#         db.session.commit()

#         pizza = Pizza.query.filter_by(id = new_rp.pizza_id).first()
#         pizza_dict = {
#             'id': pizza.id,
#             'name': pizza.name,
#             'ingredients': pizza.ingredients,
#         }
#         return make_response(jsonify(pizza_dict), 200)
#     except ValueError as e:
#         return make_response(jsonify({"error": str(e)}), 400)
                


# if __name__ == "__main__":
#     app.run(port=5555, debug=True)


#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,json,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"
# restaurant ROUTES
@app.route("/restaurants",methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{"id": restaurant.id,"name": restaurant.name,"address": restaurant.address}for restaurant in restaurants])
@app.route("/restaurants/<int:id>",methods=["GET"])
def get_restaurant(id):
    restaurant=Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return {"error": "Restaurant not found"}, 404
    return jsonify({"id": restaurant.id,"name": restaurant.name,"address": restaurant.address})
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant=Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404
    db.session.delete(restaurant)
    db.session.commit()
    return {"message": "Restaurant deleted successfully"}
# pizza ROUTES
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{"id":pizza.id,"name":pizza.name,"ingredients":pizza.ingredients} for pizza in pizzas])
@app.route("/pizzas/<int:id>", methods=["GET"])
def get_pizza(id):
    pizza=Pizza.query.filter_by(id=id).first()
    if not pizza:
        return {"error": "Pizza not found"}, 404
    return jsonify({"id":pizza.id,"name":pizza.name,"ingredients":pizza.ingredients})
# restaurantpizza ROUTES
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    data=request.get_json()
    new_RP = RestaurantPizza(
        price=data['price'],
        pizza_id=data['pizza_id'],
        restaurant_id=data['restaurant_id']
    )
    
    # Add to the session and commit to the database
    db.session.add(new_RP)
    db.session.commit()
    
    return jsonify({'message': "restaurant_pizza created successfully"}), 201




if __name__ == "__main__":
    app.run(port=5555, debug=True)
