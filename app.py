from flask import  Flask, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, RestaurantPizza, Pizzas

pizza2 = Pizzas(name="Normal",ingredients="Dough,Tomato,Cheese,Oil")
rest1 = Restaurant(name ="Pizza Inn",address = "123 Ngong Road")
restaurant_pizza1 = RestaurantPizza(restaurant_id=1, pizza_id=1)
restaurant_pizza2 = RestaurantPizza(restaurant_id=1, pizza_id=2)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)



@app.route('/')
def index():
    return "<h2>Hello World</h2>"


@app.route('/restaurants')
def get_all_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []

    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
           'address':restaurant.address
        }
        restaurant_list.append(restaurant_data)

    return jsonify(restaurant_list)

@app.route('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address':restaurant.address
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



 


if __name__ == '__main__':
    app.run()