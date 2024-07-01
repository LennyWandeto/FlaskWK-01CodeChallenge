# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(
#     naming_convention={
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     }
# )

# db = SQLAlchemy(metadata=metadata)


# class Restaurant(db.Model, SerializerMixin):
#     __tablename__ = "restaurants"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     address = db.Column(db.String)

#     # add relationship
#     # restaurant_pizzas = db.relationship('RestaurantPizza', back_populates="restaurant", cascade='all, delete-orphan')
#     pizzas = db.relationship("Pizza",secondary = "restaurant_pizzas",backref="restaurant", lazy=True)

#     # add serialization rules
#     serialize_rules = ('-pizzas.restaurants')

#     def __repr__(self):
#         return f"<Restaurant {self.name}>"


# class Pizza(db.Model, SerializerMixin):
#     __tablename__ = "pizzas"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     ingredients = db.Column(db.String(255))

#     # add relationship
#     # restaurant_pizzas = db.relationship('RestaurantPizza' ,back_populates="pizza", cascade='all, delete-orphan')
#     restaurants = db.relationship("Restaurant",secondary = "restaurant_pizzas",backref="pizza", lazy=True)

#     # add serialization rules
#     serialize_rules = ('-restaurant.pizzas')

#     def __repr__(self):
#         return f"<Pizza {self.name}, {self.ingredients}>"


# class RestaurantPizza(db.Model, SerializerMixin):
#     __tablename__ = "restaurant_pizzas"

#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer, nullable=False)
    

#     # add relationships
#     restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
#     pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))

#     restaurant = db.relationship('Restaurant', backref="restaurant_pizzas", cascade ="all, delete")
#     pizza = db.relationship('Pizza', backref="restaurant_pizzas", cascade="all,delete")



#     # add serialization rules
#     serialize_rules = ('-restaurants.restaurant_pizzas', '-pizzas.restaurant_pizzas')

#     # add validation
#     @validates('price')
#     def validate_price(self, key, value):
#         if isinstance(value, int) and (value >= 1 and value <= 30):
#             return value
#         else:
#             raise ValueError('Price must be an integer between 1 and 30')
        

#     def __repr__(self):
#         return f"<RestaurantPizza ${self.price}>"

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)



class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    #  relationship of M:M: Restaurant to Pizza through RestaurantPizza
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants', lazy=True)

    # Serialization rules to prevent recursion
    serialize_rules = ('-pizzas.restaurants',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    #  relationship of M:M: Pizza to Restaurant through RestaurantPizza
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas', lazy=True)

    # Serialization rules to prevent recursion
    serialize_rules = ('-restaurants.pizzas',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    #  foreign keys
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id", ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id", ondelete='CASCADE'))

    #  relationships with cascading delete
    pizza = db.relationship("Pizza", backref="restaurant_pizzas", cascade="all, delete")
    restaurant = db.relationship("Restaurant", backref="restaurant_pizzas", cascade="all, delete")

    def __repr__(self):
        return
