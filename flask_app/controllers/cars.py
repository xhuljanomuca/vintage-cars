from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.car import Car


@app.route('/add/car')
def addPost():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('addCar.html', loggedUser=User.get_user_by_id(loggedUserData))


@app.route('/create/car', methods=['POST'])
def createCar():
    if 'user_id' not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(request.referrer)
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'year': request.form['year'],
        'make': request.form['make'],
        'description': request.form['description'],
        'seller_contact': request.form['seller_contact'],
        'users_id': session['user_id']
    }
    Car.create_car(data)
    return redirect('/')


@app.route('/cars/<int:id>')
def viewcar(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    creator = Car.showSeller(data)
    buyer = Car.showBuyer(data)
    return render_template('viewCar.html', car=car, loggedUser=loggedUser, creator=creator, buyer=buyer)


@app.route('/cars/edit/<int:id>')
def editcar(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['users_id']:
        return render_template('editCar.html', car=car, loggedUser=loggedUser)
    return redirect(request.referrer)


@app.route('/cars/delete/<int:id>')
def deletePost(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['users_id']:
        Car.delete_car(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/edit/car/<int:id>', methods=['POST'])
def updatecar(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(request.referrer)
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'year': request.form['year'],
        'make': request.form['make'],
        'description': request.form['description'],
        'seller_contact': request.form['seller_contact'],
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['users_id']:
        Car.update_car(data)
        flash('Update succesfull!', 'updateDone')
        return redirect('/')
    return redirect('/')


@app.route('/users/purchases')
def my_purchases():
    if 'user_id' not in session:
        return redirect('/')
    data = {'user_id': session['user_id']}
    purchases = Car.get_purchases_by_user(data)
    loggedUser = User.get_user_by_id(data)
    return render_template('purchases.html', purchases=purchases, loggedUser=loggedUser)



@app.route('/cars/cancel/<int:car_id>')
def cancel_purchase(car_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'car_id': car_id, 'buyer_id': session['user_id']}
    car = Car.get_car_by_id({'car_id': car_id})
    if car['buyer_id'] == session['user_id']:
        Car.cancel_purchase(data)
        flash("Purchase canceled successfully.", "cancelled")
    else:
        flash("Unauthorized action.", "error")
    return redirect('/users/purchases')


@app.route('/cars/order/<int:car_id>')
def order_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'car_id': car_id, 'buyer_id': session['user_id']}
    car = Car.get_car_by_id({'car_id': car_id})
    if car['status'] == 'For Sale':
        Car.mark_as_sold(data)
        flash("Car purchased successfully!", "success")
    else:
        flash("Car is already sold.", "error")
    return redirect('/cars')


