from flask import Flask, request, jsonify
import mysql.connector
import hashlib
from functools import wraps
# import Login
import logging


from flask import Flask, request, jsonify, make_response
import mysql.connector
import bcrypt
import jwt
import datetime
import logging
import hashlib
import psycopg2
# import AddUser
# import Login
import requests
# import UpdateImage

# import logging
from flask_cors import CORS

# Set up logging configuration
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Configure DB connection
db_config_g1 = {
    'host': '10.0.116.125',        # Use your DB server IP
    'user': 'cs432g1',             # Your DB username
    'password': '1234',        # Your DB password
    'database': 'cs432g1'          # Your DB name
}

db_config_cims = {
    'host': '10.0.116.125',        # Use your DB server IP
    'user': 'cs432g1',             # Your DB username
    'password': '1234',        # Your DB password
    'database': 'cs432cims'          # Your DB name
}

app.config['SECRET_KEY'] = "CS"

def get_db_connection(cims = True):
    """Establish a database connection."""
    if cims:
        return mysql.connector.connect(**db_config_cims)
    else:
        return mysql.connector.connect(**db_config_g1)


# add member endpoint: creates entry  in the main cims member table also creates a login table entry
@app.route('/addMember', methods=['POST'])
def add_member():
    data = request.get_json()
    # print("hello")
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')
    password = data.get('password')
    contact_no = data.get('contact_no')
    age = data.get('age')
    profile_image = data.get('profile_image')
    role = data.get('role')

    if not username or not email or not dob:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = mysql.connector.connect(**db_config_cims)
        conn2 = mysql.connector.connect(**db_config_g1)

        cursor = conn.cursor()
        cursor2 = conn2.cursor()

        # 1. Insert into members
        insert_member = """
            INSERT INTO members (UserName, emailID, DoB)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_member, (username, email, dob))
        conn.commit()
        
        # 2. Get the new member's ID
        member_id = cursor.lastrowid

        insert_member_ext = """
            INSERT INTO memberExt (Name, Member_ID, Email, Password, Contact_No, Age, Role) VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor2.execute(insert_member_ext, (username, member_id, email, password, contact_no, age, role))
        conn2.commit()

        insert_mapping = """
            INSERT INTO MemberGroupMapping (MemberId, GroupId)
            VALUES (%s, %s)
        """
        cursor.execute(insert_mapping, (member_id, 1))
        conn.commit()

        # 3. Insert into Login with default password
        insert_login = """
            INSERT INTO Login (MemberID, Password, Role)
            VALUES (%s, %s, %s)
        """
        default_password = hashlib.md5(data.get('password', '').encode()).hexdigest()  # You can hash this later
        cursor.execute(insert_login, (member_id, default_password, 'member'))
        conn.commit()

        return jsonify({
            'message': 'Member and login created successfully',
            'member_id': member_id
        }), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()


