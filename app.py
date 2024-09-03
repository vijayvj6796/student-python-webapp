from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import bcrypt
import pymysql.cursors
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key'


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('Support_Kodekloud','MAIL_USERNAME')
# Initialize Flask-Mail
mail = Mail(app)

# Token serializer for generating and validating tokens
serializer = URLSafeTimedSerializer(app.secret_key)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MySQL configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@app.route('/')
def home():
    return render_template('List.html')

@app.route('/glow', methods=['GET', 'POST'])
def glow():
    return render_template('glow.html')

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
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to MySQL database
        connection = pymysql.connect(**db_config)

        try:
            with connection.cursor() as cursor:
                # Execute SQL query to insert new user
                sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, hashed_password, email))
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
                sql = "INSERT INTO user_info (name, class, roll_number, email, phone) VALUES (%s,%s, %s, %s, %s)"
                cursor.execute(sql, (name, student_class,  roll_number, email, phone))
                connection.commit()
                logger.info("Data inserted into 'students' table")

        except Exception as e:
            logger.error("Error during registration: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return redirect('/index')  # Redirect to index page after successful registration

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Verify that the email exists in the database
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

                if user:
                    # Generate a secure token
                    token = serializer.dumps(email, salt='password-reset-salt')
                    
                    # Create the password reset link
                    reset_link = url_for('reset_password_token', token=token, _external=True)

                    # Send the reset email
                    msg = Message('Password Reset Request', recipients=[email])
                    msg.body = f"To reset your password, click the following link: {reset_link}\n\nIf you did not request a password reset, please ignore this email."
                    mail.send(msg)
                    
                    logger.info("Password reset link sent to %s", email)
                    return "A password reset link has been sent to your email address."

                else:
                    logger.error("Password reset requested for non-existing email: %s", email)
                    return "This email is not registered."

        except Exception as e:
            logger.error("Error during password reset request: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return render_template('reset_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    try:
        # Validate the token (expires after 3600 seconds or 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        logger.error("Invalid or expired token: %s", e)
        return "The reset link is invalid or has expired."

    if request.method == 'POST':
        # Get the new password from the form
        new_password = request.form['password']
        
        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Update the password in the database
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET password = %s WHERE email = %s"
                cursor.execute(sql, (hashed_password, email))
                connection.commit()
                logger.info("Password updated successfully for %s", email)
                return redirect('/login')

        except Exception as e:
            logger.error("Error updating password: %s", e)
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            connection.close()

    return render_template('reset_password_form.html', token=token)


# Route to logout
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

