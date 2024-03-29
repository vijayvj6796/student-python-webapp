# Student Registration System

This is a simple web application built with Flask that allows students to register and login.

## Features

- **User Authentication**: Users can register, login, and logout securely.
- **Student Registration**: Registered users can add their information such as name, class, roll number, email, and phone number.
- **Data Storage**: User data and student registration details are stored in a MySQL database.
- **Password Hashing**: User passwords are securely hashed using bcrypt before storing them in the database.
- **Nginx Configuration**: The application is served using Nginx as a reverse proxy, providing better performance and security.

## Prerequisites

- Python 3.x
- Flask
- MySQL
- Nginx

## Installation

1. Clone the repository:

git clone https://github.com/vijayvj6796/student-python-webapp.git
cd student-registration-system


2. Install the required Python packages:

pip install -r requirements.txt


3. Set up MySQL database:

- Create a new database named `student`.
- Update the MySQL configuration in `app.py` with your database credentials.

4. Configure Nginx:

- Update the Nginx configuration file to proxy requests to the Flask application.
- Restart Nginx to apply the changes.

5. Run the Flask application:

python app.py


6. Access the application:

Navigate to `http://localhost` in your web browser to access the application.

## Usage

1. Register: Create a new account by providing a username and password.
2. Login: Log in to your account with the registered username and password.
3. Student Registration: After logging in, you can add your information in the registration form.
4. Logout: Click on the "Logout" button to log out from your account.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

