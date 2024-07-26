from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('rental_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carType TEXT NOT NULL,
            rentalPeriod INTEGER NOT NULL,
            renterName TEXT NOT NULL,
            renterEmail TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offered_cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carType TEXT NOT NULL,
            offerPeriod INTEGER NOT NULL,
            ownerName TEXT NOT NULL,
            ownerEmail TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('/templates/index.html')

@app.route('/rent_car', methods=['POST'])
def rent_car():
    car_type = request.form['carType']
    rental_period = int(request.form['rentalPeriod'])
    renter_name = request.form['renterName']
    renter_email = request.form['renterEmail']

    conn = sqlite3.connect('rental_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rentals (carType, rentalPeriod, renterName, renterEmail)
        VALUES (?, ?, ?, ?)
    ''', (car_type, rental_period, renter_name, renter_email))
    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/offer_car', methods=['POST'])
def offer_car():
    car_type = request.form['carType']
    offer_period = int(request.form['offerPeriod'])
    owner_name = request.form['ownerName']
    owner_email = request.form['ownerEmail']

    conn = sqlite3.connect('rental_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO offered_cars (carType, offerPeriod, ownerName, ownerEmail)
        VALUES (?, ?, ?, ?)
    ''', (car_type, offer_period, owner_name, owner_email))
    conn.commit()
    conn.close()

    return jsonify(success=True)

@app.route('/rental_data', methods=['GET'])
def rental_data():
    conn = sqlite3.connect('rental_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT carType, rentalPeriod, renterName FROM rentals')
    rentals = cursor.fetchall()
    conn.close()
    rental_list = [{'carType': rental[0], 'rentalPeriod': rental[1], 'renterName': rental[2]} for rental in rentals]
    return jsonify(rental_list)

@app.route('/offered_cars_data', methods=['GET'])
def offered_cars_data():
    conn = sqlite3.connect('rental_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT carType, offerPeriod, ownerName FROM offered_cars')
    offered_cars = cursor.fetchall()
    conn.close()
    offered_cars_list = [{'carType': car[0], 'offerPeriod': car[1], 'ownerName': car[2]} for car in offered_cars]
    return jsonify(offered_cars_list)

if __name__ == '__main__':
    app.run(debug=True)
