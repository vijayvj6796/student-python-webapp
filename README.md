# Student Registration System

This is a simple web application built with Flask that allows students to register, login, recover forgotten passwords, and manage their information.

## Description

This application provides a student registration and login system built with Flask. It includes secure user authentication, a password recovery feature via email, and integration with MySQL for data storage.

## Features

- **User Authentication**: Users can register, login, recover their password, and logout securely.
- **Student Registration**: Registered users can add their information such as name, class, roll number, email, and phone number.
- **Password Recovery**: Users can request a password reset link if they forget their password, which is sent via email.
- **Data Storage**: User data and student registration details are stored in a MySQL database.
- **Password Hashing**: User passwords are securely hashed using bcrypt before storing them in the database.
- **Nginx Configuration**: The application is served using Nginx as a reverse proxy, providing better performance and security.

## Prerequisites

- Python 3.12
- Flask
- MySQL
- Nginx
- Flask-Mail (for sending password recovery emails)
- itsdangerous (for generating secure tokens for password recovery)
- SSH Access with an SSH Key (for secure access to the remote server)

## Installation and Setup

1. **Set Up SSH Tunnel for Remote MySQL Access (if needed):**


    If your MySQL database is hosted on a remote server, use SSH tunneling to connect:
```bash
    sudo apt install mysql-client
    ssh -i yourpemkey.pem -f username@<mysql_server_ip> -L 3307:127.0.0.1:3306 -N
```
# 3307 is your local IP , 3306 is mysql default port number 
    Then, connect to the MySQL database using:
``` bash
    mysql -u mysql_user -p -h 127.0.0.1 -P 3307
```
2. **Set Up a Python Virtual Environment:**
``` bash
    apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
```
3. **Clone the repository:**

    git clone https://github.com/vijayvj6796/student-python-webapp.git
    cd student-python-webapp
4. **Install the required Python packages:**

    pip install -r requirements.txt

    - Update the MySQL configuration in `app.py` with your database credentials:

    app.config['MYSQL_HOST'] = 'your_host'
    app.config['MYSQL_USER'] = 'your_user'
    app.config['MYSQL_PASSWORD'] = 'your_password'
    app.config['MYSQL_DB'] = 'student'

6. **Enable Gmail App Password for Flask-Mail (if using Gmail):**

    If you have enabled 2-Step Verification on your Google account, you need to generate an App Password to allow your Flask application to send emails. Follow these steps:

    1. Go to your Google Account settings.
    2. Navigate to Security > App Passwords.
    3. Select the app (e.g., "Mail") and the device (e.g., "Other" and name it "Flask App").
    4. Google will generate a 16-character App Password. Use this instead of your regular Google password in your Flask-Mail configuration.

    -Update your app.config like this:
    
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your-app-password'

8. **Set Up Nginx as a Reverse Proxy:**

    - Edit the Nginx configuration file:

    sudo nano /etc/nginx/sites-available/student-python-webapp

    - Add the following configuration:

    ```nginx
    server {
        listen 80;
        server_name <your domain_name>;

        # Serve the login page by default
        location / {
            rewrite ^/$ /login redirect; # Redirect root URL to /login
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Pass requests to the Flask application
        location /login {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /signup {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /index {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

    - Enable the Nginx configuration and test:

    sudo ln -s /etc/nginx/sites-available/student-python-webapp /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx

8. **Set Up Gunicorn for Running the Flask Application:**

    - Create a systemd service file for Gunicorn:

    sudo nano /etc/systemd/system/flaskapp.service

    - Add the following configuration:

    ```ini
    
    [Unit]
    Description=Flask Application
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/path/to/your/project
    ExecStart=/path/to/your/project/venv/bin/python /path/to/your/project/app.py
    Restart=always
    StandardOutput=append:/path/to/your/project/logs/flaskapp.log
    StandardError=append:/path/to/your/project/logs/flaskapp_error.log

    [Install]
    WantedBy=multi-user.target

    ```

    - Replace `/path/to/your/project` with the actual path to your Flask project.

    - Start and enable the Gunicorn service:

    ```bash
    sudo systemctl start flaskapp
    sudo systemctl enable flaskapp
    ```

9. **Run the Flask application locally (for development):**

    ```bash
    python app.py
    ```

10. **Access the application:**

    Navigate to `http://localhost` or `http://your_domain.com` in your web browser to access the application.

## Usage

1. **Register**: Create a new account by providing a username and password.
2. **Login**: Log in to your account with the registered username and password.
3. **Forgot Password**: If you forget your password, use the "Forgot Password?" link to receive a password reset link via email.
4. **Student Registration**: After logging in, you can add your information in the registration form.
5. **Logout**: Click on the "Logout" button to log out from your account.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.