@app.route('/addAdmin', methods=['POST'])
def add_admin():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')
    password = data.get('password')

    if not username or not email or not dob:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = mysql.connector.connect(**db_config_cims)
        cursor = conn.cursor()

        # 1. Insert into members
        insert_member = """
            INSERT INTO members (UserName, emailID, DoB)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_member, (username, email, dob))
        conn.commit()

        # 2. Get the new member's ID
        member_id = cursor.lastrowid

        # 3. Insert into Login with default password
        insert_login = """
            INSERT INTO Login (MemberID, Password, Role)
            VALUES (%s, %s, %s)
        """
        default_password = hashlib.md5(data.get('password', '').encode()).hexdigest()  # You can hash this later
        cursor.execute(insert_login, (member_id, default_password, 'admin'))
        conn.commit()

        return jsonify({
            'message': 'Admin and login created successfully',
            'member_id': member_id
        }), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# login endpoint: checks the credentials of the user and returns a token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username, password)
    if not username or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        conn = mysql.connector.connect(**db_config_cims)
        cursor = conn.cursor(dictionary=True)

        # Hash the password
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Fetch MemberID from members table using the username
        cursor.execute("SELECT ID FROM members WHERE UserName = %s", (username,))
        member = cursor.fetchone()
        
        if not member:
            return jsonify({'error': 'User not found'}), 404

        member_id = member['ID']

        # Check credentials in Login table
        cursor.execute("SELECT * FROM Login WHERE MemberID = %s AND Password = %s", (member_id, hashed_password))
        user = cursor.fetchone()
        if user:
            token = jwt.encode({
                'user_id': str(user['MemberID']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            # Update session and expiry in the Login table
            session_expiry = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()
            cursor.execute(
                "UPDATE Login SET Session = %s, Expiry = %s WHERE MemberID = %s",
                (token, session_expiry, member_id)
            )
            conn.commit()

            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# --- Middleware to extract and verify JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated

# --- Protected route ---
@app.route('/verifyToken', methods=['GET'])
@token_required
def verify_token():
    return jsonify({
        'success': True,
        'user': {
            'id': request.user_id
        }
    }), 200

@app.route('/getWishlist', methods=['GET'])
@token_required  # Protect the route with the token_required decorator
def get_wishlist(user_id):
    try:
        conn = mysql.connector.connect(**db_config_g1)
        cursor = conn.cursor()

        # Query the wishlist for the authenticated user
        cursor.execute("SELECT * FROM Wishlist WHERE user_id = %s", (user_id,))
        wishlist_items = cursor.fetchall()

        if not wishlist_items:
            return jsonify({'message': 'No items found in wishlist'}), 404

        return jsonify({'wishlist': wishlist_items}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/deleteMember', methods=['DELETE'])
def delete_member():
    print("here")
    token = request.headers.get('Authorization')  # Bearer <token>
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Authorization token missing or malformed'}), 401

    token = token.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        admin_id = decoded['user_id']  # This is the admin's ID, not the member to be deleted

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validate session and role for the admin (not the member being deleted)
        cursor.execute("SELECT Role, Session FROM Login WHERE MemberID = %s", (admin_id,))
        login_info = cursor.fetchone()

        print("login_info", login_info["Session"])
        print("token", token)

        if not login_info or login_info['Session'] != token or login_info['Role'] != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        member_to_delete = data.get('member_id')

        if not member_to_delete:
            return jsonify({'error': 'member_id is required'}), 400
        
        # Check if the MemberID is mapped to GroupID 1 in MemberGroupMapping
        # Check if the MemberID is mapped to GroupID 1 in MemberGroupMapping
        cursor.execute("SELECT GroupID FROM MemberGroupMapping WHERE MemberId = %s", (member_to_delete,))
        mapping = cursor.fetchone()

        # Now check if the GroupID is 1
        if not mapping or mapping['GroupID'] != 1:
            actual_group = mapping['GroupID'] if mapping else 'None'
            return jsonify({'error': f'Member is not part of GroupID 1. Found GroupID: {actual_group}'}), 403


        # Delete from memberExt using email
        conn2 = get_db_connection(cims=False)
        cursor2 = conn2.cursor()
        cursor2.execute("DELETE FROM memberExt WHERE Member_Id = %s", (member_to_delete,))
        conn2.commit()

        # Delete from Login table
        cursor.execute("DELETE FROM Login WHERE MemberID = %s", (member_to_delete,))
        conn.commit()

        # Delete from members table
        cursor.execute("DELETE FROM members WHERE ID = %s", (member_to_delete,))
        conn.commit()

        # Delete from members table
        cursor.execute("DELETE FROM MemberGroupMapping WHERE MemberID = %s", (member_to_delete,))
        conn.commit()

        return jsonify({'message': 'Member deleted successfully'}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()


@app.route('/addProduct', methods=['POST'])
def add_product():
   
    print(request)
    data = request.get_json()
    print("jang")
    print(data)

    required_fields = ['seller_id', 'title', 'description', 'price', 'category_id', 'condition']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400


    seller_id = data['seller_id']
    title = data['title']
    description = data['description']
    price = data['price']
    category_id = data['category_id']
    condition = data['condition']
    image_url = data['image_url']

    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        query = """
            INSERT INTO product_listing (Seller_ID, Title, Description, Price, Category_ID, Condition_, Image_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (seller_id, title, description, price, category_id, condition, image_url))
        
        conn.commit()

        return jsonify({'message': 'Product listed successfully'}), 201

    except Exception as e:

        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



