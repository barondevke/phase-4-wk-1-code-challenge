from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizzas

# Create instances of Pizzas, Restaurant, and RestaurantPizza
pizza2 = Pizzas(name="Normal", ingredients="Dough, Tomato, Cheese, Oil")
rest2 = Restaurant(name="Road Inn", address="123 Jogoo Road")
restaurant_pizza1 = RestaurantPizza(restaurant_id=1, pizza_id=1)
restaurant_pizza2 = RestaurantPizza(restaurant_id=1, pizza_id=2)

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Flask-Migrate extension
migrate = Migrate(app, db)

# Initialize the SQLAlchemy database
db.init_app(app)

# Define the index route
@app.route('/')
def index():
    return "<h2>Hello World</h2>"

# Define a route to get all restaurants
@app.route('/restaurants')
def get_all_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []

    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address  # Added 'address' field
        }
        restaurant_list.append(restaurant_data)

    return jsonify(restaurant_list)

# Define a route to get all pizzas
@app.route('/pizzas')
def get_all_pizzas():
    pizzas = Pizzas.query.all()
    pizzas_list = []

    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizzas_list.append(pizza_data)

    return jsonify(pizzas_list)

# Define a route to add RestaurantPizza entries (associations between restaurants and pizzas)
@app.route('/restaurant_pizzas', methods=['POST'])
def add_RestaurantPizzas():
    new_RestaurantPizza = RestaurantPizza(
        restaurant_id=request.form.get("restaurant_id"),
        pizza_id=request.form.get("pizza_id")
    )
    db.session.add(new_RestaurantPizza)
    db.session.commit()
    
    # Retrieve the added pizza's information
    pizza = Pizzas.query.filter(Pizzas.id == request.form.get('pizza_id')).first()
    
    pizza_data = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }
    
    return jsonify(pizza_data), 201  # Return the pizza data and a 201 status code

# Define a route to get restaurant information by ID and optionally delete a restaurant
@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    
    if request.method == 'GET':
        if restaurant is None:
            return jsonify({"error": "Restaurant not found"}), 404

        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }

        RestaurantPizzas = RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == id).all()
        pizza_list = []

        for restaurantPizza in RestaurantPizzas:
            pizza = Pizzas.query.filter(Pizzas.id == restaurantPizza.pizza_id).first()
            if pizza:
                pizza_data = {
                    'id': pizza.id,
                    'name': pizza.name,
                    'ingredients': pizza.ingredients,
                }
                pizza_list.append(pizza_data)

        restaurant_data['pizzas'] = pizza_list

        return jsonify(restaurant_data)
    
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        
        response_body = {}
        response = jsonify(response_body), 200
        
        return response

if __name__ == '__main__':
    app.run()
