from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String)


class Pizzas(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'  # Renamed the table to follow the convention

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    price = db.Column(db.Integer)

    # Define relationships with Restaurant and Pizzas models
    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant_pizzas', lazy='dynamic'))
    pizza = db.relationship('Pizzas', backref=db.backref('pizza_restaurants', lazy='dynamic'))

    @validates('price')
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30")
        return value
