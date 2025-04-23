"""
Initialize the database with tables from the ct.sql file.
"""

import os
import sys
from db_engine import Database

def init_database():
    """Initialize the database with tables from the ct.sql file."""
    # Create a new database
    db = Database('campus_trade')
    
    # Create the memberExt table
    member_schema = {
        'Member_ID': {'type': 'int', 'primary_key': True},
        'Name': {'type': 'string', 'nullable': False},
        'Email': {'type': 'string', 'nullable': False},
        'Password': {'type': 'string', 'nullable': False},
        'Contact_No': {'type': 'string', 'nullable': False},
        'Age': {'type': 'int', 'nullable': False},
        'Profile_Image': {'type': 'blob', 'nullable': True},
        'Role': {'type': 'string', 'nullable': False},
        'Registered_On': {'type': 'timestamp', 'nullable': True}
    }
    db.create_table('memberExt', member_schema)
    
    # Create the category table
    category_schema = {
        'Category_ID': {'type': 'int', 'primary_key': True},
        'Category_Name': {'type': 'string', 'nullable': False}
    }
    db.create_table('category', category_schema)
    
    # Create the product_listing table
    product_schema = {
        'Product_ID': {'type': 'int', 'primary_key': True},
        'Seller_ID': {'type': 'int', 'nullable': False},
        'Title': {'type': 'string', 'nullable': False},
        'Description': {'type': 'string', 'nullable': False},
        'Price': {'type': 'float', 'nullable': False},
        'Category_ID': {'type': 'int', 'nullable': False},
        'Condition_': {'type': 'string', 'nullable': False},
        'Image_URL': {'type': 'string', 'nullable': True},
        'Listed_On': {'type': 'timestamp', 'nullable': True}
    }
    db.create_table('product_listing', product_schema)
    
    # Create the transaction_listing table
    transaction_schema = {
        'Transaction_ID': {'type': 'int', 'primary_key': True},
        'Buyer_ID': {'type': 'int', 'nullable': False},
        'Seller_ID': {'type': 'int', 'nullable': False},
        'Title': {'type': 'string', 'nullable': False},
        'Price': {'type': 'float', 'nullable': False},
        'Payment_Method': {'type': 'string', 'nullable': False},
        'Transaction_Date': {'type': 'timestamp', 'nullable': True}
    }
    db.create_table('transaction_listing', transaction_schema)
    
    # Create the credit_logs table
    credit_schema = {
        'Credit_ID': {'type': 'int', 'primary_key': True},
        'Member_ID': {'type': 'int', 'nullable': False},
        'Balance': {'type': 'float', 'nullable': False}
    }
    db.create_table('credit_logs', credit_schema)
    
    # Insert sample data into the memberExt table
    member_table = db.get_table('memberExt')
    sample_members = [
        {
            'Member_ID': 1,
            'Name': 'Alice Johnson',
            'Email': 'alice@example.com',
            'Password': 'hashedpassword1',
            'Contact_No': '9876543210',
            'Age': 22,
            'Role': 'Student'
        },
        {
            'Member_ID': 2,
            'Name': 'Bob Smith',
            'Email': 'bob@example.com',
            'Password': 'hashedpassword2',
            'Contact_No': '9876543211',
            'Age': 35,
            'Role': 'Faculty'
        },
        {
            'Member_ID': 3,
            'Name': 'Charlie Brown',
            'Email': 'charlie@example.com',
            'Password': 'hashedpassword3',
            'Contact_No': '9876543212',
            'Age': 28,
            'Role': 'Staff'
        }
    ]
    
    for member in sample_members:
        member_table.insert(member)
    
    # Insert sample data into the category table
    category_table = db.get_table('category')
    sample_categories = [
        {
            'Category_ID': 1,
            'Category_Name': 'Electronics'
        },
        {
            'Category_ID': 2,
            'Category_Name': 'Books'
        },
        {
            'Category_ID': 3,
            'Category_Name': 'Furniture'
        }
    ]
    
    for category in sample_categories:
        category_table.insert(category)
    
    # Insert sample data into the product_listing table
    product_table = db.get_table('product_listing')
    sample_products = [
        {
            'Product_ID': 1,
            'Seller_ID': 1,
            'Title': 'Laptop',
            'Description': 'Used MacBook Pro, 16GB RAM, 512GB SSD',
            'Price': 800.00,
            'Category_ID': 1,
            'Condition_': 'Used'
        },
        {
            'Product_ID': 2,
            'Seller_ID': 2,
            'Title': 'Python Programming Book',
            'Description': 'Learn Python from scratch',
            'Price': 20.00,
            'Category_ID': 2,
            'Condition_': 'New'
        },
        {
            'Product_ID': 3,
            'Seller_ID': 3,
            'Title': 'Study Table',
            'Description': 'Wooden study table with drawer',
            'Price': 50.00,
            'Category_ID': 3,
            'Condition_': 'Used'
        }
    ]
    
    for product in sample_products:
        product_table.insert(product)
    
    # Create indices for faster searching
    member_table.create_index('Email')
    member_table.create_index('Role')
    product_table.create_index('Seller_ID')
    product_table.create_index('Category_ID')
    
    # Save the database
    db.save()
    
    print("Database initialized successfully!")
    return db

if __name__ == '__main__':
    init_database()