@app.route('/getCategories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category") 
        categories = cursor.fetchall()
        print(categories)
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Get All Products endpoint
@app.route('/getProducts', methods=['GET'])
def get_products():
    try:
        token = request.headers.get('Authorization')  # Bearer <token>
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']  # This is the admin's ID, not the member to be deleted

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validate session and role for the admin (not the member being deleted)
        cursor.execute("SELECT Role, Session FROM Login WHERE MemberID = %s", (member_id,))
        login_info = cursor.fetchone()

        print("login_info", login_info["Session"])
        print("token", token)

        if not login_info or login_info['Session'] != token:
            return jsonify({'error': 'Unauthorized'}), 403
        print("Authorized")

        conn2 = get_db_connection(cims=False)
        cursor2 = conn2.cursor(dictionary=True)
        cursor2.execute("SELECT * FROM product_listing")
        products = cursor2.fetchall()

        return jsonify({'products': products}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()

# Get Product by ID endpoint
@app.route('/getProduct/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM product_listing WHERE Product_ID = %s", (product_id,))
        product = cursor.fetchone()

        if product:
            return jsonify({'product': product}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Update Product endpoint
@app.route('/updateProduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Update product in the product_listing table
        query = """
            UPDATE product_listing
            SET Seller_ID = %s, Title = %s, Description = %s, Price = %s, Category_ID = %s, Condition_ = %s, Image_URL = %s
            WHERE Product_ID = %s
        """
        cursor.execute(query, (
            data['seller_id'], data['title'], data['description'], data['price'],
            data['category_id'], data['condition'], data.get('image_url'), product_id
        ))
        conn.commit()

        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Delete Product endpoint
@app.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Delete product from the product_listing table
        cursor.execute("DELETE FROM product_listing WHERE Product_ID = %s", (product_id,))
        conn.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/addToWishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()
        query = "INSERT INTO wishlist (Member_ID, Product_ID) VALUES (%s, %s)"
        cursor.execute(query, (data['member_id'], data['product_id']))
        conn.commit()
        return jsonify({'message': 'Added to wishlist'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/buyProduct', methods=['POST'])
def buy_product():
    try:
        token = request.headers.get('Authorization')  # Bearer <token>
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Validate session and role for the admin (not the member being deleted)
        cursor.execute("SELECT Role, Session FROM Login WHERE MemberID = %s", (member_id,))
        login_info = cursor.fetchone()

        print("login_info", login_info["Session"])
        print("token", token)

        if not login_info or login_info['Session'] != token:
            return jsonify({'error': 'Unauthorized'}), 403
        print("Authorized")

        conn2 = get_db_connection(cims=False)
        cursor2 = conn2.cursor(dictionary=True)

        # Implement this
        # Get Product_ID from request body
        data = request.get_json()
        product_id = data.get('Product_ID')
        payment_mode = data.get('payment_mode')
        if not payment_mode:
            return jsonify({'error': 'Payment mode is required'}), 400

        if not product_id:
            return jsonify({'error': 'Product_ID is required'}), 400
        
        # Get Seller_ID and price from product_listing table
        cursor2.execute("SELECT Seller_ID, Price, Title FROM product_listing WHERE Product_ID = %s", (product_id,))
        product_details = cursor2.fetchone()

        if not product_details:
            return jsonify({'error': 'Product not found'}), 404

        seller_id = product_details['Seller_ID']
        price = product_details['Price']
        title = product_details['Title']

        # Delete the product from product_listing table
        cursor2.execute("DELETE FROM product_listing WHERE Product_ID = %s", (product_id,))
        conn2.commit()

        if payment_mode == 'Credit':
            # Check if buyer_id exists in credit_logs
            cursor2.execute("SELECT balance FROM credit_logs WHERE member_id = %s", (member_id,))
            buyer_credit = cursor2.fetchone()

            if buyer_credit:
                # Update buyer's balance
                new_balance = buyer_credit['balance'] + price
                cursor2.execute("UPDATE credit_logs SET balance = %s WHERE member_id = %s", (new_balance, member_id))
            else:
                # Insert new record for buyer with initial balance
                cursor2.execute("INSERT INTO credit_logs (member_id, balance) VALUES (%s, %s)", (member_id, price))

            # Check if seller_id exists in credit_logs
            cursor2.execute("SELECT balance FROM credit_logs WHERE member_id = %s", (seller_id,))
            seller_credit = cursor2.fetchone()

            if seller_credit:
                # Decrease seller's balance
                new_balance = seller_credit['balance'] - price
                cursor2.execute("UPDATE credit_logs SET balance = %s WHERE member_id = %s", (new_balance, seller_id))
            else:
                # Insert new record for seller with negative balance
                cursor2.execute("INSERT INTO credit_logs (member_id, balance) VALUES (%s, %s)", (seller_id, -price))

            conn2.commit()

        # Insert transaction details into transactions table
        transaction_query = """
            INSERT INTO transaction_listing (Buyer_ID, Seller_ID, Title, Price, Payment_Method)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor2.execute(transaction_query, (member_id, seller_id, title, price, payment_mode))
        conn2.commit()

        # Delete from wishlist if it exists
        cursor2.execute("DELETE FROM wishlist WHERE Member_ID = %s AND Product_ID = %s", (member_id, product_id))
        conn2.commit()
        
        return jsonify({'success': True, 'message': 'Product purchased and removed successfully'}), 200
    

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()

# Test route
@app.route('/', methods=['GET'])
def hello():
    return 'API is running!'

if __name__ == '__main__':
    # conn = mysql.connector.connect(**db_config)
    # print("connected to DB")
    print(app.url_map)
    app.run(host='0.0.0.0', port=5001, debug=True)
