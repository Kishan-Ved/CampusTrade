from flask import Flask, request, jsonify
import mysql.connector
import hashlib
from functools import wraps
import base64
import mysql.connector
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

app.config['SECRET_KEY'] = "IITGNCSDATABASESCAMPUSTRADE"


def get_db_connection(cims = True):
    """Establish a database connection."""
    if cims:
        return mysql.connector.connect(**db_config_cims)
    else:
        return mysql.connector.connect(**db_config_g1)


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
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Validate session and role for the admin (not the member being deleted)
            cursor.execute("SELECT Role, Session FROM Login WHERE MemberID = %s", (request.user_id,))
            login_info = cursor.fetchone()

            print("login_info", login_info["Session"])
            print("token", token)

            if not login_info or login_info['Session'] != token:
                return jsonify({'error': 'Unauthorized'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/isAuth', methods=['GET'])
@token_required
def verify_token():
    return jsonify({
        'success': True,
        'user': {
            'id': request.user_id
        }
    }), 200


# Test route
@app.route('/', methods=['GET'])
def hello():
    return 'API is running!'

@app.route('/addMember', methods=['POST'])
def add_member():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    dob = data.get('dob')
    password = data.get('password')
    contact_no = data.get('contact_no')
    age = data.get('age')
    profile_image = data.get('profile_image')  # Base64 string from frontend
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

        # Convert base64 to binary if image exists
        profile_image_binary = None
        if profile_image:
            # Remove data URL prefix if present
            if 'base64,' in profile_image:
                profile_image = profile_image.split('base64,')[1]
            profile_image_binary = base64.b64decode(profile_image)

        # 3. Insert into memberExt with Profile_Image
        insert_member_ext = """
            INSERT INTO memberExt 
            (Name, Member_ID, Email, Password, Contact_No, Age, Role, Profile_Image) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor2.execute(insert_member_ext, 
            (username, member_id, email, password, contact_no, age, role, profile_image_binary))
        conn2.commit()

        # 4. Insert into MemberGroupMapping
        insert_mapping = """
            INSERT INTO MemberGroupMapping (MemberId, GroupId)
            VALUES (%s, %s)
        """
        cursor.execute(insert_mapping, (member_id, 1))
        conn.commit()

        # 5. Insert into Login with hashed password
        insert_login = """
            INSERT INTO Login (MemberID, Password, Role)
            VALUES (%s, %s, %s)
        """
        default_password = hashlib.md5(data.get('password', '').encode()).hexdigest()
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


@app.route('/addToWishlist', methods=['POST'])
@token_required
def add_to_wishlist():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        # Get data from request
        data = request.get_json()
        if 'product_id' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: product_id'}), 400

        product_id = data['product_id']

        # Connect to database
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Optional: Check if the product exists
        cursor.execute("SELECT Product_ID FROM product_listing WHERE Product_ID = %s", (product_id,))
        if cursor.fetchone() is None:
            return jsonify({'success': False, 'error': 'Product not found'}), 404

        # Check if it's already in the wishlist
        cursor.execute("""
            SELECT * FROM wishlist WHERE Member_ID = %s AND Product_ID = %s
        """, (member_id, product_id))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Product is already in wishlist'}), 200

        # Insert into wishlist
        cursor.execute("""
            INSERT INTO wishlist (Member_ID, Product_ID) VALUES (%s, %s)
        """, (member_id, product_id))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Product added to wishlist'
        }), 201

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error adding to wishlist: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/deletefromwishlist', methods=['DELETE'])
@token_required
def delete_product_wishlist():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        # Get data from request
        data = request.get_json()
        if not data or 'Product_ID' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: Product_ID'}), 400

        product_id = data['Product_ID']

        # Connect to database
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Check if the product exists in wishlist for the user
        cursor.execute("""
            SELECT * FROM wishlist WHERE Member_ID = %s AND Product_ID = %s
        """, (member_id, product_id))
        if cursor.fetchone() is None:
            return jsonify({'success': False, 'message': 'Product not found in wishlist'}), 404

        # Delete the product from wishlist
        cursor.execute("""
            DELETE FROM wishlist WHERE Member_ID = %s AND Product_ID = %s
        """, (member_id, product_id))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Product removed from wishlist'
        }), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error deleting from wishlist: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/getWishlist', methods=['GET'])
@token_required
def get_wishlist():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        # Connect to database
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # Fetch wishlist items for the authenticated user
        cursor.execute("""
            SELECT p.Product_ID, p.Title, p.Description, p.Price, p.Category_ID, p.Condition_, p.Image_Data
            FROM wishlist w
            JOIN product_listing p ON w.Product_ID = p.Product_ID
            WHERE w.Member_ID = %s
        """, (member_id,))

        wishlist_items = cursor.fetchall()

        if not wishlist_items:
            return jsonify({'success': False, 'message': 'Your wishlist is empty'}), 200

        # Format response
        wishlist_data = []
        for item in wishlist_items:
            product = {
                'Product_ID': item['Product_ID'],
                'Title': item['Title'],
                'Description': item['Description'],
                'Price': item['Price'],
                'Category_ID': item['Category_ID'],
                'Condition_': item['Condition_']
            }

            # Handle image conversion
            if item.get('Image_Data'):
                encoded_image = base64.b64encode(item['Image_Data']).decode('utf-8')
                product['image'] = f"data:image/jpeg;base64,{encoded_image}"
            else:
                product['image'] = ""

            wishlist_data.append(product)

        return jsonify({
            'success': True,
            'wishlist': wishlist_data
        }), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error getting wishlist: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



# To Do: Cascade delete from all tables
@app.route('/deleteMember', methods=['DELETE'])
# This is an admin only method, hence, teh decorator @token_required isn't used here, as that only checks for a valid token and not the role
def delete_member():
    # print("here")
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



import base64
import mysql.connector
from flask import request, jsonify
from functools import wraps

# Assuming 'get_db_connection' and 'token_required' are defined elsewhere

@app.route('/addProduct', methods=['POST'])
@token_required
def add_product():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        # Get data from request
        data = request.get_json()

        # Check required fields
        required_fields = ['title', 'description', 'price', 'category_id', 'condition']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        # Extract data
        title = data['title']
        description = data['description']
        price = data['price']
        category_id = data['category_id']
        condition = data['condition']
        
        # Optional: Handle base64-encoded image if it's included
        image_data = None
        if 'image' in data:
            image_base64 = data['image']
            # Decode the base64 string into binary
            image_data = base64.b64decode(image_base64.split(',')[1])  # Remove the "data:image/jpeg;base64," part if present

        # Connect to database
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Insert product with or without the image
        query = """
            INSERT INTO product_listing (Seller_ID, Title, Description, Price, Category_ID, Condition_, Image_Data)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (member_id, title, description, price, category_id, condition, image_data))
        conn.commit()

        # Get the ID of the newly inserted product
        product_id = cursor.lastrowid

        return jsonify({
            'success': True,
            'message': 'Product listed successfully',
            'product_id': product_id
        }), 201

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error adding product: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
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


@app.route('/getProducts', methods=['GET'])
@token_required
def get_products():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        # Connect to database
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # Query to get products not listed by the current user
        cursor.execute("SELECT * FROM product_listing WHERE Seller_ID != %s", (member_id,))
        products = cursor.fetchall()

        # Process each product entry
        for product in products:
            for key, value in list(product.items()):
                if isinstance(value, (datetime.date, datetime.datetime)):
                    product[key] = value.isoformat()

            # Handle image processing
            if product.get('Image_Data'):
                image_data = product['Image_Data']
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                product['image'] = f"data:image/jpeg;base64,{encoded_image}"
            else:
                product['image'] = ""

            # Remove raw image data field from response
            if 'Image_Data' in product:
                del product['Image_Data']

        return jsonify({'products': products}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"Error getting products: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


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
@token_required
def delete_product(product_id):
    try:
        # Get authenticated user ID from token
        member_id = request.user_id

        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # First check if the product belongs to the authenticated user
        cursor.execute("SELECT Seller_ID FROM product_listing WHERE Product_ID = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404

        if str(product['Seller_ID']) != str(member_id):
            return jsonify({'success': False, 'error': 'You are not authorized to delete this product'}), 403

        # Delete product from the product_listing table
        cursor.execute("DELETE FROM product_listing WHERE Product_ID = %s", (product_id,))
        conn.commit()

        return jsonify({'success': True, 'message': 'Product deleted successfully'}), 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error deleting product: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/addComplaint', methods=['POST'])
@token_required
def add_complaint():
    try:
        # Get authenticated user ID from token
        member_id = request.user_id
        data = request.get_json()
        description = data.get('description')

        if not description:
            return jsonify({'success': False, 'error': 'Description is required'}), 400

        # Connect to memberExt database (cs432g1)
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Verify member exists in memberExt
        cursor.execute("SELECT Member_ID FROM memberExt WHERE Member_ID = %s", (member_id,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'error': 'Member not found'}), 404

        # Insert complaint
        insert_query = """
            INSERT INTO complaints (Member_ID, Description)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (member_id, description))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Complaint filed successfully',
            'complaint_id': cursor.lastrowid
        }), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'success': False, 'error': str(err)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/viewComplaints', methods=['GET'])
@token_required
def view_complaints():
    try:
        member_id = request.user_id  # Extracted from JWT

        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        select_query = """
            SELECT Complaint_ID, Description, Status, Filed_On
            FROM complaints
            WHERE Member_ID = %s
        """
        cursor.execute(select_query, (member_id,))
        complaints = cursor.fetchall()

        complaints_list = []
        for complaint in complaints:
            complaints_list.append({
                'complaint_id': complaint[0],
                'description': complaint[1],
                'status': complaint[2],
                'filed_on': complaint[3].strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify({
            'success': True,
            'complaints': complaints_list
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/toggleComplaintStatus', methods=['POST'])
@token_required
def toggle_complaint_status():
    try:
        member_id = request.user_id
        data = request.get_json()
        complaint_id = data.get('complaint_id')

        if not complaint_id:
            return jsonify({'success': False, 'error': 'complaint_id is required'}), 400

        conn = get_db_connection(cims=False)
        cursor = conn.cursor()

        # Fetch current status and verify ownership
        cursor.execute(
            "SELECT Status FROM complaints WHERE Complaint_ID = %s AND Member_ID = %s",
            (complaint_id, member_id)
        )
        result = cursor.fetchone()
        if not result:
            return jsonify({'success': False, 'error': 'Complaint not found or not owned by user'}), 404

        current_status = result[0]
        new_status = 'Resolved' if current_status == 'Open' else 'Open'

        # Update status
        cursor.execute(
            "UPDATE complaints SET Status = %s WHERE Complaint_ID = %s",
            (new_status, complaint_id)
        )
        conn.commit()

        return jsonify({
            'success': True,
            'complaint_id': complaint_id,
            'new_status': new_status
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/viewGroupMembers', methods=['GET'])
@token_required
def view_group_members():
    try:
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # Select only non-sensitive fields
        cursor.execute("""
            SELECT 
                Member_ID, Name, Email, Contact_No, Age, Role, Registered_On
            FROM 
                memberExt
        """)
        members = cursor.fetchall()

        return jsonify({'success': True, 'members': members}), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/getMemberListing', methods=['POST'])
@token_required
def get_member_listing():
    try:
        data = request.get_json()
        member_id = data.get('member_id')

        if not member_id:
            return jsonify({'success': False, 'error': 'member_id is required'}), 400

        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                Product_ID, Title, Description, Price,
                Category_ID, Condition_ AS `Condition`,
                Image_Data, Listed_On
            FROM product_listing
            WHERE Seller_ID = %s
        """, (member_id,))
        
        listings = cursor.fetchall()

        # Convert Image_Data (bytes) to base64 strings
        for listing in listings:
            if listing['Image_Data']:
                listing['Image_Data'] = base64.b64encode(listing['Image_Data']).decode('utf-8')

        return jsonify({'success': True, 'listings': listings}), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/buyProduct', methods=['POST'])
@token_required
def buy_product():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        conn2 = get_db_connection(cims=False)
        cursor2 = conn2.cursor(dictionary=True)

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
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()


@app.route('/getMyTransactions', methods=['GET'])
@token_required
def get_my_transactions():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        # Get transactions
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                Transaction_ID,
                Buyer_ID,
                Seller_ID,
                Title,
                Price,
                Payment_Method,
                Transaction_Date
            FROM transaction_listing
            WHERE Buyer_ID = %s OR Seller_ID = %s
            ORDER BY Transaction_Date DESC
        """
        cursor.execute(query, (member_id, member_id))
        transactions = cursor.fetchall()

        # Convert datetime objects to string to make them JSON serializable
        for transaction in transactions:
            if 'Transaction_Date' in transaction and transaction['Transaction_Date']:
                transaction['Transaction_Date'] = transaction['Transaction_Date'].isoformat()

        return jsonify({
            'success': True,
            'transactions': transactions,
            'count': len(transactions)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# post review endpoint
@app.route('/addReview', methods=['POST'])
@token_required
def add_review():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        # Get review data from request body
        data = request.get_json()
        reviewed_user_id = data.get('Reviewed_User_ID')
        rating = data.get('Rating')
        review_text = data.get('Review_Text')

        if not reviewed_user_id or not rating:
            return jsonify({'error': 'Missing required fields'}), 400

        # Insert review
        conn = get_db_connection(cims=False)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO reviews_ratings (Reviewer_ID, Reviewed_User_ID, Rating, Review_Text, Timestamp)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (member_id, reviewed_user_id, rating, review_text))
        conn.commit()

        return jsonify({'success': True, 'message': 'Review submitted successfully'}), 201

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# Get My Reviews endpoint
@app.route('/getMyReviews', methods=['GET'])
@token_required
def get_my_reviews():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        # Fetch reviews from reviews_ratings
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                Review_ID,
                Reviewer_ID,
                Reviewed_User_ID,
                Rating,
                Review_Text,
                Timestamp
            FROM reviews_ratings
            WHERE Reviewer_ID = %s OR Reviewed_User_ID = %s
            ORDER BY Timestamp DESC
        """
        cursor.execute(query, (member_id, member_id))
        reviews = cursor.fetchall()

        # Convert timestamp to string
        for review in reviews:
            if 'Timestamp' in review and review['Timestamp']:
                review['Timestamp'] = review['Timestamp'].isoformat()

        return jsonify({
            'success': True,
            'reviews': reviews,
            'count': len(reviews)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/myListings', methods=['GET'])
@token_required
def get_my_listings():
    try:
        member_id = request.user_id
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM product_listing
            WHERE Seller_ID = %s
            ORDER BY Product_ID DESC
        """
        cursor.execute(query, (member_id,))
        listings = cursor.fetchall()

        for listing in listings:
            # Handle datetime fields
            for key, value in listing.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    listing[key] = value.isoformat()

            # Handle image
            image_data = listing.get('Image_Data')
            if image_data:
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                listing['image'] = f"data:image/jpeg;base64,{encoded_image}"
            else:
                listing['image'] = ""

            # Remove raw binary field
            if 'Image_Data' in listing:
                del listing['Image_Data']

        return jsonify({
            'success': True,
            'listings': listings,
            'count': len(listings)
        }), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    except Exception as e:
        print(f"Error getting listings: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# view credit logs:
@app.route('/getMyCreditLogs', methods=['GET'])
@token_required
def get_my_credit_logs():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]

        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        member_id = decoded['user_id']

        # Get credit logs
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                credit_ID, 
                member_ID, 
                balance
            FROM credit_logs
            WHERE member_ID = %s
        """
        cursor.execute(query, (member_id,))
        credit_logs = cursor.fetchall()

        return jsonify({
            'success': True,
            'credit_logs': credit_logs,
            'count': len(credit_logs)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

import base64

@app.route('/profile', methods=['GET'])
@token_required
def get_profile():
    try:
        member_id = request.user_id  # From JWT token via @token_required

        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # Get user info (excluding password)
        cursor.execute("""
            SELECT 
                Member_ID, Name, Email, Contact_No,
                Age, Role, Registered_On,
                Profile_Image
            FROM memberExt
            WHERE Member_ID = %s
        """, (member_id,))
        profile_data = cursor.fetchone()

        if not profile_data:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Convert image to base64 if present
        if profile_data.get('Profile_Image'):
            profile_data['Profile_Image'] = base64.b64encode(
                profile_data['Profile_Image']
            ).decode('utf-8')
        else:
            profile_data['Profile_Image'] = None

        # Get products sold count
        cursor.execute("""
            SELECT COUNT(*) AS sold_count
            FROM transaction_listing
            WHERE Seller_ID = %s
        """, (member_id,))
        sold_count = cursor.fetchone()['sold_count']

        # Get products bought count
        cursor.execute("""
            SELECT COUNT(*) AS bought_count
            FROM transaction_listing
            WHERE Buyer_ID = %s
        """, (member_id,))
        bought_count = cursor.fetchone()['bought_count']

        profile_data['productsSold'] = sold_count
        profile_data['productsBought'] = bought_count

        return jsonify({
            'success': True,
            'profile': profile_data
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# view report analytics:
@app.route('/getReportAnalytics', methods=['POST'])
@token_required
def get_report_analytics():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Authorization token missing or malformed'}), 401

        token = token.split(' ')[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

        # No need to extract user_id since we're not filtering

        # Fetch all report analytics data
        conn = get_db_connection(cims=False)
        cursor = conn.cursor(dictionary=True)

        # Step 1: DELETE old data
        cursor.execute("DELETE FROM report_analytics")

        # Step 2: INSERT new report data
        insert_query = """
            INSERT INTO report_analytics (Report_Type)
            SELECT 
                CONCAT('Seller ', Seller_ID, ': ', Total_Sales, ' sales, Revenue: Rs', Total_Revenue)
            FROM (
                SELECT 
                    Seller_ID, 
                    COUNT(*) AS Total_Sales, 
                    SUM(Price) AS Total_Revenue
                FROM transaction_listing
                GROUP BY Seller_ID
            ) AS SalesReport;
        """
        cursor.execute(insert_query)
        conn.commit()


        # Step 3: Fetch updated report data
        select_query = """
            SELECT * FROM report_analytics;
        """
        # print("here")
        cursor.execute(select_query)
        report_data = cursor.fetchall()
        print(report_data)

        conn2 = get_db_connection()
        cursor2 = conn2.cursor(dictionary=True)

        cursor2.execute("INSERT INTO G1_report_analytics (Report_Type) VALUES (%s)", 
                ("Seller Summary Report",))
        conn2.commit()

        return jsonify({
            'success': True,
            'report_analytics': report_data,
            'count': len(report_data)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'cursor2' in locals():
            cursor2.close()
        if 'conn2' in locals():
            conn2.close()

if __name__ == '__main__':
    # conn = mysql.connector.connect(**db_config)
    # print("connected to DB")
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    print(app.url_map)
    app.run(host='0.0.0.0', port=5001, debug=True)
