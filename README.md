# Vintage Cars Management Flask App

This is a Flask-based web application that allows users to manage vintage cars for sale. Users can add car listings, edit and delete their posts, view cars listed by other users, and purchase cars. The app features user authentication and a responsive user interface built with Bootstrap.

---

## Features
1. **User Authentication**
   - Register, log in, and log out.
   - Passwords are securely hashed using Flask-Bcrypt.

2. **Car Management**
   - Users can add, edit, delete, and view car listings.
   - Only the owner of a car listing can edit or delete it.

3. **Purchases**
   - Users can purchase available cars and view their purchase history.
   - Purchased cars are marked as "Sold."
   - Users can cancel their purchases, making cars available for sale again.

4. **Responsive Design**
   - Fully responsive UI built with Bootstrap 5.

---

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5
- **Database**: MySQL
- **Password Hashing**: Flask-Bcrypt

---

## Prerequisites
- Python 3.8 or higher
- MySQL Server
- Pip (Python package manager)

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone 
   cd vintage-cars-flask

2. **Set Up a Virtual Environment**

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**

pip install -r requirements.txt

4. **Set Up the Database**

Create a MySQL database named vintage_cars and import the schema:

CREATE DATABASE vintage_cars;

USE vintage_cars;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    model VARCHAR(50) NOT NULL,
    make VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    description TEXT,
    seller_contact VARCHAR(15),
    status ENUM('For Sale', 'Sold') DEFAULT 'For Sale',
    buyer_id INT DEFAULT NULL,
    users_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (users_id) REFERENCES users(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE SET NULL
);

5. **Configure the Database Connection**

Open flask_app/config/mysqlconnection.py and update the database credentials:

connection = pymysql.connect(
    host='localhost',
    user='your_mysql_user',
    password='your_mysql_password',
    db='vintage_cars',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)
6. **Run the Application**


python server.py

7. **Access the Application**

Open your browser and go to: http://localhost:5000
