from flask_app.config.mysqlconnection import connectToMySQL
import datetime
import re 
from flask import flash


class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.year = data['year']
        self.make = data['make']
        self.description = data['description']
        self.seller_contact = data['seller_contact']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    

    db_name = 'vintage_cars'

    @classmethod
    def get_car_by_id(cls, data):
        query = 'SELECT * FROM cars WHERE id= %(car_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False


    @classmethod
    def get_all(cls):
        query = "SELECT cars.id as id, cars.price as price, cars.model as model, cars.year as year, cars.make as make, cars.status as status, cars.users_id as users_id, users.first_name as first_name, users.last_name as last_name FROM cars LEFT JOIN users on cars.users_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars

    @classmethod
    def showSeller(cls, data):
        query = "SELECT cars.id AS car_id, cars.users_id, users.id AS user_id, users.first_name as first_name, users.last_name as last_name FROM cars LEFT JOIN users ON cars.users_id = users.id WHERE cars.id = %(car_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def showBuyer(cls, data):
        query = "SELECT cars.id AS car_id, cars.buyer_id, users.id AS buyer_id, users.first_name as first_name, users.last_name as last_name FROM cars LEFT JOIN users ON cars.buyer_id = users.id WHERE cars.id = %(car_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False


    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars (price, model, year, make, description, seller_contact, users_id) VALUES ( %(price)s, %(model)s,  %(year)s, %(make)s, %(description)s, %(seller_contact)s, %(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def mark_as_sold(cls, data):
        query = "UPDATE cars SET status = 'Sold', buyer_id = %(buyer_id)s WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def cancel_purchase(cls, data):
        query = "UPDATE cars SET status = 'For Sale', buyer_id = NULL WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_purchases_by_user(cls, data):
        query = "SELECT cars.*, users.first_name AS seller_first_name, users.last_name AS seller_last_name FROM cars LEFT JOIN users ON cars.users_id = users.id WHERE cars.buyer_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, year = %(year)s, make = %(make)s, description = %(description)s, seller_contact = %(seller_contact)s WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_car(r):
        is_valid = True
        if not r['price']:
            flash('Price field is required', 'price')
            is_valid = False
        if r['price']:
            if int(r['price']) < 0:
                flash('Price can not be less then 0', 'price')
                is_valid = False
        if not r['make']:
            flash('Make field is required', 'make')
            is_valid = False
        if not r['model']:
            flash('Model field is required', 'model')
            is_valid = False
        if not r['year']:
            flash('Year field is required', 'year')
            is_valid = False
        if r['year']:
            if int(r['year']) < 0:
                flash('Year can not be less then 0', 'year')
                is_valid = False
            if int(r['year']) > datetime.datetime.now().year:
                flash('Year can not be greater then actual year', 'year')
                is_valid = False
        if not r['seller_contact']:
            flash('Seller Contact field is required', 'seller_contact')
            is_valid = False
        if len(r['description']) < 10:
            flash('Description must be more than 10 characters', 'description')
            is_valid = False
        return is_valid
