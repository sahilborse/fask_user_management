from flask import Blueprint,jsonify , request, render_template
import mysql.connector

main = Blueprint('main', __name__)

db_config = {
    'host': 'localhost',    
    'user': 'root',        
    'password': 'password', 
    'database': 'test_db' 
}# provide your mysql DB

@main.route('/home')
def home():
    return "Hello world!"


@main.route('/users', methods=['GET'])
def get_all_users():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('users.html', users=users)
    

@main.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')

        if not name or not email or not role:
            return "All fields are required", 400

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, role))
            connection.commit()

            cursor.close()
            connection.close()

            return "User added successfully!"

        except mysql.connector.Error as err:
            return f"Error: {err}", 500

    return render_template('new_user.html')
 
    

@main.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return "User not found", 404

    return render_template('user_details.html', user="sahil")
  
