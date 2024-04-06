# Database Setup Instructions for SeeMeHere

## Introduction
This guide provides instructions on how to set up the MySQL database for the SeeMeHere face recognition attendance management system without revealing sensitive information.

## Pre-requisites
- MySQL server installed and running
- Basic knowledge of operating MySQL commands

## Steps

1. **Open MySQL Terminal**
   - Launch your MySQL client or terminal and log in using your root or an administrative account that has permission to create databases and users.

2. **Create the Database**
   - Execute the following command to create your database:
     ```sql
     CREATE DATABASE attendance_system;
     ```
   - Feel free to replace `attendance_system` with a name that matches your project's requirement.

3. **Create User for the Database**
   - It's a best practice not to use the root account for application connections. Create a dedicated user:
     ```sql
     CREATE USER 'seemeehere_user'@'localhost' IDENTIFIED BY 'your_password_here';
     ```
   - Replace `'your_password_here'` with a strong password.

4. **Grant Permissions**
   - Grant the necessary permissions to your user for the database:
     ```sql
     GRANT ALL PRIVILEGES ON attendance_system.* TO 'seemeehere_user'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - Ensure the database name matches the one you created.

5. **Create Required Tables**
   - Use the SQL schema provided within your project repository to create the required tables. Example:
     ```sql
     USE attendance_system;
	 CREATE TABLE users (
    	id INT AUTO_INCREMENT PRIMARY KEY,
    	first_name VARCHAR(255),
    	last_name VARCHAR(255),
    	email VARCHAR(255),
    	password VARCHAR(255),
    	picture VARCHAR(255),
    	role VARCHAR(255)
);

        ...
     );
     ```
   - Repeat the process for all the necessary tables as per your application schema.

## Finalizing The Setup
After completing the above steps, ensure you update the `config.py` file in your Flask application to use the credentials of the user created and the database information as per your setup:

```python
SECRET KEY = 'Secret key'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'seemeehere_user'
MYSQL_PASSWORD = 'your_password_here'
MYSQL_DB = 'attendanc-system-python'
