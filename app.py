from flask import Flask, render_template, request, redirect, session, jsonify
import bcrypt
import pymysql.cursors
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'mysql',
    'password': 'PASSWORD',
    'db': 'student',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Route to serve login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch username and password from form
        username = request.form['username']
        password = request.form['password']

        # Log form data
        logger.debug("Form data received - Username: %s, Password: %s", username, password)

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)
        logger.info("Connected to MySQL database")

        try:
            with connection.cursor() as cursor:
                # Execute SQL query to retrieve user data
                sql = "SELECT * FROM users WHERE username = %s"
                logger.debug("Executing SQL query: %s", sql)
                cursor.execute(sql, (username,))
                user = cursor.fetchone()
                logger.debug("User data retrieved from database: %s", user)

                # Check if user exists and password is correct
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    session['username'] = username
                    logger.info("User %s authenticated successfully", username)
                    return redirect('/index')
                else:
                    logger.error("Login failed for username: %s", username)
                    return "Invalid username or password"

        except Exception as e:
            logger.error("Error during login: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return render_template('login.html')

# Route to serve index page
@app.route('/index')
def index():
    return render_template('index.html')

# Route to serve signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Execute SQL query to insert new user
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password))
                connection.commit()
                logger.info("User %s registered successfully", username)
                return redirect('/login')

        except Exception as e:
            logger.error("Error during user registration: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return render_template('signup.html')

# Route to serve registration page
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        student_class = request.form['class']
        roll_number = request.form['roll_number']
        email = request.form['email']
        phone = request.form['phone']
   
        # Log form data
        logger.debug("Form data received - Name: %s, class: %s, Roll Number: %s, Email: %s, Phone: %s", name, roll_number, email, phone)

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)
        logger.info("Connected to MySQL database")

        try:
            with connection.cursor() as cursor:
                # Execute SQL query to insert data into 'students' table
                sql = "INSERT INTO student (name, class, roll_number, email, phone) VALUES (%s,%s, %s, %s, %s)"
                cursor.execute(sql, (name, student_class,  roll_number, email, phone))
                connection.commit()
                logger.info("Data inserted into 'students' table")

        except Exception as e:
            logger.error("Error during registration: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return redirect('/index')  # Redirect to index page after successful registration


# Route to logout
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

